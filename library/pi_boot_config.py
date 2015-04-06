#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ensures the given config value is set.

from ansible.module_utils.basic import *


# START - common module code - yay for copy-paste
BOOT_CONFIG_PATH = "/boot/config.txt"

RASPI_CONFIG_BIN = "/usr/bin/raspi-config"


class ConfigFile:

    @staticmethod
    def __param_string(param, value):
        return param+"="+value

    def __init__(self, file_name=BOOT_CONFIG_PATH):
        self.is_changed = False
        self.file_name = file_name

        with open(self.file_name) as fp:
            self.lines = fp.readlines()

    def __find_starting_with(self, searched):
        try:
            return [x.find(self.__param_string(searched, "")) == 0 for x in self.lines].index(True)
        except ValueError:
            return -1

    def set(self, param, value):
        # search for an uncommented line, and a commented one if that fails
        line_num = self.__find_starting_with(param)
        if line_num == -1:
            line_num = self.__find_starting_with('#'+param)

        # ...and finally just create an empty line
        if line_num == -1:
            line_num == len(self.lines)
            self.lines.append("")

        target_value = self.__param_string(param, value)+"\n"
        if self.lines[line_num] != target_value:
            self.lines[line_num] = target_value
            self.is_changed = True
            with open(self.file_name, 'w') as fp:
                fp.writelines(self.lines)
            return True
        else:
            return False
# END - common module code - yay for copy-paste

CONFIG_VALS = "config_vals"


def main():
    module = AnsibleModule(argument_spec={
        CONFIG_VALS: {"required": True, "type": "dict"}
    }
    )

    config_vals = module.params.get(CONFIG_VALS)

    config = ConfigFile()

    out = ""
    err = ""

    # sanitize from auto-typing in YAML
    config_vals = dict((str(key), str(val)) for (key, val) in config_vals.iteritems())

    for (key, val) in config_vals.iteritems():
        try:
            modified = config.set(key, val)
            if modified:
                out += "\nModified "+key+" to "+val
            else:
                out += "\n"+key+" was already set to "+val
        except Exception as e:
            err = "Error when writing config: "+str(e)
            module.fail_json(changed=config.is_changed, msg=err, stdout=out, stderr=err)

    module.exit_json(changed=config.is_changed, stdout=out, stderr=err)


main()