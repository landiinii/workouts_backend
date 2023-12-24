#!/bin/bash
File=/tmp/dev_build.txt

if [[ "$1" == "gym" ]]; then
    if ! sam build --profile landiinii > $File; then
        cat $File
        echo Failed to run sam build
        exit 0
    else
        echo Successfully ran sam build
    fi
    cd GymFunction
    if ! GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o main . > $File; then
        echo Failed to Build Gyms Function
        cat $File
        exit 0
    else
        echo Successfully Built Gyms Function
    fi
    cd ..
    sam local invoke "GymsFunction" -e GymFunction/event.json --profile landiinii
fi

if [[ "$1" == "all" ]]; then
    if ! sam build --profile landiinii > $File; then
        cat $File
        echo Failed to run sam build
        exit 0
    else
        echo Successfully ran sam build
    fi
    cd AllFunction
    if ! GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o main . > $File; then
        echo Failed to Build All Function
        cat $File
        exit 0
    else
        echo Successfully Built All Function
    fi
    cd ..
    sam local invoke "AllFunction" -e AllFunction/event.json --profile landiinii
fi