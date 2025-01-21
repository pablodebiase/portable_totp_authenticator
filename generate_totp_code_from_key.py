import sys

import pyotp
import base64


def generate_totp(secret_key, digits=6, interval=30):
    """
    Generate a TOTP code using the provided secret key.

    :param secret_key: The TOTP secret key (in Base32 encoding).
    :param digits: Number of digits in the TOTP (default is 6).
    :param interval: Time interval for TOTP code (default is 30 seconds).
    :return: The current TOTP code.
    """
    try:
        # Ensure the key is Base32 encoded
        if isinstance(secret_key, bytes):
            secret_key = base64.b32encode(secret_key).decode('utf-8')

        # Initialize TOTP with the provided secret
        totp = pyotp.TOTP(secret_key, digits=digits, interval=interval)

        # Generate the current TOTP
        current_code = totp.now()
        return current_code

    except Exception as e:
        print(f"Error generating TOTP: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Replace this with your actual TOTP secret (Base32 encoded or raw bytes)
    if len(sys.argv) > 1:
        secret_key_from_argument = sys.argv[1]

        # Generate a TOTP code
        totp_code = generate_totp(secret_key_from_argument)
        if totp_code:
            print(f"Your TOTP code is: {totp_code}")
    else:
        print("Please provide a TOTP secret key (Base32 encoded) as an argument.")