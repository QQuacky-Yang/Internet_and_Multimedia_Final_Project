"""
common/errors.py

Shared error codes and custom exceptions.
"""

from enum import Enum


class ErrorCode(str, Enum):
    INVALID_VC = "INVALID_VC"
    EXPIRED_VC = "EXPIRED_VC"
    REVOKED_VC = "REVOKED_VC"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    NONCE_MISMATCH = "NONCE_MISMATCH"
    DELIVERY_MISMATCH = "DELIVERY_MISMATCH"
    PACKAGE_MISMATCH = "PACKAGE_MISMATCH"
    CAR_MISMATCH = "CAR_MISMATCH"
    HOLDER_MISMATCH = "HOLDER_MISMATCH"
    TPM_SIGNING_FAILED = "TPM_SIGNING_FAILED"
    FACE_AUTH_FAILED = "FACE_AUTH_FAILED"
    NETWORK_ERROR = "NETWORK_ERROR"


class VCSystemError(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code.value}: {message}")


if __name__ == "__main__":
    try:
        raise VCSystemError(
            ErrorCode.INVALID_SIGNATURE,
            "Signature verification failed",
        )
    except VCSystemError as e:
        print("Code:", e.code)
        print("Message:", e.message)
        print("String:", str(e))
