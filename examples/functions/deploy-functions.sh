#!/usr/bin/env bash
set -e

# Example deploy
GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
CLUSTER_ID=$(gcloud container clusters describe k0 \
  --project $GOOGLE_CLOUD_PROJECT \
  --zone europe-west1-b \
  --format='value(selfLink)')
CLUSTER_ID=${CLUSTER_ID#"https://container.googleapis.com/v1"}

# Deploy to FUNCTIONS
gcloud functions deploy konfig \
  --runtime python37 \
  --entry-point konfig \
  --trigger-http \
  --project $GOOGLE_CLOUD_PROJECT \
  --region europe-west1 \
  --set-env-vars "FOO=\$SecretKeyRef:${CLUSTER_ID}/namespaces/default/secrets/env/keys/foo,ENVIRONMENT=\$ConfigMapKeyRef:${CLUSTER_ID}/namespaces/default/configmaps/env/keys/environment"