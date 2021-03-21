"""
Plugin unit tests
"""
import os

def test_exclude(host):
    """
    Check if services can be excluded
    """
    with host.sudo("icinga2"):
        # stop rrdcached
        host.run("omd stop rrdcached")
        cmd_status = host.run(
            "python3 /opt/check_omd/check_omd.py -x rrdcached"
        )
        assert cmd_status.rc == 0


def test_warning(host):
    """
    Check if critical services can be limited to warnings
    """
    with host.sudo("icinga2"):
        # stop rrdcached
        host.run("omd stop rrdcached")
        cmd_status = host.run(
            "python3 /opt/check_omd/check_omd.py -w rrdcached"
        )
        assert cmd_status.rc == 1


def test_heal(host):
    """
    Check if crashed services can be restarted
    """
    with host.sudo("icinga2"):
        # stop rrdcached
        host.run("omd stop rrdcached")
        cmd_status = host.run(
            "python3 /opt/check_omd/check_omd.py -H"
        )
        assert cmd_status.rc == 1
        assert "restarted service" in cmd_status.stdout.strip().lower()
