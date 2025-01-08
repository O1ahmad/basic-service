def test_container_running(host):
    container = host.docker("full-container")
    assert container.is_running

def test_container_exposes_ports(host):
    socket = host.socket("tcp://0.0.0.0:9090")
    assert socket.is_listening

def test_container_creates_configs(host):
    container = host.get_host("docker://full-container")

    file_path = "/etc/prometheus/prometheus.yml"
    file = container.file(file_path)
    assert file.exists, f"The file {file_path} does not exist."

def test_container_creates_datadirs(host):
    container = host.get_host("docker://full-container")
    
    datadir_exists = container.run("ls -l /prometheus")
    assert datadir_exists.rc == 0, f"The data dir does not exist: {datadir_exists.stdout}"

def test_container_env_setup(host):
    container = host.get_host("docker://full-container")
    
    envvar_exists = container.run("env | grep PROMETHEUS_STORAGE_PATH")
    assert envvar_exists.rc == 0, f"The test environment variable does not exist: {envvar_exists.stdout}"
