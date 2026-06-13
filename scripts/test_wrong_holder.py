
"""
scripts/test_wrong_holder.py

Intentional failure test:
Bob tries to use sender_001's VC.
Expected: verification FAIL.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from sender_client.wallet import SenderWallet
from sender_client.car_session import SenderCarSession
from rpi5_car.challenge import ChallengeManager
from rpi5_car.verifier import VCVerifier


DELIVERY_ID = "DELIVERY_WRONG_HOLDER_TEST"
PACKAGE_ID = "PKG_WRONG_HOLDER_TEST"
CAR_ID = "CAR_RPI5_FULL_TEST_001"


def main():
    vc = {
        "id": "urn:uuid:wrong-holder-test",
        "type": [
            "VerifiableCredential",
            "SenderPickupCredential",
        ],
        "credentialSubject": {
            "delivery_id": DELIVERY_ID,
            "sender_id": "sender_001",
            "sender_pubkey": "SIMULATED_SENDER_PUBLIC_KEY_sender_001",
            "package_id": PACKAGE_ID,
            "car_id": CAR_ID,
            "action": "PICKUP_PACKAGE",
        },
    }

    SenderWallet().add_vc(
        DELIVERY_ID,
        vc,
    )

    challenge = ChallengeManager().create_challenge(
        delivery_id=DELIVERY_ID,
        car_id=CAR_ID,
        package_id=PACKAGE_ID,
        phase="PICKUP",
    )

    presentation = SenderCarSession(
        "bob_attacker"
    ).create_presentation(
        DELIVERY_ID,
        challenge,
    )

    try:
        print("presentation holder_id =", presentation["holder_id"])
        print(
            "VC sender_id =",
            presentation["vc"]["credentialSubject"].get("sender_id"),
    	)
        VCVerifier.verify_sender_pickup_presentation(
            presentation=presentation,
            delivery_id=DELIVERY_ID,
            package_id=PACKAGE_ID,
            car_id=CAR_ID,
        )

    except Exception as exc:
        print("Expected failure:")
        print(exc)
        print("=== WRONG HOLDER TEST PASS ===")
        return

    raise RuntimeError(
        "Wrong holder was incorrectly accepted"
    )


if __name__ == "__main__":
    main()
