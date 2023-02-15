# Basic Service Chart

Helm chart that supports a basic, cloud-native containerized app in Kubernetes.

## Values

| Name | Description | Type | Default | Required |
|------|-------------|:------:|:---------:|:--------:|
| name | The service name | `string` | `` | yes |
| clusterName | Name of Kubernetes cluster to deploy to | `string` | `` | yes |
| namespace | Namespace within Kubernetes cluster to deploy | `string` | `` | yes |
| createNamespace | Whether to create the cluster namespace if it does not exist | `string` | `` | yes |
| image | Container image of service release | `string` | `` | yes |
| common_name | Service common DNS name for which traffic external to the cluster should be sent to | `string` (max 64 characters) | `` | yes |
| command | Container command/entrypoint override of service's base Docker image ENTRYPOINT | `list(string)` | `[]` | no |
| args | Arguments to the command/entrypoint override | `list(string)` | `[]` | no |
| serviceAccountName | k8s service account/policy to associate with service | `string` (use value `default` if no service account required) | `` | no |
| serviceType | Type of k8s service object to provision (i.e. ClusterIP, NodePort, LoadBalancer, ExternalName) | `string` | `` | no |
| servicePort | Port incoming service traffic is directed to and mapped to `serviceTargetPort` | `string` | `` | no |
| serviceTargetPort | Port service is listening on inside the container | `string` | `` | no |
| healthCheckEndpoint | Path of service healthcheck endpoint | `string` | `` | no |
| extraCommonNames | Additional service common DNS names for which traffic external to the cluster should be sent to | `string` (max 64 characters) | `` | no |
| grpcCommonName | Service gRPC common DNS name for which traffic external to the cluster should be sent to | `string` (max 64 characters) | `` | no |
| minReplicas | Lower limit for the number of replicas to which the autoscaler can scale down | `int` | `1` | no |
| maxReplicas | Upper limit for the number of replicas to which the autoscaler can scale up | `int` | `3` | no |
| env.config | Set of environment variables to inject into the service's container runtime | `dict` | `{}` | no |
| initContainers | Container definitions to execute during service initialization | `dict` | `{}` | no |
| extraContainers | Additional container definitions to include with service deployments |`dict` | `{}` | no |
| configMaps | ConfigMap definitions to include with service deployments | `dict` | `{}` | no |
| base64DecodedSecretVolumes | List of base 64 decoded secrets to mount | `list(object)` | `[]` | no |
| extraVolumes | Additional volume definitions to include within service deployments | `dict` | `{}` | no |
| extraVolumeMounts | Additional volumeMount definitions to attach to service containers | `dict` | `{}` | no |
| volumesFromConfigMaps | Additional volumes to provision based on defined configMaps | `dict` | `{}` | no |
| labels | Collection of metadata labels to assign to service deployments | `dict` | `{}` | no |
| annotations | Collection of metadata annotations to assign to service deployments | `dict` | `{}` | no |
| grpcServicePort | Port of incoming GRPC traffic | `string` | `` | no |
| grpcServiceTargetPort | gRPC port service is listening on inside the container | `string` | `` | no |
| ingressRoutes | additional Istio ingress routes handled by the service  | `dict` | `{}` | no |
| externalRoutes | Istio external routes for inter-cluster service communication | `dict` | `{}` | no |
| serviceRoles | RBAC policies and associated service account bindings | `dict` | `{}` | no |
| includePodName | Provides the name of the pod as "POD_NAME" env variable | `bool` | `false` | no |
| deployStatefulSet | Whether to deploy a service as a k8s StatefulSet or standard Deployment workload | `bool` | `false` | no |
| statefulSetOptions | volume claim and other options associated with StatefulSet deployments | `dict` | `{}` | no |
| deployStrategy | The deployment strategy to use to replace existing pods with new ones  | `dict` | `{}` | no |
| persistentVolumeClaim | persistent volume claim that will be mounted to deployment  | `list(object)` | `[]` | no |
| persistentVolume | persistent volume that the pvc can use   | `list(object)` | `[]` | no |
| storageClass | storage class that the pvc can use   | `list(object)` | `[]` | no |
| dockercfgOverride | Docker config secret override reference (not including `-docker` suffix) | `string` | `` | no |
| tlsMode | configures the [TLS mode](https://istio.io/latest/docs/reference/config/networking/gateway/#ServerTLSSettings-TLSmode) on the Gateway | `string` | `MUTUAL` | no |
| keystoreServicePathOverride | overrides the path to the keystore secret stored in SecretsManager for services that have dynamic names but same secret | `string` | `` | no |
