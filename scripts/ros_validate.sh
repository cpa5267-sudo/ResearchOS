#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "========== ROS VALIDATION: git status =========="
git status --short

echo ""
echo "========== ROS VALIDATION: source files =========="
find src/researchos -maxdepth 3 -type f | sort

echo ""
echo "========== ROS VALIDATION: test files =========="
find tests -maxdepth 3 -type f | sort

echo ""
echo "========== ROS VALIDATION: unit tests =========="
PYTHONPATH=src python -m unittest discover -s tests -v

echo ""
echo "========== ROS VALIDATION: main run =========="
PYTHONPATH=src python src/researchos/main.py
