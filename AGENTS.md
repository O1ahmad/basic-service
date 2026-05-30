# AGENTS.md

## Overview

Ansible Galaxy role **`basic_service`** (playbooks reference it as `basic-service`) plus a Helm chart. No long-running app—development is **lint** and **Molecule** tests (`.github/workflows/CI.yaml`).

## Shell environment

```bash
export PATH="$HOME/.local/bin:$PATH"
```

The session update script (`SetupVmEnvironment`) refreshes Python tooling only; it does not install Docker or run tests.

## One-time VM setup

Required on a fresh Cloud Agent VM (not repeated each session):

1. **Docker** — Docker CE with `fuse-overlayfs` and `iptables-legacy`. Keep `dockerd` running (e.g. tmux session `dockerd-server`). If the daemon dies with zombie `[dockerd]` processes, clear stale `/var/run/docker*` and run `sudo /usr/bin/dockerd`.
2. **Socket access** — `sudo chmod 666 /var/run/docker.sock` (or add the agent user to the `docker` group in a new shell).
3. **Role symlink** — Molecule sets `ANSIBLE_ROLES_PATH` to `../../../../` (filesystem root when the repo is `/workspace`). Run `sudo ln -sfn /workspace /basic-service` so `role: basic-service` resolves.
4. **rsync** — `sudo apt-get install -y rsync` (Molecule Docker driver).
5. **Root pip deps** — `community.docker` under `become` needs root Python packages:  
   `sudo pip install --break-system-packages 'requests==2.31.0' 'urllib3<2' 'docker>=6,<7'`

## Lint

From repo root:

```bash
yamllint --config-file ./tests/yaml-lint.yml .
ansible-lint --config-file ./tests/ansible-lint.yml .
```

## Molecule tests

From `tests/`:

```bash
cd tests
molecule test -s container-basic   # or any scenario name below
```

**CI scenarios:** `systemd-basic`, `systemd-full`, `systemd-uninstall`, `container-basic`, `container-full`, `container-uninstall`, `install-basic`, `install-uninstall`.

### Cloud VM caveats

- **Container scenarios** use `docker:24.0.5-dind` with the host socket. Nested containers on cgroup v2 may need host cgroup namespace (`docker run --cgroupns=host` or `cgroupns_mode: host` in playbooks). GHA `ubuntu-latest` usually avoids this; Cloud VMs often do not.
- **Systemd / install scenarios** use a privileged instance with `/sys/fs/cgroup` and `cgroupns_mode: host` in `molecule.yml`. If `instance` exits immediately, check `docker logs instance` and daemon health.
- **Inside `instance`**, Docker API failures may need:  
  `docker exec instance pip3 install --break-system-packages 'requests==2.31.0' 'urllib3<2' 'docker>=6,<7'`  
  and `ansible-galaxy collection install community.docker`.

### Quick validation (host Docker)

With Docker running and `/basic-service` symlinked:

```bash
ansible -m community.docker.docker_container \
  -a "name=nginx-hello image=nginx:latest state=started published_ports=8080:80 cgroupns_mode=host" \
  localhost -become
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/
```

Exercises the same stack as `setup_mode: container` (the role does not set `cgroupns_mode`; full Molecule runs may still need cgroup workarounds above).

## Kubernetes / Helm

`setup_mode: k8s` is not in CI. Requires a cluster, `KUBECONFIG`, `KUBE_CONTEXT`, Helm, and `kubernetes.core` (see `README.md`, `helm/README.md`).
