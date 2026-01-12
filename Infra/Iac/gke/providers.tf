provider "google" {
  credentials = file("../sa-keys.json")
  project     = "lexical-aileron-483517-f3"
  region      = "us-central1-f"
}