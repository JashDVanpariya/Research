#!/bin/bash

echo "Switching to GKE context and deploying..."
kubectl config use-context gke_gold-circlet-439215-k9_europe-west1-b_expense-app-cluster
kubectl apply -f deployment_gke.yaml

echo "Switching to EKS context and deploying..."
kubectl config use-context iam-root-account@expense-app-cluster.eu-west-1.eksctl.io
kubectl apply -f deployment_eks.yaml

echo "Deployments completed on both GKE and EKS."


