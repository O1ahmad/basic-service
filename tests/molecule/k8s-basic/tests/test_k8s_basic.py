import json

NAMESPACE = "molecule-k8s"
RELEASE = "test-k8s-service"
DEPLOYMENT = f"{RELEASE}-deployment"
SERVICE = f"{RELEASE}-svc"


def test_namespace_exists(host):
    result = host.run(f"kubectl get namespace {NAMESPACE}")
    assert result.rc == 0, f"Namespace missing: {result.stderr}"


def test_helm_release_is_deployed(host):
    result = host.run(f"helm list -n {NAMESPACE} -o json")
    assert result.rc == 0, f"helm list failed: {result.stderr}"
    releases = json.loads(result.stdout)
    assert any(item.get("name") == RELEASE for item in releases), "Helm release was not deployed."


def test_deployment_is_ready(host):
    result = host.run(
        f"kubectl -n {NAMESPACE} rollout status deploy/{DEPLOYMENT} --timeout=180s"
    )
    assert result.rc == 0, f"Deployment not ready: {result.stderr}"


def test_service_has_endpoints(host):
    result = host.run(
        f"kubectl -n {NAMESPACE} get endpoints {SERVICE} "
        "-o jsonpath='{.subsets[0].addresses[0].ip}'"
    )
    assert result.rc == 0, f"Service endpoints lookup failed: {result.stderr}"
    assert result.stdout.strip(), "Service has no ready endpoints."


def test_service_responds_in_cluster(host):
    run_pod = host.run(
        f"kubectl -n {NAMESPACE} run curl-test "
        "--image=curlimages/curl:8.5.0 --restart=Never "
        "--command -- sleep 3600"
    )
    assert run_pod.rc == 0, f"Failed to start curl test pod: {run_pod.stderr}"

    wait_pod = host.run(
        f"kubectl -n {NAMESPACE} wait --for=condition=ready pod/curl-test --timeout=120s"
    )
    assert wait_pod.rc == 0, f"curl test pod not ready: {wait_pod.stderr}"

    curl = host.run(
        f"kubectl -n {NAMESPACE} exec curl-test -- curl -sf http://{SERVICE}/"
    )
    assert curl.rc == 0, f"In-cluster service request failed: {curl.stderr}"
    assert "Welcome to nginx" in curl.stdout, "Service did not return the nginx welcome page."

    host.run(f"kubectl -n {NAMESPACE} delete pod curl-test --wait=true")
