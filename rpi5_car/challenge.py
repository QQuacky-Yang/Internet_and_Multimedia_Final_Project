"""
rpi5_car/challenge.py

Challenge manager.

Creates and tracks active challenges.
"""

from typing import Dict, Optional

from common.protocol import (
    make_challenge_message,
)


class ChallengeManager:

    def __init__(self):
        self.active_challenges: Dict[
            str,
            dict,
        ] = {}

    def create_challenge(
        self,
        delivery_id: str,
        car_id: str,
        package_id: str,
        phase: str,
    ) -> dict:

        challenge = make_challenge_message(
            delivery_id=delivery_id,
            car_id=car_id,
            package_id=package_id,
            phase=phase,
        )

        self.active_challenges[
            delivery_id
        ] = challenge

        return challenge

    def get_challenge(
        self,
        delivery_id: str,
    ) -> Optional[dict]:

        return self.active_challenges.get(
            delivery_id
        )

    def verify_nonce(
        self,
        delivery_id: str,
        nonce: str,
    ) -> bool:

        challenge = self.get_challenge(
            delivery_id
        )

        if challenge is None:
            return False

        return (
            challenge["nonce"]
            == nonce
        )

    def clear_challenge(
        self,
        delivery_id: str,
    ) -> None:

        self.active_challenges.pop(
            delivery_id,
            None,
        )


if __name__ == "__main__":

    manager = ChallengeManager()

    challenge = manager.create_challenge(
        delivery_id="DELIVERY_001",
        car_id="CAR_RPI5_001",
        package_id="PKG_001",
        phase="PICKUP",
    )

    print("Challenge:")
    print(challenge)

    print(
        "Nonce valid:",
        manager.verify_nonce(
            "DELIVERY_001",
            challenge["nonce"],
        ),
    )

    print(
        "Nonce invalid:",
        manager.verify_nonce(
            "DELIVERY_001",
            "bad_nonce",
        ),
    )

    manager.clear_challenge(
        "DELIVERY_001"
    )

    print(
        "After clear:",
        manager.get_challenge(
            "DELIVERY_001"
        ),
    )
