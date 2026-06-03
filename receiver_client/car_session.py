"""
receiver_client/car_session.py

Interaction between receiver and delivery car.
"""

from typing import Dict, Any

from common.protocol import (
    make_signed_challenge_payload,
    make_presentation_message_v2,
)

from receiver_client.wallet import (
    ReceiverWallet,
)

from receiver_client.tpm_holder import (
    ReceiverTPM,
)

from receiver_client.face_auth import (
    ReceiverFaceAuth,
)


class ReceiverCarSession:

    def __init__(
        self,
        receiver_id: str,
    ):
        self.receiver_id = receiver_id
        self.wallet = ReceiverWallet()
        self.tpm = ReceiverTPM(receiver_id)
        self.face_auth = ReceiverFaceAuth()

    def create_presentation(
        self,
        delivery_id: str,
        challenge: Dict[str, Any],
    ) -> Dict[str, Any]:

        face_ok = self.face_auth.authenticate()

        if not face_ok:
            raise RuntimeError(
                "Receiver face authentication failed"
            )

        vc = self.wallet.get_vc(delivery_id)

        if vc is None:
            raise ValueError(
                f"No VC found for {delivery_id}"
            )

        payload = make_signed_challenge_payload(
            holder_id=self.receiver_id,
            delivery_id=challenge["delivery_id"],
            car_id=challenge["car_id"],
            package_id=challenge["package_id"],
            phase=challenge["phase"],
            nonce=challenge["nonce"],
        )

        signature = self.tpm.sign_payload(payload)

        presentation = make_presentation_message_v2(
            holder_id=self.receiver_id,
            vc=vc,
            challenge=challenge,
            signature=signature,
            signature_type=self.tpm.signature_type(),
        )

        presentation["face_verified"] = True

        return presentation


if __name__ == "__main__":

    wallet = ReceiverWallet()

    test_vc = {
        "id": "urn:uuid:test",
        "type": [
            "VerifiableCredential",
            "ReceiverDeliveryCredential",
        ],
        "credentialSubject": {
            "delivery_id": "DELIVERY_001",
            "receiver_id": "receiver_001",
            "package_id": "PKG_001",
            "car_id": "CAR_RPI5_001",
            "action": "RECEIVE_PACKAGE",
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
        "phase": "DELIVERY",
        "nonce": "TEST_NONCE_123",
        "created_at": "2026-06-04T00:00:00Z",
    }

    session = ReceiverCarSession(
        "receiver_001"
    )

    presentation = session.create_presentation(
        "DELIVERY_001",
        challenge,
    )

    print("Presentation:")
    print(presentation)