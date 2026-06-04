"""
scripts/test_car_tpm_signature.py

Test real car TPM signing and public-key verification.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from common.protocol import make_signed_challenge_payload
from common.tpm_utils import (
    export_tpm_public_key,
    tpm_verify_signature,
)
from rpi5_car.tpm_vehicle import VehicleTPM


def main():
    car_id = "CAR_RPI5_001"

    tpm = VehicleTPM(
        car_id=car_id,
        require_real_tpm=True,
    )

    payload = make_signed_challenge_payload(
        holder_id=car_id,
        delivery_id="DELIVERY_TPM_TEST",
        car_id=car_id,
        package_id="PKG_TPM_TEST",
        phase="CAR_IDENTITY",
        nonce="TEST_NONCE_123",
    )

    signature = tpm.sign_vehicle_challenge(payload)

    public_key = export_tpm_public_key("car")

    valid = tpm_verify_signature(
        payload=payload,
        signature=signature,
        public_key=public_key,
    )

    print("TPM available:", tpm.is_available())
    print("Signature valid:", valid)

    if not valid:
        raise RuntimeError("Car TPM signature verification failed")

    print("=== CAR TPM SIGNATURE TEST PASS ===")


if __name__ == "__main__":
    main()
