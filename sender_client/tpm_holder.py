"""
sender_client/tpm_holder.py

Sender TPM identity manager.

Sender TPM is optional.
If no real TPM/key exists, use simulation mode.
"""

from typing import Any, Dict

from common.tpm_utils import (
    tpm_available,
    tpm_key_ready,
    export_tpm_public_key,
    tpm_sign_payload,
)


class SenderTPM:

    def __init__(
        self,
        sender_id: str,
        require_real_tpm: bool = False,
    ):
        self.sender_id = sender_id
        self.require_real_tpm = require_real_tpm

        self.real_tpm_available = (
            tpm_available()
            and tpm_key_ready("sender")
        )

        if self.require_real_tpm and not self.real_tpm_available:
            raise RuntimeError(
                "Real sender TPM is required, but TPM is unavailable "
                "or sender TPM key has not been set up."
            )

    def is_available(self) -> bool:
        return self.real_tpm_available

    def is_simulation(self) -> bool:
        return not self.real_tpm_available

    def signature_type(self) -> str:
        if self.real_tpm_available:
            return "TPM2_RSA_SHA256"

        return "SIMULATED"

    def get_public_key(self) -> str:
        if self.real_tpm_available:
            return export_tpm_public_key("sender")

        return (
            f"SIMULATED_SENDER_PUBLIC_KEY_"
            f"{self.sender_id}"
        )

    def sign_payload(
        self,
        payload: Dict[str, Any],
    ) -> str:
        if self.real_tpm_available:
            return tpm_sign_payload(
                "sender",
                payload,
            )

        return (
            f"SIMULATED_SIGNATURE_"
            f"{self.sender_id}_"
            f"{payload.get('nonce', '')}"
        )

    def sign_nonce(
        self,
        nonce: str,
    ) -> str:
        """
        Backward-compatible helper.
        Prefer sign_payload() for new code.
        """

        return self.sign_payload(
            {
                "sender_id": self.sender_id,
                "nonce": nonce,
            }
        )

    def get_sender_identity(self) -> dict:
        return {
            "sender_id": self.sender_id,
            "public_key": self.get_public_key(),
            "simulation": self.is_simulation(),
            "tpm_available": self.is_available(),
            "signature_type": self.signature_type(),
        }


if __name__ == "__main__":
    tpm = SenderTPM("sender_001")

    payload = {
        "holder_id": "sender_001",
        "delivery_id": "DELIVERY_001",
        "car_id": "CAR_RPI5_001",
        "package_id": "PKG_001",
        "phase": "PICKUP",
        "nonce": "test_nonce",
    }

    print("TPM Available:")
    print(tpm.is_available())

    print("Simulation:")
    print(tpm.is_simulation())

    print("Public Key:")
    print(tpm.get_public_key())

    print("Signature Type:")
    print(tpm.signature_type())

    print("Signature:")
    print(tpm.sign_payload(payload))

    print("Identity:")
    print(tpm.get_sender_identity())