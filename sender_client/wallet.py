"""
sender_client/wallet.py

Sender VC wallet.

Manages all sender credentials.
"""

from typing import Any, Dict, Optional

from sender_client.vc_store import (
    save_sender_vc,
    load_sender_vc,
    list_sender_vcs,
)


class SenderWallet:

    def add_vc(
        self,
        delivery_id: str,
        vc: Dict[str, Any],
    ) -> None:

        save_sender_vc(
            delivery_id,
            vc,
        )

    def get_vc(
        self,
        delivery_id: str,
    ) -> Optional[Dict[str, Any]]:

        return load_sender_vc(
            delivery_id
        )

    def list_credentials(
        self,
    ) -> list[str]:

        return list_sender_vcs()

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

    wallet = SenderWallet()

    test_vc = {
        "id": "urn:uuid:test-wallet-vc",
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
