import time

SERVICE_CONTAINER = "binary-service-container"
SERVICE_PORT = 9090
BINARY_STAGING_DIR = "/tmp/molecule-service-binary"
READINESS_CMD = (
    "python3 -c \"import urllib.request; "
    f"urllib.request.urlopen('http://127.0.0.1:{SERVICE_PORT}/-/ready')\""
)


def test_long_running_service_container_is_running(host):
    container = host.docker(SERVICE_CONTAINER)
    assert container.is_running


def test_service_binary_staged_on_host(host):
    binary = host.file(f"{BINARY_STAGING_DIR}/prometheus")
    assert binary.exists, "Service binary was not downloaded to the host staging directory."
    assert binary.mode == 0o755, "Service binary is not executable."


def test_service_config_is_mounted(host):
    container = host.get_host(f"docker://{SERVICE_CONTAINER}")
    config_file = container.file("/etc/prometheus/prometheus.yml")
    assert config_file.exists, "Service configuration file is missing in the container."


def test_service_data_directory_is_mounted(host):
    container = host.get_host(f"docker://{SERVICE_CONTAINER}")
    result = container.run("test -d /prometheus")
    assert result.rc == 0, "Service data directory is not mounted in the container."


def test_service_publishes_port(host):
    socket = host.socket(f"tcp://0.0.0.0:{SERVICE_PORT}")
    assert socket.is_listening


def test_service_readiness_endpoint(host):
    for _ in range(30):
        result = host.run(READINESS_CMD)
        if result.rc == 0:
            return
        time.sleep(1)
    assert False, f"Service readiness check failed: {result.stderr}"


def test_service_container_restart_policy(host):
    container = host.docker(SERVICE_CONTAINER)
    restart_policy = container.inspect().get("HostConfig", {}).get("RestartPolicy", {}).get("Name", "")
    assert restart_policy == "on-failure", (
        f"Container restart policy is not 'on-failure', it is '{restart_policy}'."
    )
