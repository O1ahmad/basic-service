def test_container_running(host):
    container = host.docker("nginx-container")
    assert container.is_running

def test_container_user_is_root(host):
    """Verify that the container always runs as root."""
    container = host.docker("nginx-container")
    user = container.inspect()["Config"]["User"]
    assert user == "root", f"Container user is not 'root', it is '{user}'."

def test_container_exposes_ports(host):
    socket = host.socket("tcp://0.0.0.0:8080")
    assert socket.is_listening
