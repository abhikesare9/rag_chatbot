variable vpc_name {
  type        = string
  default     = "mlops-vpc"
  description = "vpc for mlops"
}

variable project_name {
  type        = string
  default     = "lexical-aileron-483517-f3"
  description = "description"
}
variable region {
  type        = string
  default     = "us-central1"
  description = "region for vpc"
}

variable machine_type {
  type        = string
  default     = "e2-medium"
  description = "create vm"
}