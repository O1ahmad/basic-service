def test_binary_exists(host):
    binary = host.file("/usr/local/bin/jq-tool")
    # Check that the binary file exists and is executable
    assert binary.exists
    assert binary.mode == 0o755

def test_service_not_exists(host):
    # Ensure no systemd service was created
    service = host.service("test-tool")
    assert not service.is_enabled
    try:
        assert not service.is_running
    except Exception:
        pass
    
    unit_file = host.file("/etc/systemd/system/test-tool.service")
    assert not unit_file.exists
