def test_container_running(host):
    container = host.docker("jq-container")
    assert container.is_running
    status = container.inspect()["State"]["Status"]
    assert status == "running", f"Container status is '{status}', expected 'running'."


def test_binary_downloaded_on_host(host):
    binary = host.file("/opt/binaries/jq-tool")
    assert binary.exists, "The service binary does not exist on the host."
    assert binary.is_file, "The service binary is not a regular file."
    assert binary.mode & 0o111, "The service binary is not executable."


def test_binary_mounted_in_container(host):
    container = host.docker("jq-container")
    mounts = container.inspect()["Mounts"]
    binary_mounts = [m for m in mounts if m.get("Destination") == "/opt/binaries"]
    assert len(binary_mounts) == 1, "Binary directory is not mounted in the container."
    assert binary_mounts[0]["Source"] == "/opt/binaries"


def test_binary_executes_in_container(host):
    result = host.run("docker exec jq-container /opt/binaries/jq-tool --version")
    assert result.rc == 0, f"jq failed to execute: {result.stderr}"
    assert "jq-" in result.stdout, "jq version output was unexpected."
