#!/bin/sh

echo "Running pylint..."
pylint projet
if [ $? -ne 0 ]; then
    echo "Pylint failed. Exiting."
    exit 1
fi

echo "Starting application..."
exec python -m projet
