def test_container_running(host):
    container = host.docker("full-container")
    assert container.is_running

def test_container_exposes_ports(host):
    socket = host.socket("tcp://0.0.0.0:9090")
    assert socket.is_listening

def test_container_user_is_root(host):
    container = host.docker("full-container")
    user = container.inspect()["Config"]["User"]

    assert user == "root", f"Container user is not 'root', it is '{user}'."

def test_container_creates_hostdirectory(host):
    directory = host.file("/test/mnt")
    assert directory.is_directory, "The directory /test/mnt does not exist."

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

def test_container_cpus_and_memory(host):
    container = host.docker("full-container")
    host_config = container.inspect()["HostConfig"]

    # Extract CPU and memory limits from HostConfig
    nano_cpus = host_config["NanoCpus"]
    memory = host_config["Memory"]

    # Convert NanoCpus to CPUs (divide by 1e9) and memory from bytes to MB (divide by 1024^2)
    cpus = nano_cpus / 1e9
    memory_mb = memory / (1024 * 1024)

    assert cpus == 2, f"Container CPUs are not set to 2, they are set to {cpus}."
    assert memory_mb == 1024, f"Container memory is not set to 1024M, it is set to {memory_mb}M."

def test_container_restart_policy(host):
    container = host.docker("full-container")
    restart_policy = container.inspect().get("HostConfig", {}).get("RestartPolicy", {}).get("Name", "")
    assert restart_policy == "always", f"Container restart policy is not 'always', it is '{restart_policy}'."
