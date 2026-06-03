"""
common/protocol.py

Shared protocol message helpers.

Used by:
- sender_client
- receiver_client
- rpi5_car
"""

import base64
import os
from datetime import datetime, timezone
from typing import Any, Dict


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def generate_nonce(num_bytes: int = 32) -> str:
    """
    Generate a URL-safe random nonce.

    The car sends this nonce to sender/receiver.
    Sender/receiver signs it using TPM-backed key.
    """

    return base64.urlsafe_b64encode(
        os.urandom(num_bytes)
    ).decode("utf-8")


def make_challenge_message(
    delivery_id: str,
    car_id: str,
    package_id: str,
    phase: str,
) -> Dict[str, Any]:
    """
    Create challenge message from car to sender/receiver.

    phase:
        PICKUP
        DELIVERY
    """

    return {
        "message_type": "CHALLENGE",
        "delivery_id": delivery_id,
        "car_id": car_id,
        "package_id": package_id,
        "phase": phase,
        "nonce": generate_nonce(),
        "created_at": now_iso(),
    }


def make_presentation_message(
    delivery_id: str,
    holder_id: str,
    vc: Dict[str, Any],
    nonce: str,
    signature: str,
) -> Dict[str, Any]:
    """
    Create message from sender/receiver to car.

    This contains:
    - VC
    - nonce
    - TPM-backed signature over nonce
    """

    return {
        "message_type": "VC_PRESENTATION",
        "delivery_id": delivery_id,
        "holder_id": holder_id,
        "vc": vc,
        "nonce": nonce,
        "signature": signature,
        "created_at": now_iso(),
    }


def validate_challenge_message(message: Dict[str, Any]) -> bool:
    required_fields = {
        "message_type",
        "delivery_id",
        "car_id",
        "package_id",
        "phase",
        "nonce",
        "created_at",
    }

    return (
        isinstance(message, dict)
        and message.get("message_type") == "CHALLENGE"
        and required_fields.issubset(message.keys())
    )


def validate_presentation_message(message: Dict[str, Any]) -> bool:
    required_fields = {
        "message_type",
        "delivery_id",
        "holder_id",
        "vc",
        "nonce",
        "signature",
        "created_at",
    }

    return (
        isinstance(message, dict)
        and message.get("message_type") == "VC_PRESENTATION"
        and required_fields.issubset(message.keys())
    )

def make_signed_challenge_payload(
    holder_id: str,
    delivery_id: str,
    car_id: str,
    package_id: str,
    phase: str,
    nonce: str,
) -> Dict[str, Any]:
    """
    Canonical payload signed by sender/receiver.

    This prevents replay across:
    - different deliveries
    - different cars
    - different packages
    - pickup vs delivery phase
    """

    return {
        "holder_id": holder_id,
        "delivery_id": delivery_id,
        "car_id": car_id,
        "package_id": package_id,
        "phase": phase,
        "nonce": nonce,
    }


def make_presentation_message_v2(
    holder_id: str,
    vc: Dict[str, Any],
    challenge: Dict[str, Any],
    signature: str,
    signature_type: str = "SIMULATED",
) -> Dict[str, Any]:
    """
    VC presentation tied to a car challenge.
    """

    return {
        "message_type": "VC_PRESENTATION",
        "holder_id": holder_id,
        "vc": vc,
        "challenge": challenge,
        "signature": signature,
        "signature_type": signature_type,
        "created_at": now_iso(),
    }


def validate_presentation_message_v2(
    message: Dict[str, Any],
) -> bool:
    required_fields = {
        "message_type",
        "holder_id",
        "vc",
        "challenge",
        "signature",
        "signature_type",
        "created_at",
    }

    return (
        isinstance(message, dict)
        and message.get("message_type") == "VC_PRESENTATION"
        and required_fields.issubset(message.keys())
        and validate_challenge_message(message["challenge"])
    )

if __name__ == "__main__":
    challenge = make_challenge_message(
        delivery_id="DELIVERY_001",
        car_id="CAR_RPI5_001",
        package_id="PKG_001",
        phase="PICKUP",
    )

    print("Challenge:")
    print(challenge)
    print("Valid challenge:", validate_challenge_message(challenge))

    presentation = make_presentation_message(
        delivery_id="DELIVERY_001",
        holder_id="sender_001",
        vc={"example": "vc"},
        nonce=challenge["nonce"],
        signature="signature-placeholder",
    )

    print("Presentation:")
    print(presentation)
    print("Valid presentation:", validate_presentation_message(presentation))
