"""
receiver_client/tpm_holder.py

Receiver TPM identity manager.

Current:
    Software simulation

Future:
    Real TPM 2.0 integration.
"""

from common.tpm_utils import (
    tpm_available,
    export_tpm_public_key,
)


class ReceiverTPM:

    def __init__(
        self,
        receiver_id: str,
    ):
        self.receiver_id = receiver_id

        self.simulation = (
            not tpm_available()
        )

    def is_available(
        self,
    ) -> bool:

        return (
            not self.simulation
        )

    def get_public_key(
        self,
    ) -> str:

        if self.simulation:

            return (
                f"SIMULATED_RECEIVER_PUBLIC_KEY_"
                f"{self.receiver_id}"
            )

        return export_tpm_public_key()

    def sign_nonce(
        self,
        nonce: str,
    ) -> str:

        if self.simulation:

            return (
                f"SIMULATED_SIGNATURE_"
                f"{self.receiver_id}_"
                f"{nonce}"
            )

        raise NotImplementedError(
            "Real TPM signing not implemented yet"
        )

    def get_receiver_identity(
        self,
    ) -> dict:

        return {
            "receiver_id": self.receiver_id,
            "public_key":
                self.get_public_key(),
            "simulation":
                self.simulation,
        }


if __name__ == "__main__":

    tpm = ReceiverTPM(
        "receiver_001"
    )

    print(
        "TPM Available:"
    )

    print(
        tpm.is_available()
    )

    print(
        "Public Key:"
    )

    print(
        tpm.get_public_key()
    )

    print(
        "Signature:"
    )

    print(
        tpm.sign_nonce(
            "test_nonce"
        )
    )

    print(
        "Identity:"
    )

    print(
        tpm.get_receiver_identity()
    )
