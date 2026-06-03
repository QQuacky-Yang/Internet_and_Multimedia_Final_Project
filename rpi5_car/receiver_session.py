"""
rpi5_car/receiver_session.py

Session helpers for receiving VC presentations.

Current:
    Local simulation

Future:
    Replace with HTTP/WebSocket/Bluetooth communication.
"""

from typing import Any, Dict

from common.protocol import (
    make_presentation_message,
    validate_presentation_message,
)


def simulate_receive_presentation(
    delivery_id: str,
    holder_id: str,
    vc: Dict[str, Any],
    nonce: str,
    signature: str = "signature-placeholder",
) -> Dict[str, Any]:
    """
    Simulate receiving a VC presentation from sender/receiver.
    """

    return make_presentation_message(
        delivery_id=delivery_id,
        holder_id=holder_id,
        vc=vc,
        nonce=nonce,
        signature=signature,
    )


def validate_received_presentation(
    presentation: Dict[str, Any],
) -> bool:
    """
    Check that a presentation message has required fields.
    """

    return validate_presentation_message(
        presentation
    )


if __name__ == "__main__":

    test_vc = {
        "type": [
            "VerifiableCredential",
            "SenderPickupCredential",
        ],
        "credentialSubject": {
            "delivery_id": "DELIVERY_001",
            "sender_id": "sender_001",
            "package_id": "PKG_001",
            "car_id": "CAR_RPI5_001",
            "action": "PICKUP_PACKAGE",
        },
    }

    presentation = simulate_receive_presentation(
        delivery_id="DELIVERY_001",
        holder_id="sender_001",
        vc=test_vc,
        nonce="nonce-placeholder",
    )

    print("Presentation:")
    print(presentation)

    print("Valid:")
    print(validate_received_presentation(presentation))
