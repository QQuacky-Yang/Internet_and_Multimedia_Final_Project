"""
rpi5_car/verifier.py

VC verifier.

Current:
    Structural VC verification
    Challenge binding verification
    Simulated signature verification

Future:
    Real TPM / software public-key signature verification
    VC signature verification
    Revocation checking
"""

from common.vc_schema import (
    get_delivery_id,
    get_package_id,
    get_car_id,
    is_sender_pickup_vc,
    is_receiver_delivery_vc,
)

from common.protocol import (
    validate_presentation_message_v2,
    make_signed_challenge_payload,
)

from common.errors import (
    VCSystemError,
    ErrorCode,
)


class VCVerifier:

    @staticmethod
    def _verify_challenge_binding(
        challenge: dict,
        delivery_id: str,
        package_id: str,
        car_id: str,
        expected_phase: str,
    ) -> None:

        if challenge.get("delivery_id") != delivery_id:
            raise VCSystemError(
                ErrorCode.DELIVERY_MISMATCH,
                "Challenge delivery ID mismatch",
            )

        if challenge.get("package_id") != package_id:
            raise VCSystemError(
                ErrorCode.PACKAGE_MISMATCH,
                "Challenge package ID mismatch",
            )

        if challenge.get("car_id") != car_id:
            raise VCSystemError(
                ErrorCode.CAR_MISMATCH,
                "Challenge car ID mismatch",
            )

        if challenge.get("phase") != expected_phase:
            raise VCSystemError(
                ErrorCode.INVALID_VC,
                "Challenge phase mismatch",
            )

    @staticmethod
    def _verify_simulated_signature(
        holder_id: str,
        nonce: str,
        signature: str,
    ) -> bool:

        expected = (
            f"SIMULATED_SIGNATURE_"
            f"{holder_id}_"
            f"{nonce}"
        )

        return signature == expected

    @staticmethod
    def verify_sender_pickup_presentation(
        presentation: dict,
        delivery_id: str,
        package_id: str,
        car_id: str,
    ) -> bool:

        if not validate_presentation_message_v2(presentation):
            raise VCSystemError(
                ErrorCode.INVALID_VC,
                "Invalid presentation message",
            )

        holder_id = presentation["holder_id"]
        vc = presentation["vc"]
        challenge = presentation["challenge"]
        signature = presentation["signature"]
        signature_type = presentation["signature_type"]

        if not is_sender_pickup_vc(vc):
            raise VCSystemError(
                ErrorCode.INVALID_VC,
                "Not a sender pickup VC",
            )

        if get_delivery_id(vc) != delivery_id:
            raise VCSystemError(
                ErrorCode.DELIVERY_MISMATCH,
                "VC delivery ID mismatch",
            )

        if get_package_id(vc) != package_id:
            raise VCSystemError(
                ErrorCode.PACKAGE_MISMATCH,
                "VC package ID mismatch",
            )

        if get_car_id(vc) != car_id:
            raise VCSystemError(
                ErrorCode.CAR_MISMATCH,
                "VC car ID mismatch",
            )

        VCVerifier._verify_challenge_binding(
            challenge=challenge,
            delivery_id=delivery_id,
            package_id=package_id,
            car_id=car_id,
            expected_phase="PICKUP",
        )

        make_signed_challenge_payload(
            holder_id=holder_id,
            delivery_id=delivery_id,
            car_id=car_id,
            package_id=package_id,
            phase="PICKUP",
            nonce=challenge["nonce"],
        )

        if signature_type == "SIMULATED":
            if not VCVerifier._verify_simulated_signature(
                holder_id,
                challenge["nonce"],
                signature,
            ):
                raise VCSystemError(
                    ErrorCode.INVALID_SIGNATURE,
                    "Simulated sender signature invalid",
                )

        elif signature_type == "TPM2_RSA_SHA256":
            raise NotImplementedError(
                "Real TPM signature verification not implemented yet"
            )

        else:
            raise VCSystemError(
                ErrorCode.INVALID_SIGNATURE,
                f"Unsupported signature type: {signature_type}",
            )

        return True

    @staticmethod
    def verify_receiver_delivery_presentation(
        presentation: dict,
        delivery_id: str,
        package_id: str,
        car_id: str,
    ) -> bool:

        if not validate_presentation_message_v2(presentation):
            raise VCSystemError(
                ErrorCode.INVALID_VC,
                "Invalid presentation message",
            )

        holder_id = presentation["holder_id"]
        vc = presentation["vc"]
        challenge = presentation["challenge"]
        signature = presentation["signature"]
        signature_type = presentation["signature_type"]

        if not is_receiver_delivery_vc(vc):
            raise VCSystemError(
                ErrorCode.INVALID_VC,
                "Not a receiver delivery VC",
            )

        if get_delivery_id(vc) != delivery_id:
            raise VCSystemError(
                ErrorCode.DELIVERY_MISMATCH,
                "VC delivery ID mismatch",
            )

        if get_package_id(vc) != package_id:
            raise VCSystemError(
                ErrorCode.PACKAGE_MISMATCH,
                "VC package ID mismatch",
            )

        if get_car_id(vc) != car_id:
            raise VCSystemError(
                ErrorCode.CAR_MISMATCH,
                "VC car ID mismatch",
            )

        VCVerifier._verify_challenge_binding(
            challenge=challenge,
            delivery_id=delivery_id,
            package_id=package_id,
            car_id=car_id,
            expected_phase="DELIVERY",
        )

        make_signed_challenge_payload(
            holder_id=holder_id,
            delivery_id=delivery_id,
            car_id=car_id,
            package_id=package_id,
            phase="DELIVERY",
            nonce=challenge["nonce"],
        )

        if signature_type == "SIMULATED":
            if not VCVerifier._verify_simulated_signature(
                holder_id,
                challenge["nonce"],
                signature,
            ):
                raise VCSystemError(
                    ErrorCode.INVALID_SIGNATURE,
                    "Simulated receiver signature invalid",
                )

        elif signature_type == "TPM2_RSA_SHA256":
            raise NotImplementedError(
                "Real TPM signature verification not implemented yet"
            )

        else:
            raise VCSystemError(
                ErrorCode.INVALID_SIGNATURE,
                f"Unsupported signature type: {signature_type}",
            )

        return True

    # Backward compatibility with older test code
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

    challenge = {
        "message_type": "CHALLENGE",
        "delivery_id": "DELIVERY_001",
        "car_id": "CAR_RPI5_001",
        "package_id": "PKG_001",
        "phase": "PICKUP",
        "nonce": "TEST_NONCE_123",
        "created_at": "2026-06-04T00:00:00Z",
    }

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

    presentation = {
        "message_type": "VC_PRESENTATION",
        "holder_id": "sender_001",
        "vc": sender_vc,
        "challenge": challenge,
        "signature": "SIMULATED_SIGNATURE_sender_001_TEST_NONCE_123",
        "signature_type": "SIMULATED",
        "created_at": "2026-06-04T00:00:00Z",
    }

    print(
        VCVerifier.verify_sender_pickup_presentation(
            presentation=presentation,
            delivery_id="DELIVERY_001",
            package_id="PKG_001",
            car_id="CAR_RPI5_001",
        )
    )