"""
common/vc_schema.py

Shared VC inspection helpers.

Used by:
- sender_client
- receiver_client
- rpi5_car
- platform_server if needed
"""

from typing import Any, Dict, Optional


def get_vc_id(vc: Dict[str, Any]) -> Optional[str]:
    return vc.get("id")


def get_vc_types(vc: Dict[str, Any]) -> list:
    return vc.get("type", [])


def get_credential_subject(vc: Dict[str, Any]) -> Dict[str, Any]:
    return vc.get("credentialSubject", {})


def get_delivery_id(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("delivery_id")


def get_package_id(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("package_id")


def get_car_id(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("car_id")


def get_action(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("action")


def get_sender_id(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("sender_id")


def get_receiver_id(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("receiver_id")


def get_sender_pubkey(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("sender_pubkey")


def get_receiver_pubkey(vc: Dict[str, Any]) -> Optional[str]:
    return get_credential_subject(vc).get("receiver_pubkey")

def get_expiration_date(vc: Dict[str, Any]) -> Optional[str]:
    return vc.get("expirationDate")

def is_sender_pickup_vc(vc: Dict[str, Any]) -> bool:
    return (
        "SenderPickupCredential" in get_vc_types(vc)
        and get_action(vc) == "PICKUP_PACKAGE"
    )


def is_receiver_delivery_vc(vc: Dict[str, Any]) -> bool:
    return (
        "ReceiverDeliveryCredential" in get_vc_types(vc)
        and get_action(vc) == "RECEIVE_PACKAGE"
    )


def vc_matches_delivery(
    vc: Dict[str, Any],
    delivery_id: str,
    package_id: str,
    car_id: str,
) -> bool:
    return (
        get_delivery_id(vc) == delivery_id
        and get_package_id(vc) == package_id
        and get_car_id(vc) == car_id
    )


if __name__ == "__main__":
    test_vc = {
        "id": "urn:uuid:test",
        "type": [
            "VerifiableCredential",
            "SenderPickupCredential",
        ],
        "credentialSubject": {
            "delivery_id": "DELIVERY_001",
            "sender_id": "sender_001",
            "sender_pubkey": "sender_pubkey_001",
            "package_id": "PKG_001",
            "car_id": "CAR_RPI5_001",
            "action": "PICKUP_PACKAGE",
        },
    }

    print("VC ID:", get_vc_id(test_vc))
    print("Delivery ID:", get_delivery_id(test_vc))
    print("Package ID:", get_package_id(test_vc))
    print("Car ID:", get_car_id(test_vc))
    print("Is sender pickup VC:", is_sender_pickup_vc(test_vc))
    print(
        "Matches delivery:",
        vc_matches_delivery(
            test_vc,
            "DELIVERY_001",
            "PKG_001",
            "CAR_RPI5_001",
        ),
    )
