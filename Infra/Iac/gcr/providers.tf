provider "google" {
  credentials = file("sa.json")
  project     = "daring-night-479819-f3"
  region      = "us-central1"
}