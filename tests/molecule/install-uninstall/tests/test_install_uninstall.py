def test_binary_does_not_exist(host):
    binary = host.file("/usr/local/bin/tool-to-remove")
    assert not binary.exists
