"""
receiver_client/tpm_holder.py

Receiver TPM identity manager.

Receiver TPM is optional.
If no real TPM/key exists, use simulation mode.
"""

from typing import Any, Dict

from common.tpm_utils import (
    tpm_available,
    tpm_key_ready,
    export_tpm_public_key,
    tpm_sign_payload,
)


class ReceiverTPM:

    def __init__(
        self,
        receiver_id: str,
        require_real_tpm: bool = False,
    ):
        self.receiver_id = receiver_id
        self.require_real_tpm = require_real_tpm

        self.real_tpm_available = (
            tpm_available()
            and tpm_key_ready("receiver")
        )

        if self.require_real_tpm and not self.real_tpm_available:
            raise RuntimeError(
                "Real receiver TPM is required, but TPM is unavailable "
                "or receiver TPM key has not been set up."
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
            return export_tpm_public_key("receiver")

        return (
            f"SIMULATED_RECEIVER_PUBLIC_KEY_"
            f"{self.receiver_id}"
        )

    def sign_payload(
        self,
        payload: Dict[str, Any],
    ) -> str:
        if self.real_tpm_available:
            return tpm_sign_payload(
                "receiver",
                payload,
            )

        return (
            f"SIMULATED_SIGNATURE_"
            f"{self.receiver_id}_"
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
                "receiver_id": self.receiver_id,
                "nonce": nonce,
            }
        )

    def get_receiver_identity(self) -> dict:
        return {
            "receiver_id": self.receiver_id,
            "public_key": self.get_public_key(),
            "simulation": self.is_simulation(),
            "tpm_available": self.is_available(),
            "signature_type": self.signature_type(),
        }


if __name__ == "__main__":
    tpm = ReceiverTPM("receiver_001")

    payload = {
        "holder_id": "receiver_001",
        "delivery_id": "DELIVERY_001",
        "car_id": "CAR_RPI5_001",
        "package_id": "PKG_001",
        "phase": "DELIVERY",
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
    print(tpm.get_receiver_identity())