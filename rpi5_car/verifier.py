"""
rpi5_car/verifier.py

VC verifier.

Current:
    Structural verification

Future:
    Signature verification
    TPM verification
    Revocation checking
"""

from common.vc_schema import (
    get_delivery_id,
    get_package_id,
    get_car_id,
    is_sender_pickup_vc,
    is_receiver_delivery_vc,
)

from common.errors import (
    VCSystemError,
    ErrorCode,
)


class VCVerifier:

    @staticmethod
    def verify_sender_pickup(
        vc: dict,
        delivery_id: str,
        package_id: str,
        car_id: str,
        nonce_valid: bool,
    ) -> bool:

        if not is_sender_pickup_vc(vc):
            raise VCSystemError(
                ErrorCode.INVALID_VC,
                "Not a sender pickup VC",
            )

        if get_delivery_id(vc) != delivery_id:
            raise VCSystemError(
                ErrorCode.DELIVERY_MISMATCH,
                "Delivery ID mismatch",
            )

        if get_package_id(vc) != package_id:
            raise VCSystemError(
                ErrorCode.PACKAGE_MISMATCH,
                "Package ID mismatch",
            )

        if get_car_id(vc) != car_id:
            raise VCSystemError(
                ErrorCode.CAR_MISMATCH,
                "Car ID mismatch",
            )

        if not nonce_valid:
            raise VCSystemError(
                ErrorCode.NONCE_MISMATCH,
                "Nonce mismatch",
            )

        return True

    @staticmethod
    def verify_receiver_delivery(
        vc: dict,
        delivery_id: str,
        package_id: str,
        car_id: str,
        nonce_valid: bool,
    ) -> bool:

        if not is_receiver_delivery_vc(vc):
            raise VCSystemError(
                ErrorCode.INVALID_VC,
                "Not a receiver delivery VC",
            )

        if get_delivery_id(vc) != delivery_id:
            raise VCSystemError(
                ErrorCode.DELIVERY_MISMATCH,
                "Delivery ID mismatch",
            )

        if get_package_id(vc) != package_id:
            raise VCSystemError(
                ErrorCode.PACKAGE_MISMATCH,
                "Package ID mismatch",
            )

        if get_car_id(vc) != car_id:
            raise VCSystemError(
                ErrorCode.CAR_MISMATCH,
                "Car ID mismatch",
            )

        if not nonce_valid:
            raise VCSystemError(
                ErrorCode.NONCE_MISMATCH,
                "Nonce mismatch",
            )

        return True


if __name__ == "__main__":

    sender_vc = {
        "type": [
            "VerifiableCredential",
            "SenderPickupCredential",
        ],
        "credentialSubject": {
            "delivery_id": "DELIVERY_001",
            "package_id": "PKG_001",
            "car_id": "CAR_RPI5_001",
            "action": "PICKUP_PACKAGE",
        },
    }

    try:

        result = (
            VCVerifier.verify_sender_pickup(
                vc=sender_vc,
                delivery_id="DELIVERY_001",
                package_id="PKG_001",
                car_id="CAR_RPI5_001",
                nonce_valid=True,
            )
        )

        print("Verified:", result)

    except VCSystemError as e:

        print("Verification failed:")
        print(e)
