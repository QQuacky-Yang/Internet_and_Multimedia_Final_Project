"""
sender_client/face_auth.py

Sender-side face authentication placeholder.

Current:
    Always allows authentication in simulation mode.

Future:
    Connect to real face-recognition module if sender biometric
    authentication is required.
"""


class SenderFaceAuth:
    def __init__(self, simulation: bool = True):
        self.simulation = simulation

    def authenticate(self) -> bool:
        if self.simulation:
            print("[SIM] Sender face authentication passed")
            return True

        raise NotImplementedError(
            "Real sender face authentication is not implemented yet"
        )


if __name__ == "__main__":
    auth = SenderFaceAuth(simulation=True)

    result = auth.authenticate()

    print("Authenticated:", result)
