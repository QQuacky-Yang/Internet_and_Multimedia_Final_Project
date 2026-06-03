"""
rpi5_car/tpm_vehicle.py

Car TPM identity manager.

RPi5 car:
    Prefer real TPM.

Development laptop:
    Fall back to simulation.
"""

from typing import Any, Dict

from common.tpm_utils import (
    tpm_available,
    tpm_key_ready,
    export_tpm_public_key,
    tpm_sign_payload,
)


class VehicleTPM:

    def __init__(
        self,
        car_id: str,
        require_real_tpm: bool = False,
    ):
        self.car_id = car_id
        self.require_real_tpm = require_real_tpm
        self.real_tpm_available = (
            tpm_available()
            and tpm_key_ready("car")
        )

        if self.require_real_tpm and not self.real_tpm_available:
            raise RuntimeError(
                "Real car TPM is required, but TPM is unavailable "
                "or car TPM key has not been set up."
            )

    def is_available(self) -> bool:
        return self.real_tpm_available

    def is_simulation(self) -> bool:
        return not self.real_tpm_available

    def get_public_key(self) -> str:
        if self.real_tpm_available:
            return export_tpm_public_key("car")

        return f"SIMULATED_TPM_PUBLIC_KEY_FOR_{self.car_id}"

    def sign_vehicle_challenge(
        self,
        challenge: Dict[str, Any],
    ) -> str:
        if self.real_tpm_available:
            return tpm_sign_payload(
                "car",
                challenge,
            )

        return (
            f"SIMULATED_SIGNATURE_BY_"
            f"{self.car_id}_"
            f"{challenge.get('nonce', '')}"
        )

    def attest_vehicle_state(self) -> dict:
        if self.real_tpm_available:
            return {
                "car_id": self.car_id,
                "mode": "REAL_TPM",
                "tpm_available": True,
                "key_ready": True,
                "attested": False,
                "note": "PCR quote attestation not implemented yet",
            }

        return {
            "car_id": self.car_id,
            "mode": "SIMULATION",
            "tpm_available": False,
            "key_ready": False,
            "attested": False,
        }


if __name__ == "__main__":
    tpm = VehicleTPM(
        "CAR_RPI5_001",
        require_real_tpm=False,
    )

    print("TPM available:")
    print(tpm.is_available())

    print("Simulation:")
    print(tpm.is_simulation())

    print("Public key:")
    print(tpm.get_public_key())

    print("Signature:")
    print(
        tpm.sign_vehicle_challenge(
            {"nonce": "test-nonce"}
        )
    )

    print("Attestation:")
    print(tpm.attest_vehicle_state())