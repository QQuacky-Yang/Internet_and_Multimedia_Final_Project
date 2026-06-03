"""
receiver_client/wallet.py

Receiver VC wallet.

Manages all receiver delivery credentials.
"""

from typing import Any, Dict, Optional

from receiver_client.vc_store import (
    save_receiver_vc,
    load_receiver_vc,
    list_receiver_vcs,
)


class ReceiverWallet:

    def add_vc(
        self,
        delivery_id: str,
        vc: Dict[str, Any],
    ) -> None:

        save_receiver_vc(
            delivery_id,
            vc,
        )

    def get_vc(
        self,
        delivery_id: str,
    ) -> Optional[Dict[str, Any]]:

        return load_receiver_vc(
            delivery_id
        )

    def list_credentials(
        self,
    ) -> list[str]:

        return list_receiver_vcs()

    def has_vc(
        self,
        delivery_id: str,
    ) -> bool:

        return (
            self.get_vc(
                delivery_id
            )
            is not None
        )


if __name__ == "__main__":

    wallet = ReceiverWallet()

    test_vc = {
        "id": "urn:uuid:test-wallet-vc",
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

    print(
        "Has VC:",
        wallet.has_vc(
            "DELIVERY_001"
        )
    )

    print(
        "VC:",
        wallet.get_vc(
            "DELIVERY_001"
        )
    )

    print(
        "Credentials:"
    )

    print(
        wallet.list_credentials()
    )

