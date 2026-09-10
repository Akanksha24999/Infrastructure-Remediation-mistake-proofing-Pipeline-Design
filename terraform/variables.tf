# ==============================================================================
# Terraform Input Variables Definition
# ==============================================================================

variable "gcp_project_id" {
  type        = string
  description = "The Google Cloud Platform project ID where resources will be provisioned."
  default     = "habot-staging-project"
}

variable "gcp_region" {
  type        = string
  description = "Primary GCP region for storage and analytics resources."
  default     = "us-central1"
}

variable "gcp_zone" {
  type        = string
  description = "Primary GCP availability zone."
  default     = "us-central1-a"
}

variable "environment" {
  type        = string
  description = "Deployment environment name."
  default     = "staging"
}

variable "data_retention_days" {
  type        = number
  description = "Number of days before raw landing objects are auto-purged or archived."
  default     = 90
}
