"""
receiver_client/vc_store.py

Local VC storage for the receiver.

Stores receiver delivery VCs in local JSON files.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


VC_DIR = Path("data/receiver/vcs")


def ensure_vc_dir() -> None:
    VC_DIR.mkdir(parents=True, exist_ok=True)


def vc_path(delivery_id: str) -> Path:
    return VC_DIR / f"{delivery_id}_receiver_delivery_vc.json"


def save_receiver_vc(
    delivery_id: str,
    vc: Dict[str, Any],
) -> Path:
    ensure_vc_dir()

    path = vc_path(delivery_id)

    path.write_text(
        json.dumps(
            vc,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return path


def load_receiver_vc(
    delivery_id: str,
) -> Optional[Dict[str, Any]]:
    path = vc_path(delivery_id)

    if not path.exists():
        return None

    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


def delete_receiver_vc(
    delivery_id: str,
) -> bool:
    path = vc_path(delivery_id)

    if not path.exists():
        return False

    path.unlink()
    return True


def list_receiver_vcs() -> list[str]:
    ensure_vc_dir()

    return [
        path.name
        for path in VC_DIR.glob(
            "*_receiver_delivery_vc.json"
        )
    ]


if __name__ == "__main__":
    test_vc = {
        "id": "urn:uuid:test-receiver-vc",
        "type": [
            "VerifiableCredential",
            "ReceiverDeliveryCredential",
        ],
        "credentialSubject": {
            "delivery_id": "DELIVERY_001",
            "receiver_id": "receiver_001",
            "package_id": "PKG_001",
            "car_id": "CAR_RPI5_001",
            "action": "RECEIVE_PACKAGE",
        },
    }

    path = save_receiver_vc(
        "DELIVERY_001",
        test_vc,
    )

    print("Saved to:")
    print(path)

    loaded = load_receiver_vc(
        "DELIVERY_001"
    )

    print("Loaded:")
    print(loaded)

    print("All VCs:")
    print(list_receiver_vcs())
