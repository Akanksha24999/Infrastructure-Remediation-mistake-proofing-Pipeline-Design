# ==============================================================================
# HabotConnect Staging Environment - Main Terraform Configuration
# ==============================================================================
# Position: Junior Cloud & DevOps Engineer (GCP / Django / React)
# Purpose: Defines required providers and GCP project bindings for staging.
# ==============================================================================

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}
