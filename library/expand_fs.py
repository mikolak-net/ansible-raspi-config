#!/usr/bin/python
# -*- coding: utf-8 -*-
# Made because matching the condition in Jinja2 was a royal pain the a**

from ansible.module_utils.basic import *

MAIN_PARTITION_NAME = "/dev/mmcblk0p2"


def main():
    module = AnsibleModule(argument_spec=dict())

    (rc, out, err) = module.run_command(["sudo", "raspi-config", "--expand-rootfs"], check_rc=True)

    fs_expanded = (lambda x, y: x-y)(*[int(l.split()[2]) for l in out.split("\n") if l.startswith(MAIN_PARTITION_NAME)])
    module.exit_json(changed=fs_expanded, stdout=out, stderr=err)


main()