#!/bin/bash

ctrlc_received=0

# SIGINT is a signal generated when a user presses Control-C. This will terminate the program from the terminal. 
trap deactivate_venv SIGINT

deactivate_venv() {
    deactivate
    exit 0
}

source src/venv/bin/activate
python3 src/server.py