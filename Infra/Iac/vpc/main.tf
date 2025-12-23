resource "google_compute_network" "vpc_network" {
  name = var.vpc_name
  project = var.project_name
  auto_create_subnetworks = false

}

resource "google_compute_subnetwork" "public-subnet-1" {
  name          = "public-subnet-1"
  ip_cidr_range = "10.168.224.0/19"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id
}


resource "google_compute_subnetwork" "public-subnet-2" {
  name          = "public-subnet-2"
  ip_cidr_range = "10.168.192.0/19"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_subnetwork" "private-subnet-1" {
  name          = "private-subnet-1"
  ip_cidr_range = "10.168.0.0/18"
  region        = "us-central1"
  purpose       = "PRIVATE"
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_subnetwork" "private-subnet-2" {
  name          = "private-subnet-2"
  ip_cidr_range = "10.168.64.0/18"
  region        = "us-central1"
  purpose       = "PRIVATE"
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_subnetwork" "private-subnet-3" {
  name          = "private-subnet-3"
  ip_cidr_range = "10.168.128.0/18"
  purpose       = "PRIVATE"
  region        = "us-central1"
  network       = google_compute_network.vpc_network.id
}

resource "google_compute_router" "router" {
  project = var.project_name
  name    = "nat-router"
  network = google_compute_network.vpc_network.id
  region  = var.region
}

resource "google_compute_router_nat" "nat" {
  name                               = "my-router-nat"
  router                             = google_compute_router.router.name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "LIST_OF_SUBNETWORKS"
  subnetwork {
    name                    = google_compute_subnetwork.private-subnet-1.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
  subnetwork {
    name                    = google_compute_subnetwork.private-subnet-2.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }
  subnetwork {
    name                    = google_compute_subnetwork.private-subnet-3.id
    source_ip_ranges_to_nat = ["ALL_IP_RANGES"]
  }

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}


#create vm to deploy infra on it.
# resource "google_compute_instance" "mlops-vm" {
#   project      = var.project_name
#   zone         = "${var.region}-f"
#   name         = "mlops-vm"
#   machine_type = var.machine_type
#   tags         = ["allow-ssh"]
#   boot_disk {
#     initialize_params {
#       image = "debian-cloud/debian-11"
#     }
#   }
#   network_interface {
#     network    = google_compute_network.vpc_network.id
#     subnetwork = google_compute_subnetwork.private-subnet-1.id # Replace with a reference or self link to your subnet, in quotes
    
#   }
# }

# resource "google_compute_firewall" "rules" {
#   project = var.project_name
#   name    = "allow-ssh"
#   network = google_compute_network.vpc_network.id 

#   allow {
#     protocol = "tcp"
#     ports    = ["22"]
#   }
#   source_ranges = ["0.0.0.0/0"]
# }