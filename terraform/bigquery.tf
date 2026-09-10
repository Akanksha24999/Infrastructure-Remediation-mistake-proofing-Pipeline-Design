# ==============================================================================
# Task 1: BigQuery Staged & Enforced Dataset Provisioning (D1 Staged/Enforced)
# ==============================================================================
# AWS Equivalent: Amazon Redshift / AWS Glue Data Catalog Schema
# ==============================================================================

# D1 Staged/Enforced BigQuery Dataset
resource "google_bigquery_dataset" "d1_staged_enforced" {
  dataset_id                  = "d1_staged_enforced_${var.environment}"
  friendly_name               = "D1 Staged & Enforced Student Dataset"
  description                 = "Contains validated, schema-enforced student onboarding records."
  location                    = var.gcp_region
  default_table_expiration_ms = null # Permanent analytical dataset

  labels = {
    environment = var.environment
    layer       = "d1_staged_enforced"
    managed_by  = "terraform"
  }
}

# Student Onboarding Staged Table with Explicit Schema Enforcement
resource "google_bigquery_table" "student_onboarding_staged" {
  dataset_id          = google_bigquery_dataset.d1_staged_enforced.dataset_id
  table_id            = "student_onboarding_staged"
  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "ingestion_timestamp"
  }

  schema = jsonencode([
    {
      name        = "student_id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Unique UUID identifying the student"
    },
    {
      name        = "ingestion_timestamp"
      type        = "TIMESTAMP"
      mode        = "REQUIRED"
      description = "Record processing timestamp"
    },
    {
      name        = "age"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "Student age (validated between 3 and 18)"
    },
    {
      name        = "evaluation_score"
      type        = "FLOAT"
      mode        = "REQUIRED"
      description = "Diagnostic assessment score (0.0 to 100.0)"
    },
    {
      name        = "has_parent_consent"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "DCYN Binary Flag: 1 = Yes, 0 = No"
    },
    {
      name        = "requires_lsa_support"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "DCYN Binary Flag: 1 = Yes (Score < 70), 0 = No"
    },
    {
      name        = "is_eligible_for_program"
      type        = "INTEGER"
      mode        = "REQUIRED"
      description = "DCYN Binary Flag: 1 = Eligible (Age valid & Consent given), 0 = Ineligible"
    },
    {
      name        = "guardian_contact_hash"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "SHA-256 anonymized hash of parent contact for PII protection"
    }
  ])
}
