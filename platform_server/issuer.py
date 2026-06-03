"""
platform_server/issuer.py

Responsible for:
1. loading/generating the platform issuer keypair
2. creating Delivery Verifiable Credentials
3. signing credentials
4. verifying platform-issued credentials
"""

import json
import base64
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization


KEY_DIR = Path("data/platform/keys")
PRIVATE_KEY_PATH = KEY_DIR / "issuer_private_key.pem"
PUBLIC_KEY_PATH = KEY_DIR / "issuer_public_key.pem"

PLATFORM_DID = "did:platform:logistics"
DEFAULT_EXPIRATION_HOURS = 24


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8")


def _b64decode(data: str) -> bytes:
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def canonical_json(data: Dict[str, Any]) -> bytes:
    """
    Convert JSON to deterministic bytes before signing.
    The proof field is excluded when signing/verifying.
    """
    unsigned = dict(data)
    unsigned.pop("proof", None)

    return json.dumps(
        unsigned,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def generate_issuer_keypair() -> None:
    """
    Generate platform issuer Ed25519 keypair if it does not already exist.
    """
    KEY_DIR.mkdir(parents=True, exist_ok=True)

    if PRIVATE_KEY_PATH.exists() and PUBLIC_KEY_PATH.exists():
        return

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    PRIVATE_KEY_PATH.write_bytes(private_bytes)
    PUBLIC_KEY_PATH.write_bytes(public_bytes)


def load_private_key() -> Ed25519PrivateKey:
    generate_issuer_keypair()

    key_data = PRIVATE_KEY_PATH.read_bytes()
    private_key = serialization.load_pem_private_key(
        key_data,
        password=None,
    )

    if not isinstance(private_key, Ed25519PrivateKey):
        raise TypeError("Issuer private key is not Ed25519")

    return private_key


def load_public_key() -> Ed25519PublicKey:
    generate_issuer_keypair()

    key_data = PUBLIC_KEY_PATH.read_bytes()
    public_key = serialization.load_pem_public_key(key_data)

    if not isinstance(public_key, Ed25519PublicKey):
        raise TypeError("Issuer public key is not Ed25519")

    return public_key


def sign_vc(vc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Sign a VC using the platform issuer private key.
    """
    private_key = load_private_key()
    message = canonical_json(vc)
    signature = private_key.sign(message)

    signed_vc = dict(vc)
    signed_vc["proof"] = {
        "type": "Ed25519Signature",
        "created": datetime.now(timezone.utc).isoformat(),
        "proofPurpose": "assertionMethod",
        "verificationMethod": f"{PLATFORM_DID}#issuer-key-1",
        "signature": _b64encode(signature),
    }

    return signed_vc


def verify_vc(vc: Dict[str, Any]) -> bool:
    """
    Verify that a VC was signed by this platform issuer.
    """
    proof = vc.get("proof")
    if not proof:
        return False

    signature_b64 = proof.get("signature")
    if not signature_b64:
        return False

    public_key = load_public_key()
    message = canonical_json(vc)
    signature = _b64decode(signature_b64)

    try:
        public_key.verify(signature, message)
        return True
    except Exception:
        return False


def create_delivery_vc(
    receiver_id: str,
    receiver_pubkey: str,
    package_id: str,
    car_id: str,
    delivery_id: str | None = None,
    expiration_hours: int = DEFAULT_EXPIRATION_HOURS,
) -> Dict[str, Any]:
    """
    Create and sign a delivery VC.

    This VC says:
    receiver_id is authorized to receive package_id from car_id.
    """
    now = datetime.now(timezone.utc)
    valid_until = now + timedelta(hours=expiration_hours)

    vc_id = f"urn:uuid:{uuid.uuid4()}"
    delivery_id = delivery_id or f"delivery-{uuid.uuid4()}"

    unsigned_vc = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://example.com/contexts/delivery-v1",
        ],
        "id": vc_id,
        "type": [
            "VerifiableCredential",
            "DeliveryCredential",
        ],
        "issuer": PLATFORM_DID,
        "issuanceDate": now.isoformat(),
        "expirationDate": valid_until.isoformat(),
        "credentialSubject": {
            "delivery_id": delivery_id,
            "receiver_id": receiver_id,
            "receiver_pubkey": receiver_pubkey,
            "package_id": package_id,
            "car_id": car_id,
        },
    }

    return sign_vc(unsigned_vc)


def export_platform_public_key() -> str:
    """
    Return platform public key as PEM string.
    Cars need this to verify VC signatures.
    """
    generate_issuer_keypair()
    return PUBLIC_KEY_PATH.read_text()

def create_sender_pickup_vc(
    sender_id: str,
    sender_pubkey: str,
    package_id: str,
    car_id: str,
    delivery_id: str,
    expiration_hours: int = DEFAULT_EXPIRATION_HOURS,
) -> Dict[str, Any]:
    """
    Create and sign a VC proving that the sender is authorized
    to hand package_id to car_id.
    """

    now = datetime.now(timezone.utc)
    valid_until = now + timedelta(hours=expiration_hours)

    unsigned_vc = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://example.com/contexts/delivery-v1",
        ],
        "id": f"urn:uuid:{uuid.uuid4()}",
        "type": [
            "VerifiableCredential",
            "SenderPickupCredential",
        ],
        "issuer": PLATFORM_DID,
        "issuanceDate": now.isoformat(),
        "expirationDate": valid_until.isoformat(),
        "credentialSubject": {
            "delivery_id": delivery_id,
            "sender_id": sender_id,
            "sender_pubkey": sender_pubkey,
            "package_id": package_id,
            "car_id": car_id,
            "action": "PICKUP_PACKAGE",
        },
    }

    return sign_vc(unsigned_vc)


def create_receiver_delivery_vc(
    receiver_id: str,
    receiver_pubkey: str,
    package_id: str,
    car_id: str,
    delivery_id: str,
    expiration_hours: int = DEFAULT_EXPIRATION_HOURS,
) -> Dict[str, Any]:
    """
    Create and sign a VC proving that the receiver is authorized
    to receive package_id from car_id.
    """

    now = datetime.now(timezone.utc)
    valid_until = now + timedelta(hours=expiration_hours)

    unsigned_vc = {
        "@context": [
            "https://www.w3.org/2018/credentials/v1",
            "https://example.com/contexts/delivery-v1",
        ],
        "id": f"urn:uuid:{uuid.uuid4()}",
        "type": [
            "VerifiableCredential",
            "ReceiverDeliveryCredential",
        ],
        "issuer": PLATFORM_DID,
        "issuanceDate": now.isoformat(),
        "expirationDate": valid_until.isoformat(),
        "credentialSubject": {
            "delivery_id": delivery_id,
            "receiver_id": receiver_id,
            "receiver_pubkey": receiver_pubkey,
            "package_id": package_id,
            "car_id": car_id,
            "action": "RECEIVE_PACKAGE",
        },
    }

    return sign_vc(unsigned_vc)


if __name__ == "__main__":
    sender_vc = create_sender_pickup_vc(
        sender_id="sender_001",
        sender_pubkey="sender-public-key-placeholder",
        package_id="PKG_001",
        car_id="CAR_RPI5_001",
        delivery_id="DELIVERY_001",
    )

    receiver_vc = create_receiver_delivery_vc(
        receiver_id="receiver_001",
        receiver_pubkey="receiver-public-key-placeholder",
        package_id="PKG_001",
        car_id="CAR_RPI5_001",
        delivery_id="DELIVERY_001",
    )

    print("Sender Pickup VC valid:", verify_vc(sender_vc))
    print("Receiver Delivery VC valid:", verify_vc(receiver_vc))
