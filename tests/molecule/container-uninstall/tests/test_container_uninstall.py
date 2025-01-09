def test_container_removed(host):
    """Verify the container has been removed."""
    container = host.run("docker ps -a --filter 'name=full-container' --format '{{.Names}}'")
    assert container.stdout.strip() == "", "The container 'full-container' still exists."

def test_config_directory_removed(host):
    """Verify the configuration directory has been removed."""
    config_dir = host.file("/test/mnt/etc/prometheus")
    assert not config_dir.exists, "The configuration directory still exists."

def test_data_directory_removed(host):
    """Verify the data directory has been removed."""
    data_dir = host.file("/tmp/prometheus")
    assert not data_dir.exists, "The data directory still exists."

def test_host_data_directory_removed(host):
    """Verify the host data directory has been removed."""
    host_data_dir = host.file("/test/mnt/prometheus")
    assert not host_data_dir.exists, "The host data directory still exists."
