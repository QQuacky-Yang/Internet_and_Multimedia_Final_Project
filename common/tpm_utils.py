"""
common/tpm_utils.py

Shared TPM utilities.

Uses tpm2-tools when a real TPM is available.
Supports role-specific TPM key paths:
- car
- receiver
- sender

If TPM is unavailable, caller can fall back to simulation.
"""

import base64
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict


def canonical_payload(payload: Dict[str, Any]) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def get_tpm_dir(role: str) -> Path:
    return Path("data") / role / "tpm"


def get_tpm_key_context_path(role: str) -> Path:
    return get_tpm_dir(role) / f"{role}_key.ctx"


def get_tpm_public_key_path(role: str) -> Path:
    return get_tpm_dir(role) / f"{role}_public.pem"


def run_command(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=False,
    )


def tpm_available() -> bool:
    try:
        run_command(["tpm2_getrandom", "8"])
        return True
    except Exception:
        return False


def export_tpm_public_key(role: str) -> str:
    path = get_tpm_public_key_path(role)

    if not path.exists():
        return f"TPM_PUBLIC_KEY_PLACEHOLDER_{role}"

    return path.read_text(encoding="utf-8")


def tpm_key_ready(role: str) -> bool:
    return (
        get_tpm_key_context_path(role).exists()
        and get_tpm_public_key_path(role).exists()
    )


def tpm_sign_payload(
    role: str,
    payload: Dict[str, Any],
) -> str:
    key_path = get_tpm_key_context_path(role)

    if not key_path.exists():
        raise FileNotFoundError(
            f"TPM key context not found: {key_path}"
        )

    message = canonical_payload(payload)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        message_path = tmpdir_path / "message.bin"
        signature_path = tmpdir_path / "signature.bin"

        message_path.write_bytes(message)

        run_command(
            [
                "tpm2_sign",
                "-c",
                str(key_path),
                "-g",
                "sha256",
                "-o",
                str(signature_path),
                str(message_path),
            ]
        )

        signature = signature_path.read_bytes()

    return base64.b64encode(signature).decode("utf-8")


def tpm_verify_signature(
    payload: Dict[str, Any],
    signature: str,
    public_key: str,
) -> bool:
    raise NotImplementedError(
        "TPM signature verification is not implemented yet"
    )


if __name__ == "__main__":
    print("TPM available:", tpm_available())

    for role in ["car", "receiver", "sender"]:
        print(f"\nRole: {role}")
        print("Key ready:", tpm_key_ready(role))
        print("Public key:")
        print(export_tpm_public_key(role))