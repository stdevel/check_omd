# test

This repository contains a [Vagrantbox](Vagrantfile) for checking the plugin.

In order to run the tests, you will need:

- Python
- [`testinfra`](https://pypi.org/project/testinfra)
- [`pytest`](https://pypi.org/project/pytest)
- [Vagrant](https://vagrantup.com)
- A supported hypervisor, such as [Oracle VirtualBox](https://virtualbox.org)

## Procedure

Open a shell, move to this folder an run the following command to create the testing VM:

```shell
$ vagrant up
...
```

This will take a couple of minutes, as a CentOS 7 template is downloaded and deployed. It will also automatically install and configure OMD.

Afterwards, create a SSH configuration and run the tests using `pytest`:

```shell
$ vagrant ssh-config > .vagrant/ssh_config
$ py.test --connection=ssh --ssh-config .vagrant/ssh_config --hosts=omd test_plugin.py --sudo
...
=== 3 passed in 4.01s ===
```
