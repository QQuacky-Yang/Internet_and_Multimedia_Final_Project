"""
sender_client/car_session.py

Interaction between sender and delivery car.
"""

from typing import Dict, Any

from common.protocol import (
    make_signed_challenge_payload,
    make_presentation_message_v2,
)

from sender_client.wallet import (
    SenderWallet,
)

from sender_client.tpm_holder import (
    SenderTPM,
)


class SenderCarSession:

    def __init__(
        self,
        sender_id: str,
    ):
        self.sender_id = sender_id
        self.wallet = SenderWallet()
        self.tpm = SenderTPM(sender_id)

    def create_presentation(
        self,
        delivery_id: str,
        challenge: Dict[str, Any],
    ) -> Dict[str, Any]:

        vc = self.wallet.get_vc(delivery_id)

        if vc is None:
            raise ValueError(
                f"No VC found for {delivery_id}"
            )

        payload = make_signed_challenge_payload(
            holder_id=self.sender_id,
            delivery_id=challenge["delivery_id"],
            car_id=challenge["car_id"],
            package_id=challenge["package_id"],
            phase=challenge["phase"],
            nonce=challenge["nonce"],
        )

        signature = self.tpm.sign_payload(payload)

        presentation = make_presentation_message_v2(
            holder_id=self.sender_id,
            vc=vc,
            challenge=challenge,
            signature=signature,
            signature_type=self.tpm.signature_type(),
        )

        return presentation


if __name__ == "__main__":

    wallet = SenderWallet()

    test_vc = {
        "id": "urn:uuid:test",
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

    wallet.add_vc(
        "DELIVERY_001",
        test_vc,
    )

    challenge = {
        "message_type": "CHALLENGE",
        "delivery_id": "DELIVERY_001",
        "car_id": "CAR_RPI5_001",
        "package_id": "PKG_001",
        "phase": "PICKUP",
        "nonce": "TEST_NONCE_123",
        "created_at": "2026-06-04T00:00:00Z",
    }

    session = SenderCarSession(
        "sender_001"
    )

    presentation = session.create_presentation(
        "DELIVERY_001",
        challenge,
    )

    print("Presentation:")
    print(presentation)