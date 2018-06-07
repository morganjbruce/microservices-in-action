Listing 8.1 Creating a GCE project

```
gcloud projects create <project-id> --set-as-default --enable-cloud-apis
```

Listing 8.2 Creating a virtual machine

```
gcloud compute instances create market-data-service \
  --image-family=debian-9 \
  --image-project=debian-cloud \
  --machine-type=g1-small \
  --scopes userinfo-email,cloud-platform \
  --metadata-from-file startup-script=startup-script.sh \
  --tags api-service \
  --zone=europe-west1-b
```
Listing 8.3 Tailing startup script progress

```
gcloud compute instances tail-serial-port-output market-data-service
```

Listing 8.4 Opening firewall access to our new VM

```
gcloud compute firewall-rules create default-allow-http-8080 \
  --allow tcp:8080 \
  --source-ranges 0.0.0.0/0 \
  --target-tags api-service \
  --description "Allow port 8080 access to api-service"
```

Listing 8.6 Creating an instance template

```
gcloud compute instance-templates create market-data-service-template \
  --machine-type g1-small \
  --image-family debian-9 \
  --image-project debian-cloud \
  --metadata-from-file startup-script=startup-script.sh \
  --tags api-service \
  --scopes userinfo-email,cloud-platform
```

Listing 8.7 Creating an instance group

```
gcloud compute instance-groups managed create market-data-service-group \
  --base-instance-name market-data-service \
  --size 3 \
  --template market-data-service-template \
  --region europe-west1
```

Listing 8.8 Adding a health check that targets our service

```
gcloud compute health-checks create http api-health-check \
  --port=8080 \
  --request-path="/ping"

gcloud beta compute instance-groups managed set-autohealing \
  market-data-service-group \
  --region=europe-west1 \
  --http-health-check=api-health-check
```

Listing 8.9 Adjusting the size of an instance group

```
gcloud compute instance-groups managed resize market-data-service-group \
--size=6 \
--region=europe-west1
```

Listing 8.10 Adding a backend service

```
gcloud compute instance-groups managed set-named-ports \
  market-data-service-group \
  --named-ports http:8080 \
  --region europe-west1

gcloud compute backend-services create market-data-service \
  --protocol HTTP \
  --health-checks api-health-check \
  --global
```

Listing 8.11 Adding a map and a proxy

```
gcloud compute url-maps create api-map \
  --default-service market-data-service

gcloud compute target-http-proxies create api-proxy \
  --url-map api-map
```

Listing 8.12 Adding a static IP address

```
gcloud compute addresses create market-data-service-ip \
  --ip-version=IPV4 \
  --global

export IP=`gcloud compute addresses describe market-data-service-ip --global --format json | jq --raw-output '.address'`

gcloud compute forwarding-rules create api-forwarding-rule \
  --address $IP \
  --global \
  --target-http-proxy api-proxy \
  --ports 80

printenv IP
```

Listing 8.13 instance-template.json

```
{
  "variables": {
    "commit": "{{env `COMMIT`}}"
  },
  "builders":
  [
    {
      "type": "googlecompute",
      "project_id": "market-data-1",
      "source_image_family": "debian-9",
      "zone": "europe-west1-b",
      "image_name": "market-data-service-{{user `commit`}}",
      "image_description": "image built for market-data-service {{user `commit`}}",
      "instance_name": "market-data-service-{{uuid}}",
      "machine_type": "n1-standard-1",
      "disk_type": "pd-ssd",
      "ssh_username": "debian",
      "startup_script_file": "startup-script.sh"
    }
  ]
}
```

Listing 8.14 packer build

```
packer build \
-var "commit=`git rev-parse head`" \
instance-template.json
```

Listing 8.15 Dockerfile for market-data service

```
FROM python:3.6
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "-c", "config.py", "app:app", "--bind", "0.0.0.0:8080"]
EXPOSE 8000
```

Listing 8.16 Building a Docker container

```
$ docker build -t market-data:`git rev-parse head` .
```

Listing 8.17 Running a Docker container

```
$ docker run -d -p 8080:8080 market-data:`git rev-parse head`
```

Listing 8.18 Using the GCE container registry

```
TAG="market-data:$(git rev-parse head)"
PROJECT_ID=<your-project-id>

docker tag $TAG eu.gcr.io/$PROJECT_ID/$TAG

gcloud docker -- push eu.gcr.io/$PROJECT_ID/$TAG
```

Listing 8.19 Start a new instance running a container

```
gcloud beta compute instances create-with-container \
  market-data-service-c \
  --container-image eu.gcr.io/$PROJECT_ID/$TAG
  --tags api-service
```

Listing 8.20 Create an instance template from a container

```
gcloud beta compute instance-templates create-with-container \
  market-data-service-template-2 \
  --container-image eu.gcr.io/$PROJECT_ID/$TAG
  --tags=api-service
```

Listing 8.21 Start a canary rollout

```
gcloud beta compute instance-groups managed rolling-action start-update \
  market-data-service-group \
  --version template=market-data-service-template \
  --canary-version template=market-data-service-template-2,target-size=1 \
  --region europe-west1
```

Listing 8.22 Continue rolling out the new version

```
gcloud beta compute instance-groups managed rolling-action start-update \
  market-data-service-group \
  --version template=market-data-service-template-2 \
  --region europe-west1
```

Listing 8.23 Rollback to the previous version

```
gcloud beta compute instance-groups managed rolling-action start-update \
  market-data-service-group \
  --version template=market-data-service-template \
  --region europe-west1
```
