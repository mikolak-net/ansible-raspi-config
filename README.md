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

```yaml
- name: mikolak.raspi-config
```

and then run:

    ansible-galaxy install -r requirements.yml

The role and its dependencies should be now installed and ready to reference in your playbook via the name given
in the requirements file.    

_Note:_ you can also install the role directly:

    ansible-galaxy install mikolak.raspi-config
    
but creating a requirements file is just good practice.

Role Variables
--------------

All user variables reside in `defaults/main.yml`. Currently the following are available:
 
```yaml
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
# ignored if "raspi_config_replace_user" is set (warning will still display)
raspi_config_fail_on_auth_test: yes
# user to replace the default "pi" user with
# NOTE: if you use this for the first time as "pi", any post_tasks will fail!
raspi_config_replace_user:
  name:
  path_to_ssh_key: #LOCAL path to your public key file
# use this to add any additional options to the config in raw form
raspi_config_other_options: {}
```


Dependencies
------------

See `dependencies` in `meta/main.yml`.

Example Playbook
----------------

```yaml
- hosts: pi*
  remote_user: pi
  sudo: true
  roles:
     - role: mikolak.raspi-config
       raspi_config_replace_user:
         name: mainuser
         path_to_ssh_key: "~/.ssh/my_pub_key_id_rsa.pub"
```

License
-------

BSD

Author Information
------------------

Issues should be reported on the [project page](https://github.com/mikolak-net/ansible-raspi-config).