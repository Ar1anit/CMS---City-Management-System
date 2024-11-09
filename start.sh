#!/bin/bash

docker load --input application.tar

docker-compose up -d
