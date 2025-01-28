def test_systemd_service_exists(host):
    """Verify that the systemd service file exists."""
    service_file = host.file("/etc/systemd/system/test-service.service")
    assert service_file.exists, "The systemd service file does not exist."
    assert service_file.is_file, "The systemd service file is not a regular file."


def test_systemd_service_properties(host):
    """Verify the systemd service properties match the role configuration."""
    service_content = host.file("/etc/systemd/system/test-service.service").content_string

    # Verify key systemd properties
    assert "ExecStart=/usr/bin/prometheus --config.file=/test/mnt/etc/prometheus/prometheus.yml" in service_content, "ExecStart is not correctly set."
    assert "User=root" in service_content, "The service user is not correctly set to root."
    assert "CPUQuota=50%" in service_content, "CPUQuota is not correctly set."
    assert "MemoryHigh=512M" in service_content, "MemoryHigh is not correctly set."
    assert "Restart=on-failure" in service_content, "Restart policy is not correctly set."


def test_systemd_service_status(host):
    """Verify the systemd service is active and enabled."""
    service = host.service("test-service")
    assert service.is_running, "The systemd service is not running."
    assert service.is_enabled, "The systemd service is not enabled."

def test_systemd_service_environment_variables(host):
    """Verify environment variables set in the systemd service file."""
    service_content = host.file("/etc/systemd/system/test-service.service").content_string

    # Verify environment directive
    assert "Environment=" in service_content, "Environment variables are not set in the service file."
    assert "PROMETHEUS_STORAGE_PATH=/prometheus" in service_content, "Expected environment variable is missing."

def test_systemd_service_config_files(host):
    """Verify the service configuration files exist with required settings."""
    config_file = host.file("/test/mnt/etc/prometheus/prometheus.yml")
    assert config_file.exists, "The Prometheus configuration file does not exist."

    config_content = config_file.content_string.strip()

    # Verify key settings are present in the configuration file
    assert "global:" in config_content, "The 'global' section is missing in the configuration file."
    assert "scrape_interval: 15s" in config_content, "The 'scrape_interval' setting is missing or incorrect."
    assert "evaluation_interval: 15s" in config_content, "The 'evaluation_interval' setting is missing or incorrect."
    assert "scrape_configs:" in config_content, "The 'scrape_configs' section is missing in the configuration file."
    assert "- job_name: prometheus" in config_content, "The 'prometheus' job is missing in the scrape_configs section."
    assert 'targets: ["localhost:9090"]' in config_content, "The target 'localhost:9090' is missing in the scrape_configs section."

def test_binary_file_exists_and_executable(host):
    """Verify that the service binary exists and is executable."""
    binary = host.file("/usr/bin/prometheus")
    assert binary.exists, "The service binary does not exist."
    assert binary.is_file, "The service binary is not a regular file."
    assert binary.mode & 0o111, "The service binary is not executable."


def test_data_directory_exists(host):
    """Verify the data directory exists with correct permissions."""
    data_dir = host.file("/var/tmp/prometheus")
    assert data_dir.exists, "The data directory does not exist."
    assert data_dir.is_directory, "The data directory is not a directory."
    assert data_dir.user == "root", "The data directory is not owned by root."
    assert data_dir.group == "root", "The data directory group is not root."


def test_service_logs_no_errors(host):
    """Verify that the systemd service logs contain no errors."""
    logs = host.run("journalctl -u test-service --no-pager --since '1 hour ago'")
    assert logs.rc == 0, "Failed to fetch systemd logs for the service."
    assert "error" not in logs.stdout.lower(), "Systemd logs contain errors."
    assert "failed" not in logs.stdout.lower(), "Systemd logs indicate failure."

def test_iptables_prometheus_port(host):
    """Verify that the ingress ports are allowed in iptables."""
    # Check if the iptables rule for port 9090 exists
    iptables_output = host.run("iptables -L INPUT -v -n")
    assert iptables_output.rc == 0, "Failed to list iptables rules."

    # Verify that the rule allowing TCP traffic on port 9090 exists
    assert "9090" in iptables_output.stdout, "The iptables rule for port 9090 is missing."
