"""
scripts/setup_car_tpm.py

Create TPM signing key for the RPi5 car.

Requires:
    sudo apt install tpm2-tools

Output:
    data/car/tpm/car_primary.ctx
    data/car/tpm/car_key.priv
    data/car/tpm/car_key.pub
    data/car/tpm/car_key.ctx
    data/car/tpm/car_public.pem
"""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TPM_DIR = PROJECT_ROOT / "data" / "car" / "tpm"

PRIMARY_CTX = TPM_DIR / "car_primary.ctx"
KEY_PRIV = TPM_DIR / "car_key.priv"
KEY_PUB = TPM_DIR / "car_key.pub"
KEY_CTX = TPM_DIR / "car_key.ctx"
PUBLIC_PEM = TPM_DIR / "car_public.pem"


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    TPM_DIR.mkdir(parents=True, exist_ok=True)

    try:
        run(["tpm2_getrandom", "8"])
    except Exception:
        print("TPM not available or tpm2-tools not installed.")
        sys.exit(1)

    run([
        "tpm2_createprimary",
        "-C", "o",
        "-G", "rsa",
        "-c", str(PRIMARY_CTX),
    ])

    run([
        "tpm2_create",
        "-C", str(PRIMARY_CTX),
        "-G", "rsa",
        "-u", str(KEY_PUB),
        "-r", str(KEY_PRIV),
    ])

    run([
        "tpm2_load",
        "-C", str(PRIMARY_CTX),
        "-u", str(KEY_PUB),
        "-r", str(KEY_PRIV),
        "-c", str(KEY_CTX),
    ])

    run([
        "tpm2_readpublic",
        "-c", str(KEY_CTX),
        "-f", "pem",
        "-o", str(PUBLIC_PEM),
    ])

    print("Car TPM key setup complete.")
    print("Public key:", PUBLIC_PEM)
    print("Key context:", KEY_CTX)


if __name__ == "__main__":
    main()
