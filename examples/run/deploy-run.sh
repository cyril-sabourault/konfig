#!/usr/bin/env bash
set -e

# Example deploy
CLUSTER_ID=$(gcloud container clusters describe k0 \
  --zone europe-west1-b \
  --format='value(selfLink)')
CLUSTER_ID=${CLUSTER_ID#"https://container.googleapis.com/v1"}

# Deploy to RUN
gcloud alpha run deploy konfig \
  --allow-unauthenticated \
  --concurrency 50 \
  --image eu.gcr.io/$(GOOGLE_CLOUD_PROJECT)/konfig \
  --memory 2G \
  --region us-central1 \
  --set-env-vars "FOO=\$SecretKeyRef:${CLUSTER_ID}/namespaces/default/secrets/env/keys/foo,ENVIRONMENT=\$ConfigMapKeyRef:${CLUSTER_ID}/namespaces/default/configmaps/env/keys/environment"