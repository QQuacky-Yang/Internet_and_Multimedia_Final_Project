"""
receiver_client/face_auth.py

Receiver face authentication.

Current:
    Simulation mode

Future:
    Face recognition using camera.
"""

from datetime import datetime


class ReceiverFaceAuth:

    def __init__(
        self,
        simulation: bool = True,
    ):
        self.simulation = simulation

    def authenticate(
        self,
    ) -> bool:

        if self.simulation:

            print(
                "[SIM] Receiver face verified"
            )

            return True

        raise NotImplementedError(
            "Real face authentication "
            "not implemented yet"
        )

    def authentication_report(
        self,
    ) -> dict:

        result = self.authenticate()

        return {
            "timestamp":
                datetime.utcnow().isoformat(),
            "face_verified":
                result,
            "simulation":
                self.simulation,
        }


if __name__ == "__main__":

    auth = ReceiverFaceAuth()

    report = (
        auth.authentication_report()
    )

    print(
        "Authentication Report:"
    )

    print(report)
