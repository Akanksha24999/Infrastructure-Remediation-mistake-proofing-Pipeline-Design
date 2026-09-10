# ==============================================================================
# Task 1: GCS Raw Landing Bucket Provisioning (D0 Raw Landing)
# ==============================================================================
# AWS Equivalent: S3 Bucket with Default Encryption, Versioning, and Bucket Policy
# ==============================================================================

# Random suffix to guarantee global bucket name uniqueness across GCP
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "d0_raw_landing" {
  name          = "habot-${var.environment}-d0-raw-landing-${random_id.bucket_suffix.hex}"
  location      = var.gcp_region
  force_destroy = false # Prevent accidental deletion of raw student data
  storage_class = "STANDARD"

  # Security Control 1: Enforce Uniform Bucket-Level Access (No public ACLs)
  uniform_bucket_level_access = true

  # Security Control 2: Object Versioning for auditability & data recovery
  versioning {
    enabled = true
  }

  # Lifecycle rule: Automatically transition raw logs to Coldline storage after 30 days
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }

  # Lifecycle rule: Auto-purge raw landing files after retention threshold
  lifecycle_rule {
    condition {
      age = var.data_retention_days
    }
    action {
      type = "Delete"
    }
  }

  labels = {
    environment = var.environment
    layer       = "d0_raw_landing"
    managed_by  = "terraform"
    owner       = "cloud_devops_team"
  }
}

data "google_project" "current" {}
