<!-- @format -->

<p><img src="https://code.benco.io/icon-collection/logos/ansible.svg" alt="ansible logo" title="ansible" align="left" height="60" /></p>

# Basic-Service
[![Galaxy Role](https://img.shields.io/ansible/role/61415.svg)](https://galaxy.ansible.com/0x0I/basic_service)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/0x0I/basic-service?color=yellow)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Configure and operate a basic cloud-native service: running anything from cypto blockchain clients to the immense app store of open-source ([Apache](https://projects.apache.org/projects.html), [CNCF](https://landscape.cncf.io/card-mode?project=hosted&grouping=no) and beyond) services.

## Requirements

[Docker SDK](https://docker-py.readthedocs.io/en/stable/) for Python (for Python 2.6 support, use the deprecated `docker-py` library instead) or installation of the `docker` engine.

## vars

|       var       |                        description                         |     default      |
| :-------------: | :--------------------------------------------------------: | :--------------: |
|   _setupMode_   |  infrastructure provisioning setup mode (`container, helm, systemd`)  |   `container`    |
|     _name_      |                 name of service to deploy                  |    **required**    |
|     _image_     |             service container image to deploy              |    **required**    |
|     _command_     |             Command and arguments to execute on startup              |    **required**    |
|     _user_     |             service container image to deploy              |    `root`    |
|    _config_     |  configuration files associated with the service to mount  |       `{}`       |
|   _configEnv_   |  environment variables to set within the service runtime   |       `{}`       |
|     _ports_     |          listening port information for a service          |       `{}`       |
|     _setup_iptables_     |          configure IP tables to allow ingress paths          |       `false`       |
|  _hostDataDir_  |   host directory to store node runtime/operational data    |    `/var/tmp`    |
|    _dataDir_    | container directory to store node runtime/operational data |      `/tmp`      |
|    _workDir_    |      operational directory to store runtime artifacts      |    `/var/tmp`    |
| _restartPolicy_ |                  container restart policy                  | `unless-stopped` |
|   _systemd_   |    Systemd deployment custom unit, service and install properties    |     `{}`      |
|     _cpus_      |  available CPU resources each deployed service can use   |      `1.0`       |
|    _memory_     | available memory resources each deployed service can use |       `4g`       |
|   _uninstall_   |    whether to remove installed service and artifacts    |     `false`      |

## Containerized Apps
- [O1 Containers](https://github.com/0x0I/containers)
- [Dockerhub](https://hub.docker.com/search?q=)
- [Quay.io](https://quay.io/search)

## Dependencies

```
collections:
- name: community.docker
```

## Example Playbook

```
- hosts: servers
  roles:
```

- Launch a container that sleeps for infinity:

```
  - role: o1labs.basic-service
    vars:
      name: sleepy-service
      image: busybox:latest
      command: ["sleep", "infinity"]
```

## License

MIT

## Author Information

This Ansible role was created in 2023 by O1.IO.

🏆 **always happy to help & donations are always welcome** 💸

- **ETH (Ethereum):** 0x652eD9d222eeA1Ad843efec01E60C29bF2CF6E4c

- **BTC (Bitcoin):** 3E8gMxwEnfAAWbvjoPVqSz6DvPfwQ1q8Jn

- **ATOM (Cosmos):** cosmos19vmcf5t68w6ug45mrwjyauh4ey99u9htrgqv09
