"""
sender_client/platform_api.py

HTTP client for sender to communicate with platform server.
"""

from typing import Any, Dict

import requests

from common.config import SERVER_URL


def register_sender(
    sender_id: str,
    sender_pubkey: str,
    display_name: str | None = None,
) -> Dict[str, Any]:
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

    response.raise_for_status()

    return response.json()


def get_sender_pickup_vc(
    delivery_id: str,
) -> Dict[str, Any]:
    """
    Download sender pickup VC.
    """

    response = requests.get(
        f"{SERVER_URL}/vc/sender/{delivery_id}",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


def get_platform_status() -> Dict[str, Any]:
    """
    Simple health check.
    """

    response = requests.get(
        f"{SERVER_URL}/",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":

    try:
        print(
            "Platform status:"
        )

        print(
            get_platform_status()
        )

    except Exception as exc:

        print(
            "Unable to reach platform:"
        )

        print(exc)
