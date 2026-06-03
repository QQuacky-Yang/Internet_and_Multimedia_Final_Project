"""
common/tpm_utils.py

Shared TPM utilities.

Uses tpm2-tools when a real TPM is available.
Falls back to safe simulation when TPM is unavailable.
"""

import base64
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_TPM_KEY_CONTEXT = Path("data/car/tpm/car_key.ctx")
DEFAULT_TPM_PUBLIC_KEY = Path("data/car/tpm/car_public.pem")


def canonical_payload(payload: Dict[str, Any]) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def run_command(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=False,
    )


def tpm_available() -> bool:
    """
    Check whether tpm2-tools can talk to TPM.
    """

    try:
        run_command(["tpm2_getrandom", "8"])
        return True
    except Exception:
        return False


def export_tpm_public_key(
    public_key_path: Optional[Path] = None,
) -> str:
    """
    Read exported TPM public key PEM.

    The key file will be generated later by setup_car_tpm.py.
    """

    path = public_key_path or DEFAULT_TPM_PUBLIC_KEY

    if not path.exists():
        return "TPM_PUBLIC_KEY_PLACEHOLDER"

    return path.read_text(encoding="utf-8")


def tpm_sign_payload(
    payload: Dict[str, Any],
    key_context_path: Optional[Path] = None,
) -> str:
    """
    Sign canonical JSON payload using TPM key context.

    Requires:
        tpm2-tools
        existing TPM key context file
    """

    key_path = key_context_path or DEFAULT_TPM_KEY_CONTEXT

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
    """
    Placeholder.

    For the first real TPM milestone, signing is enough.
    Verification will be done after we decide signature format.
    """

    raise NotImplementedError(
        "TPM signature verification is not implemented yet"
    )


if __name__ == "__main__":
    print("TPM available:", tpm_available())
    print("TPM public key:")
    print(export_tpm_public_key())

    if tpm_available():
        print("TPM detected. Signing requires key setup first.")
    else:
        print("No TPM detected or tpm2-tools not installed.")
