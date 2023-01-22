#!/bin/bash
File=/tmp/sandbox_deploy.txt

# build and zip
cd GymFunction
if ! GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o main . > $File; then
  echo Failed to Build Gym Function
  cat $File
  exit 0
else
  echo Successfully Built Gym Function
fi
if zip -q -r main.zip main; then
  echo Zipping Gym Lambda File Complete
else
  echo Failed to Zip Gym Lambda file
  exit 0
fi

# terraform run
cd ../infrastructure
terraform init > $File
if ! grep -q "Terraform has been successfully initialized!" $File; then
  echo Failed to initialize terraform
  cat $File
  exit 0
fi

if ! terraform fmt > $File; then
  echo Failed to format terraform files
  cat $File
  exit 0
fi

terraform validate > $File
if ! grep -q "The configuration is valid." $File; then
  echo Failed to validate terraform
  cat $File
  exit 0
else
  echo Successully Initialized, Formatted, and Validated Terraform, Now calling apply
fi

terraform apply
