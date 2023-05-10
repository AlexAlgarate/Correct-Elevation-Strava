#!/bin/bash

# Activate virtual environment if necessary
if [ -d venv ]; then
  . venv/bin/activate
fi

# Run linter
flake8 src/correct_elevation

# Deactivate virtual environment if necessary
if [ -n "$VIRTUAL_ENV" ]; then
  deactivate
fi
