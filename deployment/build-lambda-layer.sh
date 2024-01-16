#!/bin/bash
set -eo pipefail
cd database/crdr-reconciliation/src/function
rm -rf package
pip3 install --target ./package/python -r requirements.txt

