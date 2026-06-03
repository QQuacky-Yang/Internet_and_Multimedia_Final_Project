"""
scripts/register_car.py

Register a car to the platform server.
"""

import argparse
import sys
from pathlib import Path

# Allow running as: python scripts/register_car.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rpi5_car.tpm_vehicle import VehicleTPM
from rpi5_car.platform_api import get_platform_public_key
from common.config import SERVER_URL

import requests


def register_car(
    car_id: str,
    description: str,
    require_real_tpm: bool = False,
):
    tpm = VehicleTPM(
        car_id=car_id,
        require_real_tpm=require_real_tpm,
    )

    car_pubkey = tpm.get_public_key()

    payload = {
        "car_id": car_id,
        "car_pubkey": car_pubkey,
        "description": description,
    }

    response = requests.post(
        f"{SERVER_URL}/register_car",
        json=payload,
        timeout=5,
    )

    if not response.ok:
        try:
            error = response.json()
        except Exception:
            error = {"detail": response.text}

        detail = error.get("detail", "")

        if response.status_code == 400 and "already exists" in detail:
            print(f"Car already registered: {car_id}")
            return {
                "status": "already_registered",
                "car_id": car_id,
                "detail": detail,
            }

        print("Request failed:")
        print("Status code:", response.status_code)
        print("Response:", error)

        response.raise_for_status()

    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Register RPi5 car to platform"
    )

    parser.add_argument(
        "--car-id",
        default="CAR_RPI5_001",
    )

    parser.add_argument(
        "--description",
        default="RPi5 autonomous delivery car",
    )

    parser.add_argument(
        "--require-real-tpm",
        action="store_true",
    )

    args = parser.parse_args()

    result = register_car(
        car_id=args.car_id,
        description=args.description,
        require_real_tpm=args.require_real_tpm,
    )

    print("Registered car:")
    print(result)


if __name__ == "__main__":
    main()