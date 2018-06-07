#### Listing 8.1 Creating a GCE project

```sh
gcloud projects create <project-id> --set-as-default --enable-cloud-apis
```

#### Listing 8.2 Creating a virtual machine

```sh
gcloud compute instances create market-data-service \
  --image-family=debian-9 \
  --image-project=debian-cloud \
  --machine-type=g1-small \
  --scopes userinfo-email,cloud-platform \
  --metadata-from-file startup-script=startup-script.sh \
  --tags api-service \
  --zone=europe-west1-b
```
### Listing 8.3 Tailing startup script progress

```sh
gcloud compute instances tail-serial-port-output market-data-service
```
