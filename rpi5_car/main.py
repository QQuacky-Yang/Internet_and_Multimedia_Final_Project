"""
rpi5_car/main.py

Main car controller.

Current:
    Software simulation

Future:
    Real RPi5 operation.
"""

from rpi5_car.platform_api import (
    get_manifest,
)

from rpi5_car.manifest import (
    list_pending_pickups,
)

from rpi5_car.car_state import (
    DeliveryCarState,
)

from rpi5_car.challenge import (
    ChallengeManager,
)

from rpi5_car.verifier import (
    VCVerifier,
)

from rpi5_car.gpio_lock import (
    LockController,
)

from rpi5_car.receiver_session import (
    simulate_receive_presentation,
)

from common.vc_schema import (
    get_delivery_id,
    get_package_id,
    get_car_id,
)


class DeliveryCar:

    def __init__(self, car_id: str):

        self.car_id = car_id

        self.state = DeliveryCarState()

        self.challenge_manager = (
            ChallengeManager()
        )

        self.lock = LockController(
            simulation=True
        )

    def load_manifest(self):

        manifest = get_manifest(
            self.car_id
        )

        return manifest

    def run_demo(self):

        print(
            f"=== Car {self.car_id} Demo ==="
        )

        manifest = self.load_manifest()

        pending = list_pending_pickups(
            manifest
        )

        if len(pending) == 0:

            print(
                "No pending deliveries."
            )

            return

        delivery = pending[0]

        delivery_id = (
            delivery["delivery_id"]
        )

        package_id = (
            delivery["package_id"]
        )

        print(
            f"Selected delivery: "
            f"{delivery_id}"
        )

        self.state.assign_delivery(
            delivery_id,
            package_id,
        )

        challenge = (
            self.challenge_manager
            .create_challenge(
                delivery_id=delivery_id,
                car_id=self.car_id,
                package_id=package_id,
                phase="PICKUP",
            )
        )

        print("Challenge created.")

        #
        # Simulation only:
        #
        test_vc = {
            "type": [
                "VerifiableCredential",
                "SenderPickupCredential",
            ],
            "credentialSubject": {
                "delivery_id": delivery_id,
                "package_id": package_id,
                "car_id": self.car_id,
                "action": "PICKUP_PACKAGE",
            },
        }

        presentation = (
            simulate_receive_presentation(
                delivery_id=delivery_id,
                holder_id="sender_001",
                vc=test_vc,
                nonce=challenge["nonce"],
            )
        )

        nonce_valid = (
            self.challenge_manager
            .verify_nonce(
                delivery_id,
                presentation["nonce"],
            )
        )

        result = (
            VCVerifier
            .verify_sender_pickup(
                vc=presentation["vc"],
                delivery_id=delivery_id,
                package_id=package_id,
                car_id=self.car_id,
                nonce_valid=nonce_valid,
            )
        )

        if result:

            print(
                "Pickup verified."
            )

            self.lock.unlock(
                seconds=3
            )

            self.state.mark_picked_up()

            print(
                self.state.to_dict()
            )


if __name__ == "__main__":

    car = DeliveryCar(
        "CAR_RPI5_001"
    )

    car.run_demo()
