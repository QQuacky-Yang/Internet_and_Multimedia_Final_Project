"""
receiver_client/main.py

Main receiver workflow.
"""

from receiver_client.wallet import (
    ReceiverWallet,
)

from receiver_client.car_session import (
    ReceiverCarSession,
)


class ReceiverClient:

    def __init__(
        self,
        receiver_id: str,
    ):
        self.receiver_id = receiver_id

        self.wallet = ReceiverWallet()

        self.session = ReceiverCarSession(
            receiver_id
        )

    def present_for_delivery(
        self,
        delivery_id: str,
        challenge: dict,
    ) -> dict:

        presentation = (
            self.session.create_presentation(
                delivery_id,
                challenge,
            )
        )

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

    receiver = ReceiverClient(
        "receiver_001"
    )

    presentation = receiver.present_for_delivery(
        "DELIVERY_001",
        challenge,
    )

    print("Presentation:")
    print(presentation)
