"""
common/crypto_utils.py

Generic cryptographic helpers.

Current:
    Software RSA signing

Future:
    TPM-backed signing
"""

import base64
import json

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)


def generate_rsa_keypair():
    """
    Generate RSA keypair.

    Used for:
    - Development
    - TPM simulation
    """

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()

    return private_key, public_key


def export_public_key(public_key) -> str:
    """
    Export PEM public key string.
    """

    return public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")


def canonical_json(data: dict) -> bytes:
    """
    Deterministic JSON encoding.
    """

    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sign_dict(
    private_key,
    data: dict,
) -> str:
    """
    Sign a dictionary.
    """

    message = canonical_json(data)

    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )

    return base64.b64encode(signature).decode("utf-8")


def verify_dict(
    public_key,
    data: dict,
    signature_b64: str,
) -> bool:
    """
    Verify signature on dictionary.
    """

    try:
        signature = base64.b64decode(signature_b64)

        public_key.verify(
            signature,
            canonical_json(data),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )

        return True

    except Exception:
        return False


if __name__ == "__main__":

    private_key, public_key = (
        generate_rsa_keypair()
    )

    payload = {
        "delivery_id": "DELIVERY_001",
        "package_id": "PKG_001",
    }

    signature = sign_dict(
        private_key,
        payload,
    )

    print("Signature:")
    print(signature)

    result = verify_dict(
        public_key,
        payload,
        signature,
    )

    print("Valid:", result)
