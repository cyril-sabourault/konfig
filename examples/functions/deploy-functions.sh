#!/usr/bin/env bash
set -e

# Example deploy
CLUSTER_ID=$(gcloud container clusters describe k0 \
  --zone europe-west1-b \
  --format='value(selfLink)')
CLUSTER_ID=${CLUSTER_ID#"https://container.googleapis.com/v1"}

# Deploy to FUNCTIONS
gcloud functions deploy konfig \
  --runtime python37 \
  --entry-point konfig \
  --trigger-http \
  --region europe-west1 \
  --set-env-vars "FOO=\$SecretKeyRef:${CLUSTER_ID}/namespaces/default/secrets/env/keys/foo,ENVIRONMENT=\$ConfigMapKeyRef:${CLUSTER_ID}/namespaces/default/configmaps/env/keys/environment"