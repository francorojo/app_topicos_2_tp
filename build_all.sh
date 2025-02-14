#!/bin/bash

cd ai_model_service
./build.sh
cd ../api_core_service
./build.sh
cd ../log_service
./build.sh
cd ../users_service
./build.sh

cd ..
