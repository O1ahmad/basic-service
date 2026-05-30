def test_binary_exists(host):
    binary = host.file("/usr/local/bin/jq-tool")
    assert binary.exists
    assert binary.mode == 0o755


def test_service_not_exists(host):
    unit_file = host.file("/etc/systemd/system/test-tool.service")
    assert not unit_file.exists

    # systemctl is-enabled exits 4 when the unit is missing
    status = host.run("systemctl is-enabled test-tool")
    assert status.rc != 0
    assert "not-found" in status.stdout or status.rc == 4
