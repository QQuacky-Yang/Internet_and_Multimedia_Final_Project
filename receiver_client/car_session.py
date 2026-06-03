"""
receiver_client/car_session.py

Interaction between receiver and delivery car.
"""

from typing import Dict, Any

from common.protocol import (
    make_presentation_message,
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

        self.tpm = ReceiverTPM(
            receiver_id
        )

        self.face_auth = ReceiverFaceAuth()

    def create_presentation(
        self,
        delivery_id: str,
        challenge: Dict[str, Any],
    ) -> Dict[str, Any]:

        face_ok = (
            self.face_auth.authenticate()
        )

        if not face_ok:
            raise RuntimeError(
                "Receiver face authentication failed"
            )

        vc = self.wallet.get_vc(
            delivery_id
        )

        if vc is None:
            raise ValueError(
                f"No VC found for {delivery_id}"
            )

        nonce = challenge["nonce"]

        signature = self.tpm.sign_nonce(
            nonce
        )

        presentation = make_presentation_message(
            delivery_id=delivery_id,
            holder_id=self.receiver_id,
            vc=vc,
            nonce=nonce,
            signature=signature,
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
        "nonce": "TEST_NONCE_123"
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
