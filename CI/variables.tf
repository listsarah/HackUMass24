variable "project_id" {
  description = "The GCP project ID"
}

variable "region" {
  description = "The region for deploying services"
  default     = "us-central1"
}

variable "image_tag" {
  description = "The Docker image tag for the Flask app"
}

variable "next_api_index" {
  description = "The index for the next API subdomain"
}
