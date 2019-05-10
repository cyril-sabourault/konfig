#!/usr/bin/env bash
set -e

# Example deploy
GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
CLUSTER_ID=$(gcloud container clusters describe k0 \
  --project $GOOGLE_CLOUD_PROJECT \
  --zone europe-west1-b \
  --format='value(selfLink)')
CLUSTER_ID=${CLUSTER_ID#"https://container.googleapis.com/v1"}

# Submit build to Cloud Build
gcloud builds submit . \
  --tag eu.gcr.io/$GOOGLE_CLOUD_PROJECT/konfig

# Deploy to RUN
gcloud beta run deploy konfig \
  --allow-unauthenticated \
  --image eu.gcr.io/$GOOGLE_CLOUD_PROJECT/konfig \
  --region us-central1 \
  --set-env-vars "FOO=\$SecretKeyRef:${CLUSTER_ID}/namespaces/default/secrets/env/keys/foo,ENVIRONMENT=\$ConfigMapKeyRef:${CLUSTER_ID}/namespaces/default/configmaps/env/keys/environment"