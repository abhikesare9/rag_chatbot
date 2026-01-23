resource "google_project_service" "artifact_registry" {
  service = "artifactregistry.googleapis.com"
}

resource "google_artifact_registry_repository" "docker_repo" {
  location      = "us-central1"
  repository_id = "rag-backend-test"
  description   = "Docker repo for container images"
  format        = "DOCKER"

  depends_on = [
    google_project_service.artifact_registry
  ]
}

resource "google_artifact_registry_repository" "docker_repo_for_agent" {
  location      = "us-central1"
  repository_id = "agent-repo-test"
  description   = "Docker repo for container images"
  format        = "DOCKER"

  depends_on = [
    google_project_service.artifact_registry
  ]
}