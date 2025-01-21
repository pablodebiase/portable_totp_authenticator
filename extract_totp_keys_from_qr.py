
# Extract TOTP Key from Google Authenticator Export QR Code data
import base64
from urllib.parse import unquote

import cv2
from google.protobuf.json_format import MessageToDict
from pyzbar.pyzbar import decode
from google_authenticator_migration_pb2 import MigrationPayload


def decode_google_auth_export_data(data_url):
    # Extract the 'data' parameter
    data_base64 = data_url.split("data=")[-1]
    # URL-decode the Base64 string
    data_base64 = unquote(data_base64)
    # Ensure the Base64 string is properly padded
    missing_padding = len(data_base64) % 4
    if missing_padding:
        data_base64 += "=" * (4 - missing_padding)
    # Decode the Base64 data
    try:
        decoded_data = base64.urlsafe_b64decode(data_base64)
    except base64.binascii.Error as e:
        print(f"Error decoding Base64: {e}")
        exit(1)
    # Parse the protocol buffer data
    migration_payload = MigrationPayload()
    migration_payload.ParseFromString(decoded_data)
    # Convert the parsed data to a dictionary for readability
    payload_dict = MessageToDict(migration_payload)
    # Print the results
    for otp in payload_dict.get('otpParameters', []):
        print(f"Account Name: {otp.get('name')}")
        print(f"Issuer: {otp.get('issuer')}")
        base64_key = otp.get('secret')
        decoded_key = base64.b64decode(base64_key)
        base32_key = base64.b32encode(decoded_key).decode('utf-8')
        print(f"Secret Key: {base32_key}")
        print("-" * 40)


def read_qr_code_from_webcam():
    """
    Reads a QR code from the webcam and returns the data as a string.

    Returns:
        str: The data encoded in the QR code, or None if no QR code is detected.
    """
    # Initialize the webcam (default camera index is 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access the webcam.")
        return None

    print("Press 'q' to quit.")

    qr_data = None

    while True:
        # Capture frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame from the webcam.")
            break

        # Decode QR codes in the frame
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')  # Decode QR data as a UTF-8 string
            print(f"QR Code Data: {qr_data}")

            # Draw a rectangle around the QR code
            points = obj.polygon
            if len(points) > 4:  # If QR code polygon has more than 4 points
                hull = cv2.convexHull(points)
                points = hull

            n = len(points)
            for j in range(n):
                start_point = (int(points[j].x), int(points[j].y))
                end_point = (int(points[(j + 1) % n].x), int(points[(j + 1) % n].y))
                cv2.line(frame, start_point, end_point, (0, 255, 0), 3)

        # Display the video feed with any detected QR codes highlighted
        cv2.imshow("QR Code Scanner", frame)

        # Exit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # If a QR code is detected, break out of the loop
        if qr_data:
            break

    # Release the webcam and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    return qr_data


if __name__ == "__main__":
    auth_export_data = read_qr_code_from_webcam()
    decode_google_auth_export_data(auth_export_data)