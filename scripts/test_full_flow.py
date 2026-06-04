"""
scripts/test_full_flow.py

End-to-end software simulation test.

Requires platform server running:
uvicorn platform_server.app:app --host 127.0.0.1 --port 8000
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.register_sender import register_sender
from scripts.register_receiver import register_receiver
from scripts.register_car import register_car
from scripts.create_delivery import create_delivery

from sender_client.wallet import SenderWallet
from receiver_client.wallet import ReceiverWallet

from sender_client.platform_api import get_sender_pickup_vc
from receiver_client.platform_api import get_receiver_delivery_vc

from sender_client.car_session import SenderCarSession
from receiver_client.car_session import ReceiverCarSession

from rpi5_car.challenge import ChallengeManager
from rpi5_car.verifier import VCVerifier
from rpi5_car.gpio_lock import LockController

from datetime import datetime

RUN_ID = datetime.now().strftime("%Y%m%d%H%M%S")
DELIVERY_ID = f"DELIVERY_FULL_TEST_{RUN_ID}"
PACKAGE_ID = f"PKG_FULL_TEST_{RUN_ID}"
SENDER_ID = "sender_full_test_001"
RECEIVER_ID = "receiver_full_test_001"
CAR_ID = "CAR_RPI5_FULL_TEST_001"


def main():
    print("=== Register actors ===")

    register_sender(
        sender_id=SENDER_ID,
        display_name="Full Test Sender",
    )

    register_receiver(
        receiver_id=RECEIVER_ID,
        display_name="Full Test Receiver",
    )

    register_car(
        car_id=CAR_ID,
        description="Full test RPi5 car",
    )

    print("=== Create delivery ===")

    delivery = create_delivery(
        delivery_id=DELIVERY_ID,
        sender_id=SENDER_ID,
        receiver_id=RECEIVER_ID,
        package_id=PACKAGE_ID,
        car_id=CAR_ID,
    )

    print("Delivery created:")
    print(delivery["delivery_id"])

    print("=== Download VCs ===")

    sender_vc_response = get_sender_pickup_vc(
        DELIVERY_ID
    )

    receiver_vc_response = get_receiver_delivery_vc(
        DELIVERY_ID
    )

    sender_vc = sender_vc_response["sender_pickup_vc"]
    receiver_vc = receiver_vc_response["receiver_delivery_vc"]

    SenderWallet().add_vc(
        DELIVERY_ID,
        sender_vc,
    )

    ReceiverWallet().add_vc(
        DELIVERY_ID,
        receiver_vc,
    )

    challenge_manager = ChallengeManager()
    lock = LockController(simulation=True)

    print("=== Sender pickup verification ===")

    pickup_challenge = challenge_manager.create_challenge(
        delivery_id=DELIVERY_ID,
        car_id=CAR_ID,
        package_id=PACKAGE_ID,
        phase="PICKUP",
    )

    sender_presentation = SenderCarSession(
        SENDER_ID
    ).create_presentation(
        DELIVERY_ID,
        pickup_challenge,
    )

    VCVerifier.verify_sender_pickup_presentation(
        presentation=sender_presentation,
        delivery_id=DELIVERY_ID,
        package_id=PACKAGE_ID,
        car_id=CAR_ID,
    )

    print("Pickup PASS")
    lock.unlock(seconds=1)

    print("=== Receiver delivery verification ===")

    delivery_challenge = challenge_manager.create_challenge(
        delivery_id=DELIVERY_ID,
        car_id=CAR_ID,
        package_id=PACKAGE_ID,
        phase="DELIVERY",
    )

    receiver_presentation = ReceiverCarSession(
        RECEIVER_ID
    ).create_presentation(
        DELIVERY_ID,
        delivery_challenge,
    )

    VCVerifier.verify_receiver_delivery_presentation(
        presentation=receiver_presentation,
        delivery_id=DELIVERY_ID,
        package_id=PACKAGE_ID,
        car_id=CAR_ID,
    )

    print("Delivery PASS")
    lock.unlock(seconds=1)

    print("=== FULL FLOW PASS ===")


if __name__ == "__main__":
    main()
