"""
scripts/setup_sender_tpm.py

Create TPM signing key for sender device.

Sender TPM is optional.
If no TPM exists, sender_client will use simulation mode.

Requires:
    sudo apt install tpm2-tools

Output:
    data/sender/tpm/sender_primary.ctx
    data/sender/tpm/sender_key.priv
    data/sender/tpm/sender_key.pub
    data/sender/tpm/sender_key.ctx
    data/sender/tpm/sender_public.pem
"""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TPM_DIR = PROJECT_ROOT / "data" / "sender" / "tpm"

PRIMARY_CTX = TPM_DIR / "sender_primary.ctx"
KEY_PRIV = TPM_DIR / "sender_key.priv"
KEY_PUB = TPM_DIR / "sender_key.pub"
KEY_CTX = TPM_DIR / "sender_key.ctx"
PUBLIC_PEM = TPM_DIR / "sender_public.pem"


def run(cmd: list[str]) -> None:
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def main():
    TPM_DIR.mkdir(parents=True, exist_ok=True)

    try:
        run(["tpm2_getrandom", "8"])
    except Exception:
        print("TPM not available or tpm2-tools not installed.")
        print("Sender TPM setup skipped.")
        sys.exit(0)

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

    print("Sender TPM key setup complete.")
    print("Public key:", PUBLIC_PEM)
    print("Key context:", KEY_CTX)


if __name__ == "__main__":
    main()
