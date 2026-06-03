"""
scripts/register_sender.py

Register a sender to the platform server.
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import requests

from common.config import SERVER_URL
from sender_client.tpm_holder import SenderTPM


def register_sender(
    sender_id: str,
    display_name: str,
):
    tpm = SenderTPM(sender_id)

    sender_pubkey = tpm.get_public_key()

    payload = {
        "sender_id": sender_id,
        "sender_pubkey": sender_pubkey,
        "display_name": display_name,
    }

    response = requests.post(
        f"{SERVER_URL}/register_sender",
        json=payload,
        timeout=5,
    )

    if not response.ok:
        try:
            error = response.json()
        except Exception:
            error = {"detail": response.text}

        detail = error.get("detail", "")

        if response.status_code == 400 and "already exists" in detail:
            print(f"Sender already registered: {sender_id}")
            return {
                "status": "already_registered",
                "sender_id": sender_id,
                "detail": detail,
            }

        print("Request failed:")
        print("Status code:", response.status_code)
        print("Response:", error)
        response.raise_for_status()

    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Register sender to platform"
    )

    parser.add_argument(
        "--sender-id",
        default="sender_001",
    )

    parser.add_argument(
        "--display-name",
        default="Default Sender",
    )

    args = parser.parse_args()

    result = register_sender(
        sender_id=args.sender_id,
        display_name=args.display_name,
    )

    print("Registered sender:")
    print(result)


if __name__ == "__main__":
    main()
