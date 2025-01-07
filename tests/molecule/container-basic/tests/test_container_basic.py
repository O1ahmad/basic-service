def test_container_running(host):
    container = host.docker("nginx-container")
    assert container.is_running

def test_container_exposes_ports(host):
    socket = host.socket("tcp://0.0.0.0:8080")
    assert socket.is_listening
