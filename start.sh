#!/bin/bash

ctrlc_received=0

trap deactivate_venv SIGINT

deactivate_venv() {
    deactivate
    exit 0
}

source src/venv/bin/activate
python3 src/server.py


