#!/bin/bash

# Step 1: Go to the site-packages directory
cd .venv/lib/python3.13/site-packages || exit 1

# Step 2: Create zip file at the root of the project
zip -r9 ../../../../harmonyseeker_api.zip *

# Step 3: Go back to the root of the project
cd ../../../../

# Step 4: Add code to the zip file
zip -rg harmonyseeker_api.zip routers main.py lambda_function.py