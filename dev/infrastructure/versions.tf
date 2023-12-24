terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.47"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-storage-819643791142"
    dynamodb_table = "terraform-state-lock-819643791142"
    key            = "workouts-lambdas.tfstate"
    region         = "us-west-2"
    profile        = "stylifi"
  } # Update in new environment
}


provider "aws" {
  profile = "stylifi"
  region  = var.region
  default_tags {
    tags = {
      Name  = "workouts"
      Owner = "Landen Bailey"
    }
  }
}
