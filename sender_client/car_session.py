"""
sender_client/car_session.py

Interaction between sender and delivery car.
"""

from typing import Dict, Any

from common.protocol import (
    make_presentation_message,
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

        self.tpm = SenderTPM(
            sender_id
        )

    def create_presentation(
        self,
        delivery_id: str,
        challenge: Dict[str, Any],
    ) -> Dict[str, Any]:

        vc = self.wallet.get_vc(
            delivery_id
        )

        if vc is None:

            raise ValueError(
                f"No VC found for "
                f"{delivery_id}"
            )

        nonce = challenge["nonce"]

        signature = (
            self.tpm.sign_nonce(
                nonce
            )
        )

        presentation = (
            make_presentation_message(
                delivery_id=delivery_id,
                holder_id=self.sender_id,
                vc=vc,
                nonce=nonce,
                signature=signature,
            )
        )

        return presentation


if __name__ == "__main__":

    #
    # Setup test VC
    #

    wallet = SenderWallet()

    test_vc = {
        "id": "urn:uuid:test",
        "type": [
            "VerifiableCredential",
            "SenderPickupCredential",
        ],
        "credentialSubject": {
            "delivery_id":
                "DELIVERY_001",
            "sender_id":
                "sender_001",
            "package_id":
                "PKG_001",
            "car_id":
                "CAR_RPI5_001",
            "action":
                "PICKUP_PACKAGE",
        },
    }

    wallet.add_vc(
        "DELIVERY_001",
        test_vc,
    )

    challenge = {
        "nonce":
            "TEST_NONCE_123"
    }

    session = SenderCarSession(
        "sender_001"
    )

    presentation = (
        session.create_presentation(
            "DELIVERY_001",
            challenge,
        )
    )

    print(
        "Presentation:"
    )

    print(
        presentation
    )
