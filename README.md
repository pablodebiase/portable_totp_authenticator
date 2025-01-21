# Portable TOTP Authenticator with Migration Tool
This project provides a set of command-line tools for migrating Google Authenticator TOTP secrets from one device to any device with Python and be able to generate TOTP codes.

## Generate a TOTP code from a secret key
The file `generate_totp_code_from_key.py`, is a Python script that generates a Time-based One-Time Password (TOTP) code from a provided secret key.

## Extract TOTP keys from a QR code
The script `extract_totp_keys_from_qr.py` extracts TOTP (Time-Based One-Time Password) keys from Google Authenticator export QR code data. It uses the webcam to read the QR code, decodes the data, and then parses the protocol buffer data to extract the TOTP secret keys, account names, and issuers.

## Get Google Authenticator export QR code data


To get the QR code from the Google Authenticator app with the export data, follow these steps:

1. Open the Google Authenticator app on your device.
2. Tap the three dots (⋮) in the top right corner of the screen.
3. Tap "Settings".
4. Tap "Export accounts".
5. Select the accounts you want to export.
6. Tap "Export" and then "QR code".
7. A QR code will be displayed on the screen.

You can then use a webcam or a QR code reader app to scan this QR code and extract the TOTP secret keys, account names, and issuers.

## Installation

To install the tools, run the following command in your terminal:

```bash
bash ./install.sh
```

## Execution Instructions

To execute the tools, run the following commands in your terminal:

```bash
# Extract TOTP keys from a QR code
.venv/bin/python extract_totp_keys_from_qr.py
# Generate a TOTP code from a secret key
.venv/bin/python generate_totp_code_from_key.py <secret_key>
```

## Requirements
- Python 3.12
- pip
- and packages in requirements.txt