"""
rpi5_car/tpm_vehicle.py

Car TPM identity manager.

Current:
    Simulation mode

Future:
    Real TPM 2.0 key generation, signing, and attestation.
"""

from common.tpm_utils import (
    tpm_available,
    export_tpm_public_key,
)


class VehicleTPM:
    def __init__(self, car_id: str):
        self.car_id = car_id
        self.simulation = not tpm_available()

    def is_available(self) -> bool:
        return not self.simulation

    def get_public_key(self) -> str:
        if self.simulation:
            return f"SIMULATED_TPM_PUBLIC_KEY_FOR_{self.car_id}"

        return export_tpm_public_key()

    def sign_vehicle_challenge(self, challenge: dict) -> str:
        if self.simulation:
            return f"SIMULATED_SIGNATURE_BY_{self.car_id}"

        raise NotImplementedError(
            "Real car TPM signing is not implemented yet"
        )

    def attest_vehicle_state(self) -> dict:
        if self.simulation:
            return {
                "car_id": self.car_id,
                "mode": "SIMULATION",
                "attested": False,
            }

        raise NotImplementedError(
            "Real TPM attestation is not implemented yet"
        )


if __name__ == "__main__":
    tpm = VehicleTPM("CAR_RPI5_001")

    print("TPM available:")
    print(tpm.is_available())

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
