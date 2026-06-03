"""
sender_client/main.py

Main sender workflow.
"""

from sender_client.wallet import (
    SenderWallet,
)

from sender_client.car_session import (
    SenderCarSession,
)

from sender_client.face_auth import (
    SenderFaceAuth,
)


class SenderClient:

    def __init__(
        self,
        sender_id: str,
    ):
        self.sender_id = sender_id

        self.wallet = SenderWallet()

        self.session = (
            SenderCarSession(
                sender_id
            )
        )

        self.face_auth = (
            SenderFaceAuth()
        )

    def present_for_pickup(
        self,
        delivery_id: str,
        challenge: dict,
    ) -> dict:

        #
        # Optional sender auth
        #

        if not (
            self.face_auth.authenticate()
        ):
            raise RuntimeError(
                "Sender authentication failed"
            )

        presentation = (
            self.session
            .create_presentation(
                delivery_id,
                challenge,
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

    sender = SenderClient(
        "sender_001"
    )

    presentation = (
        sender.present_for_pickup(
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
