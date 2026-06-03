"""
common/tpm_utils.py

TPM helper interface.

Current:
    Placeholder / software-compatible interface

Future:
    Real TPM 2.0 calls using tpm2-tools or TPM Python bindings.
"""

from typing import Dict, Any


def tpm_available() -> bool:
    """
    Check whether TPM is available.

    MVP:
        Always False.

    Future:
        Check /dev/tpm0 or call tpm2_getrandom.
    """

    return False


def export_tpm_public_key() -> str:
    """
    Export TPM public key.

    MVP:
        Placeholder.

    Future:
        Return real TPM public key PEM.
    """

    return "TPM_PUBLIC_KEY_PLACEHOLDER"


def tpm_sign_payload(payload: Dict[str, Any]) -> str:
    """
    Ask TPM to sign a payload.

    MVP:
        Placeholder.

    Future:
        Canonicalize payload and call TPM2_Sign.
    """

    raise NotImplementedError(
        "Real TPM signing is not implemented yet"
    )


def tpm_verify_signature(
    payload: Dict[str, Any],
    signature: str,
    public_key: str,
) -> bool:
    """
    Verify TPM signature.

    MVP:
        Placeholder.

    Future:
        Use normal public-key verification.
    """

    raise NotImplementedError(
        "Real TPM signature verification is not implemented yet"
    )


if __name__ == "__main__":
    print("TPM available:", tpm_available())
    print("TPM public key:", export_tpm_public_key())
