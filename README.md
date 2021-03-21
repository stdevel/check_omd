# check_omd

![Example Icinga screenshot](https://raw.githubusercontent.com/stdevel/check_omd/master/Icinga_Screenshot.jpg "Example Icinga screenshot")

``check_omd`` is a Nagios / Icinga plugin for checking a particular [OMD](http://www.omdistro.org) site's services.

## Requirements

I successfully tested the plugin with OMD site versions 1.20 to 2.70. As the plugin needs to be executed **by the site user**, a sudo rule is needed. A template (*``check_omd-sudo-template``*) is part of the repository.

## Usage

By default, the script checks all services of the site - it is also possible to exclude services if they are predicted to fail in your environment (*``-x`` / ``--exclude`` parameters*).

The following parameters can be specified:

| Parameter | Description |
|:----------|:------------|
| `-d` / `--debug` | enable debugging outputs (*default: no*) |
| `-h` / `--help` | shows help and quits |
| `-w` / `--warning` | defines one or more services that only should throw a warning if not running (*useful for fragile stuff like npcd*) |
| `-x` / `--exclude` | excludes a particular service from the check |
| `-H` / `--heal` | automatically restarts the services that are not running |
| `--version` | prints programm version and quits |

## Examples

The following example indicates an running OMD site:

```shell
$ ./check_omd.py
OK: OMD site 'stankowic' services are running.
```

A site with a failed ``nagios`` service:

```shell
$ ./check_omd.py
CRITICAL: OMD site 'hansel' has failed service(s): 'nagios'
```

OMD site ``giertz`` with a well-known daemon, that's crashing sometimes:

```shell
$ ./check_omd.py -x npcd
OK: OMD site 'giertz' services are running.
```

OMD site ``clpmchn``, excluding npcd from throwing critical states:

```shell
$ ./check_omd.py -w npcd
WARNING: OMD site 'clpmchn' has service(s) in warning state: 'npcd'
```

## Installation

To install the plugin, move the Python script, the agent configuration and sudo rule into their appropriate directories. The paths may vary, depending on your Linux distribution and architecture. For RPM-based distribtions, proceed with the following steps:

```shell
# mv check_omd.py /usr/lib64/nagios/plugins
# mv check_omd-sudo-template /etc/sudoers.d/
# chmod +x /usr/lib64/nagios/plugins/check_omd.py
# chmod 0440 /etc/sudoers.d/check_omd-sudo-template
```

When using NRPE, copy the appropriate configuration and restart the daemon:

```shell
# mv check_omd.cfg /etc/nrpe.d/
# service nrpe restart
```

When using Icinga2, copy the configuration to **ITL** (*Icinga Template Library*), e.g.:

```shell
# cp check_omd.conf /usr/share/icinga2/include/plugins-contrib.d/
# service icinga2 restart
```

Make sure to alter the sudo configuration to match your OMD site name, e.g.:

```shell
nrpe ALL = (stankowic) NOPASSWD: /usr/lib64/nagios/plugins/check_omd.py
```

It also possible to create a RPM file for your Linux distribution with the RPM spec file:

```shell
$ rpmbuild -ba nagios-plugins-check_omd.spec
...
```

The RPM spec has been tested on Enterprise Linux 5 to 7, i386 and x86_64. Currently, the RPM package only includes NRPE-related configuration, Icinga2 will follow.

## Configuration

### Nagios / Icinga 1.x

Inside Nagios / Icinga you will need to configure a remote check command, e.g. for NRPE:

```text
#check_nrpe_omd
define command{
    command_name        check_nrpe_omd
    command_line        $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_omd -a $ARG1$
}
```

Configure the check for a particular host, e.g.:

```text
#SRV: omd stankowic
define service{
        use                             generic-service
        host_name                       st-mon02
        service_description             SRV: omd stankowic
        check_command                   check_nrpe_omd!stankowic
}
```

### Icinga2

Define a service like this:

```text
apply Service for (SITE => config in host.vars.omd_sites) {
  import "generic-service"
  check_command = "check_omd"
  if (host.name != NodeName) {
    command_endpoint = host.name
  }
  vars += config
  assign where host.vars.app == "omd"
  ignore where host.vars.noagent
}
```

Create ``omd_site`` dictionaries for your hosts and assign the ``app`` variable:

```text
object Host "st-mon04.stankowic.loc" {
  import "linux-host"
  ...
  vars.app = "omd"
  ...
  vars.omd_sites["PROC: OMD pinkepank"] = {
    omd_site = "pinkepank"
  }
  vars.omd_sites["PROC: OMD giertz"] = {
    omd_site = "giertz"
  }
```

Validate the configuration and reload the Icinga2 daemon:

```shell
# icinga2 daemon -C
# service icinga2 reload
```

## Troubleshooting

### Plugin not executed as OMD site user

The plugin will not work if is not executed as site user:

```shell
$ whoami
taylor
$ ./check_omd.py
UNKNOWN: unable to check site: 'omd: no such site: taylor' - did you miss running this plugin as OMD site user?
```

An error message like this will be displayed if multiple OMD sites are available and you're running the plugin as `root`:

```shell
# ./check_omd.py
UNKOWN: unable to check site, it seems this plugin is executed as root (use OMD site context!)
````
