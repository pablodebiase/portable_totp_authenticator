#!/bin/bash

python3 -m venv .venv
python=.venv/bin/python
$python -m pip install --upgrade pip
$python -m pip install -r requirements.txt
bash generate-py-from-proto.bash

echo "To run the tools:"
echo ".venv/bin/python extract_totp_keys_from_qr.py"
echo ".venv/bin/python generate_totp_code_from_key.py"
echo
echo "For more information read the README.md file"