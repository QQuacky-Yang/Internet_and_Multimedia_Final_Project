"""
scripts/register_receiver.py

Register a receiver to the platform server.
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import requests

from common.config import SERVER_URL
from receiver_client.tpm_holder import ReceiverTPM


def register_receiver(
    receiver_id: str,
    display_name: str,
):
    tpm = ReceiverTPM(receiver_id)

    receiver_pubkey = tpm.get_public_key()

    payload = {
        "receiver_id": receiver_id,
        "receiver_pubkey": receiver_pubkey,
        "display_name": display_name,
    }

    response = requests.post(
        f"{SERVER_URL}/register_receiver",
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
            print(f"Receiver already registered: {receiver_id}")
            return {
                "status": "already_registered",
                "receiver_id": receiver_id,
                "detail": detail,
            }

        print("Request failed:")
        print("Status code:", response.status_code)
        print("Response:", error)
        response.raise_for_status()

    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Register receiver to platform"
    )

    parser.add_argument(
        "--receiver-id",
        default="receiver_001",
    )

    parser.add_argument(
        "--display-name",
        default="Default Receiver",
    )

    args = parser.parse_args()

    result = register_receiver(
        receiver_id=args.receiver_id,
        display_name=args.display_name,
    )

    print("Registered receiver:")
    print(result)


if __name__ == "__main__":
    main()
