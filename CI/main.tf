resource "google_cloud_run_service" "flask_api" {
  name     = "flask-api-${count.index + 1}" # Incrementing service name
  location = var.region
  project  = var.project_id

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/flask-api:${var.image_tag}"
        env {
          name  = "API_URL"
          value = "http://api${count.index + 1}.ismyhouseonfire.tech"
        }
      }
    }
  }

  autogenerate_revision_name = true
  count = var.next_api_index
}

resource "google_dns_record_set" "api_dns" {
  name         = "api${count.index + 1}.ismyhouseonfire.tech."
  type         = "CNAME"
  ttl          = 300
  managed_zone = google_dns_managed_zone.my_zone.name
  rrdatas      = ["flask-api-${count.index + 1}-svgkugxoaa-uc.a.run.app."]  # Ensure trailing dot for rrdatas
  project      = var.project_id
  count        = var.next_api_index
}

resource "google_storage_bucket" "react_app" {
  name     = "ismyhouseonfire-dev"
  location = var.region
  project  = var.project_id
  website {
    main_page_suffix = "index.html"
    not_found_page   = "404.html"
  }
}

resource "google_storage_bucket_object" "react_app_files" {
  for_each = fileset("../client/build", "**") # Use relative path to 'client/build'

  name   = each.value
  bucket = google_storage_bucket.react_app.name
  source = "../client/build/${each.value}"
  content_type = lookup(
    {
      "html" = "text/html",
      "js"   = "application/javascript",
      "css"  = "text/css"
    }, split(".", each.value)[length(split(".", each.value)) - 1], "application/octet-stream"
  )
}

resource "google_storage_bucket_object" "react_config" {
  name   = "config.js"
  bucket = google_storage_bucket.react_app.name
  content = templatefile("${path.module}/config.js.tpl", {
    api_url = "http://api${var.next_api_index}.ismyhouseonfire.tech"
  })
}

resource "google_storage_bucket_iam_member" "public_access" {
  bucket = google_storage_bucket.react_app.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

resource "google_dns_managed_zone" "my_zone" {
  name     = "ismyhouseonfire-dev-zone"
  dns_name = "ismyhouseonfire.tech."
  project  = var.project_id
}

# New resources for load balancing and DNS pointing
resource "google_compute_backend_bucket" "react_backend_bucket" {
  name        = "react-app-backend"
  bucket_name = google_storage_bucket.react_app.name
  project     = var.project_id
}

resource "google_compute_url_map" "url_map" {
  name            = "react-url-map"
  default_service = google_compute_backend_bucket.react_backend_bucket.self_link
  project         = var.project_id
}

resource "google_compute_target_http_proxy" "http_proxy" {
  name    = "react-http-proxy"
  url_map = google_compute_url_map.url_map.self_link
  project = var.project_id
}

resource "google_compute_global_address" "global_ip" {
  name    = "react-global-ip"
  project = var.project_id
}

resource "google_compute_global_forwarding_rule" "forwarding_rule" {
  name       = "react-forwarding-rule"
  target     = google_compute_target_http_proxy.http_proxy.self_link
  port_range = "80"
  ip_address = google_compute_global_address.global_ip.address
  project    = var.project_id
}

resource "google_dns_record_set" "react_dns" {
  name         = "ismyhouseonfire.tech."
  type         = "A"
  ttl          = 300
  managed_zone = google_dns_managed_zone.my_zone.name
  rrdatas      = [google_compute_global_address.global_ip.address]
  project      = var.project_id
}
