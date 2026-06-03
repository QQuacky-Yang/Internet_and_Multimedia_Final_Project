"""
common/did_utils.py

Simple DID helpers.

Current:
    Local DID generation

Future:
    Real DID methods
    DID Documents
"""

from uuid import uuid4


def generate_did(
    entity_type: str,
    entity_id: str,
) -> str:
    """
    Generate a deterministic-style DID.

    Examples:

    did:delivery:sender:sender_001
    did:delivery:receiver:receiver_001
    did:delivery:car:CAR_RPI5_001
    """

    return (
        f"did:delivery:{entity_type}:{entity_id}"
    )


def generate_vc_id() -> str:
    """
    Generate VC identifier.
    """

    return f"urn:uuid:{uuid4()}"


def generate_delivery_did(
    delivery_id: str,
) -> str:
    """
    Generate delivery DID.
    """

    return (
        f"did:delivery:job:{delivery_id}"
    )


def is_did(value: str) -> bool:
    """
    Simple DID validation.
    """

    return (
        isinstance(value, str)
        and value.startswith("did:")
    )


if __name__ == "__main__":

    sender_did = generate_did(
        "sender",
        "sender_001",
    )

    receiver_did = generate_did(
        "receiver",
        "receiver_001",
    )

    car_did = generate_did(
        "car",
        "CAR_RPI5_001",
    )

    delivery_did = generate_delivery_did(
        "DELIVERY_001",
    )

    vc_id = generate_vc_id()

    print("Sender DID:")
    print(sender_did)

    print("Receiver DID:")
    print(receiver_did)

    print("Car DID:")
    print(car_did)

    print("Delivery DID:")
    print(delivery_did)

    print("VC ID:")
    print(vc_id)

    print("Valid DID:")
    print(is_did(sender_did))
