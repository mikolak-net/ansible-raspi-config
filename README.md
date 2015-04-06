raspi-config
=========

A configuration role for Raspbian-based Raspberry Pi machines. Provides the following features:
 - exposes and/or emulates those `raspi-config` options that are most relevant to headless servers (see _Rule Variables_),
 - allows to add user-specified settings to `/boot/config.txt` via the `raspi_config_other_options` variable,
 - warns about leaving the default credentials accessible.

Requirements
------------

None, other than installing the role itself. To do that, create a `requirements.yml` file next to your playbook with
the following contents:

     - name: raspi-config
       src: https://github.com/mikolak-net/ansible-raspi-config

and then run:

    ansible-galaxy install -r requirements.yml
    
The role and its dependencies should be now installed and ready to reference in your playbook via the name given
in the requirements file.    

Role Variables
--------------

All user variables reside in `defaults/main.yml`. Currently the following are available:
 
    # perform full update+upgrade
    raspi_config_update_packages: yes
    # have the FS fill the SD card
    raspi_config_expanded_filesystem: yes
    # how much memory should be owned by the GPU (vs RAM)
    raspi_config_memory_split_gpu: 16
    #currently sets Pi2 OC setting if applicable
    raspi_config_ensure_optimal_cpu_params: yes
    # set global locale
    raspi_config_locale: en_US.UTF8
    # set timezone
    raspi_config_timezone: UTC
    # set hostname
    raspi_config_hostname: pi
    # ensure camera support is on - CURRENTLY UNVERIFIED
    raspi_config_enable_camera: no
    # specify whether to fail deployment when user/password is default
    raspi_config_fail_on_auth_test: yes
    # use this to add any additional options to the config in raw form
    raspi_config_other_options: {}


Dependencies
------------

See `dependencies` in `meta/main.yml`.

Example Playbook
----------------

    - hosts: pi*
      roles:
         - { role: raspi-config }

License
-------

BSD

Author Information
------------------

Issues should be reported on the [project page](https://github.com/mikolak-net/ansible-raspi-config).