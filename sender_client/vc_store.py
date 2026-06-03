"""
sender_client/vc_store.py

Local VC storage for the sender.

Stores sender pickup VCs in local JSON files.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


VC_DIR = Path("data/sender/vcs")


def ensure_vc_dir() -> None:
    VC_DIR.mkdir(parents=True, exist_ok=True)


def vc_path(delivery_id: str) -> Path:
    return VC_DIR / f"{delivery_id}_sender_pickup_vc.json"


def save_sender_vc(
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


def load_sender_vc(
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


def delete_sender_vc(
    delivery_id: str,
) -> bool:
    path = vc_path(delivery_id)

    if not path.exists():
        return False

    path.unlink()
    return True


def list_sender_vcs() -> list[str]:
    ensure_vc_dir()

    return [
        path.name
        for path in VC_DIR.glob(
            "*_sender_pickup_vc.json"
        )
    ]


if __name__ == "__main__":
    test_vc = {
        "id": "urn:uuid:test-sender-vc",
        "type": [
            "VerifiableCredential",
            "SenderPickupCredential",
        ],
        "credentialSubject": {
            "delivery_id": "DELIVERY_001",
            "sender_id": "sender_001",
            "package_id": "PKG_001",
            "car_id": "CAR_RPI5_001",
            "action": "PICKUP_PACKAGE",
        },
    }

    path = save_sender_vc(
        "DELIVERY_001",
        test_vc,
    )

    print("Saved to:")
    print(path)

    loaded = load_sender_vc(
        "DELIVERY_001"
    )

    print("Loaded:")
    print(loaded)

    print("All VCs:")
    print(list_sender_vcs())
