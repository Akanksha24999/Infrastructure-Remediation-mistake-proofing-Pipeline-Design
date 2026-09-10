# ==============================================================================
# Terraform Outputs Export
# ==============================================================================

output "gcs_d0_raw_landing_bucket_name" {
  description = "Name of the provisioned GCS raw landing bucket."
  value       = google_storage_bucket.d0_raw_landing.name
}

output "gcs_d0_raw_landing_bucket_url" {
  description = "Google Cloud Storage URI for D0 raw landing."
  value       = google_storage_bucket.d0_raw_landing.url
}

output "bigquery_d1_dataset_id" {
  description = "ID of the provisioned D1 BigQuery dataset."
  value       = google_bigquery_dataset.d1_staged_enforced.dataset_id
}

output "bigquery_student_staged_table_id" {
  description = "Fully qualified table ID for staged student onboarding data."
  value       = "${google_bigquery_dataset.d1_staged_enforced.dataset_id}.${google_bigquery_table.student_onboarding_staged.table_id}"
}
