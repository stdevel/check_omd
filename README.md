# check_omd
``check_omd`` is a Nagios / Icinga plugin for checking a particular [OMD](http://www.omdistro.org) site's services.

# Requirements
I successfully tested the plugin with OMD site versions 1.20 and 1.30. As the plugin needs to be executed **by the site user**, a sudo rule is needed. A template (``check_omd-sudo-template``) is part of the repository.

# Usage
By default, the script checks all services of the site - it is also possible to exclude services if they are predicted to fail in your environment (``-x`` / ``--exclude`` parameters).

The following parameters can be specified:

| Parameter | Description |
|:----------|:------------|
| `-d` / `--debug` | enable debugging outputs (*default: no*) |
| `-h` / `--help` | shows help and quits |
| `-x` / `--exclude` | excludes a particular service from the check |
| `--version` | prints programm version and quits |

## Examples
The following example indicates an running OMD site:
```
$ /opt/check_omd.py 
OK: OMD site 'stankowic' services are running.
```

A site with a failed ``nagios`` service:
```
$ /opt/check_omd.py 
CRITICAL: OMD site 'hansel' has failed service(s): 'nagios'
```

OMD site ``giertz`` with a well-known daemon, that's crashing sometimes:
```
$ /opt/check_omd.py -x npcd
OK: OMD site 'giertz' services are running.
```

# Installation
To install the plugin, move the Python script, the NRPE configuration and sudo rule into their appropriate directories. The paths may vary, depending on your Linux distribution and architecture. For RPM-based distribtions, proceed with the following steps:
```
# mv check_omd.cfg /etc/nrpe.d/
# mv check_omd.py /usr/lib64/nagios/plugins
# mv check_omd-sudo-template /etc/sudoers.d/
# chmod +x /usr/lib64/nagios/plugins/check_omd.py
# chmod 0440 /etc/sudoers.d/check_omd-sudo-template
# service nrpe restart
```
Make sure to alter the sudo configuration to match your OMD site name, e.g.:
```
nrpe ALL = (stankowic) NOPASSWD: /usr/lib64/nagios/plugins/check_omd.py
```

It also possible to create a RPM file for your Linux distribution with the RPM spec file:
```
$ rpmbuild -ba nagios-plugins-check_omd.spec
```
The RPM spec has been tested on Enterprise Linux 5 to 7, i386 and x86_64.

# Configuration
Inside Nagios / Icinga you will need to configure a remote check command, e.g. for NRPE:
```
#check_nrpe_omd
define command{
    command_name        check_nrpe_omd
    command_line        $USER1$/check_nrpe -H $HOSTADDRESS$ -c check_omd -a $ARG1$
}
```

Configure the check for a particular host, e.g.:
```
#SRV: omd stankowic
define service{
        use                             generic-service
        host_name                       st-mon02
        service_description             SRV: omd stankowic
        check_command                   check_nrpe_omd!stankowic
}
```

# Trobleshooting
##Plugin not executed as OMD site user
The plugin will not work if is not executed as site user:
```
$ whoami
taylor
$ ./check_omd.py 
UNKNOWN: unable to check site: 'omd: no such site: taylor' - did you miss running this plugin as OMD site user?
```
