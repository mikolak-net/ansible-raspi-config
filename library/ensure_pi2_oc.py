#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ensures Pi2 have the correct "overclocking" setting

from ansible.module_utils.basic import *
import re

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

CPU_INFO_PATH = "/proc/cpuinfo"

CPU_PI2 = "Pi2"

CPU_TYPES = "cpu_types"

CONFIG_OC_REGEXP = re.compile("set_overclock " + CPU_PI2 + " (?P<arm_freq>\d+) (?P<core_freq>\d+) (?P<sdram_freq>\d+) (?P<over_voltage>\d+)")


def read_oc_params():
    with open(RASPI_CONFIG_BIN) as fp:
        oc_config = CONFIG_OC_REGEXP.search(fp.read()).groupdict()
    return oc_config


def main():
    module = AnsibleModule(argument_spec={
        CPU_TYPES: {"required": True, "type": "dict"}
    }
    )

    pi2_cpu = module.params.get(CPU_TYPES)[CPU_PI2]

    is_pi2 = False

    with open(CPU_INFO_PATH) as fp:
        is_pi2 = any(x.find(pi2_cpu) > -1 for x in fp.readlines())

    if is_pi2:
        oc_config = read_oc_params()
        config_file = ConfigFile()
        for (param, value) in oc_config.iteritems():
            config_file.set(param, value)
        module.exit_json(changed=config_file.is_changed, msg="Is Pi2, ensured optimum CPU params.")
    else:
        module.exit_json(changed=False, msg="CPU chipset does not appear to be a Pi2 (but you can still custom-OC it by setting 'raspi_config_other_options!).")

main()