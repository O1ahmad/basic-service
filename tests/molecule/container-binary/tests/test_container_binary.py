def test_container_running(host):
    container = host.docker("jq-container")
    assert container.is_running


def test_binary_downloaded_on_host(host):
    binary = host.file("/usr/local/bin/jq-tool")
    assert binary.exists, "The service binary does not exist on the host."
    assert binary.is_file, "The service binary is not a regular file."
    assert binary.mode & 0o111, "The service binary is not executable."


def test_binary_mounted_in_container(host):
    container = host.get_host("docker://jq-container")
    binary = container.file("/usr/local/bin/jq-tool")
    assert binary.exists, "The service binary is not mounted in the container."
    assert binary.mode & 0o111, "The mounted binary is not executable."


def test_binary_executes_in_container(host):
    container = host.get_host("docker://jq-container")
    result = container.run("/usr/local/bin/jq-tool --version")
    assert result.rc == 0, f"jq failed to execute: {result.stderr}"
    assert "jq-" in result.stdout, "jq version output was unexpected."
