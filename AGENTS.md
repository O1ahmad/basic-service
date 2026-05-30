# AGENTS.md

## Cursor Cloud specific instructions

This repository is the **Ansible Galaxy role `basic_service`** (plus a Helm chart). There is no long-running web app; development means **linting** and **Molecule integration tests** (see `.github/workflows/CI.yaml`).

### One-time VM setup (not in the update script)

These steps are required on a fresh Cloud Agent VM and are **not** repeated on every session:

1. **Docker Engine** — Install Docker CE with `fuse-overlayfs` storage driver and `iptables-legacy` (standard Cursor Cloud Docker-in-VM pattern). Ensure `dockerd` stays running; if the daemon exits leaving zombie `[dockerd]` processes, remove stale `/var/run/docker*` state and start `sudo /usr/bin/dockerd` in a dedicated tmux session (`dockerd-server`).
2. **Docker socket access** — `sudo chmod 666 /var/run/docker.sock` (or add the agent user to the `docker` group and use a new shell).
3. **Role path symlink** — Molecule sets `ANSIBLE_ROLES_PATH` to `../../../../` from each scenario, which resolves to `/` when the repo is checked out as `/workspace`. Create: `sudo ln -sfn /workspace /basic-service` so the role name `basic-service` resolves correctly.
4. **rsync** — `sudo apt-get install -y rsync` (Molecule Docker driver uses it during `create`).
5. **Root Python deps for `become`** — Ansible’s `community.docker` modules run under `sudo` and need compatible libraries in **root’s** Python:  
   `sudo pip install --break-system-packages 'requests==2.31.0' 'urllib3<2' 'docker>=6,<7'`  
   (Avoids `http+docker` / urllib3 v2 errors with the distro `community.docker` collection.)

### Update script (automatic on session start)

The VM update script only refreshes **Python tooling** (see `SetupVmEnvironment`). It does not start Docker or run tests.

### Lint

From repo root (matches CI):

```bash
export PATH="$HOME/.local/bin:$PATH"
yamllint --config-file ./tests/yaml-lint.yml .
ansible-lint --config-file ./tests/ansible-lint.yml .
```

### Tests (Molecule)

From `tests/`:

```bash
export PATH="$HOME/.local/bin:$PATH"
cd tests
molecule test -s container-basic   # or any CI scenario name
```

CI scenarios: `systemd-basic`, `systemd-full`, `systemd-uninstall`, `container-basic`, `container-full`, `container-uninstall`.

**Cloud VM caveats:**

- **Container scenarios** (`container-basic`, etc.) use `docker:24.0.5-dind` with the host Docker socket. Starting nested containers may fail with cgroup v2 “threaded mode” unless the daemon or containers use host cgroup namespace (`docker run --cgroupns=host`). GitHub Actions `ubuntu-latest` does not hit this; Cursor Cloud VMs often do.
- **Systemd scenarios** need a healthy privileged instance with `/sys/fs/cgroup` mounted (already in their `molecule.yml`). If the Molecule `instance` container exits immediately, check `docker logs instance` and Docker daemon stability.
- Inside the Molecule **instance** container, if converge fails on Docker API errors, install root pip deps there too: `docker exec instance pip3 install --break-system-packages 'requests==2.31.0' 'docker>=6,<7'` and `ansible-galaxy collection install community.docker`.

### Quick hello-world (container mode, host Docker)

With Docker running and the `/basic-service` symlink in place:

```bash
export PATH="$HOME/.local/bin:$PATH"
ansible -m community.docker.docker_container -a "name=nginx-hello image=nginx:latest state=started published_ports=8080:80 cgroupns_mode=host" localhost -become
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/
```

This exercises the same `community.docker` stack the role uses for `setup_mode: container` (the role itself does not set `cgroupns_mode`; full `molecule test` on Cloud VMs may still need the cgroup workarounds above).

### Kubernetes / Helm

`setup_mode: k8s` is **not** covered by CI. It requires a live cluster, `KUBECONFIG`, `KUBE_CONTEXT`, Helm, and `kubernetes.core` (see root `README.md` and `helm/README.md`).
