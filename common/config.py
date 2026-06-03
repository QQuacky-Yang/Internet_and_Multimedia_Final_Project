"""
common/config.py

Shared configuration values.

Used by:
- platform_server
- sender_client
- receiver_client
- rpi5_car
"""

# =========================================================
# Platform Server
# =========================================================

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000

SERVER_URL = (
    f"http://{SERVER_HOST}:{SERVER_PORT}"
)

# =========================================================
# Delivery
# =========================================================

DEFAULT_EXPIRATION_HOURS = 24

# =========================================================
# Challenge Protocol
# =========================================================

NONCE_SIZE_BYTES = 32

CHALLENGE_PHASE_PICKUP = "PICKUP"
CHALLENGE_PHASE_DELIVERY = "DELIVERY"

# =========================================================
# Delivery States
# =========================================================

STATUS_CREATED = "CREATED"

STATUS_PICKUP_PENDING = "PICKUP_PENDING"
STATUS_PICKED_UP = "PICKED_UP"

STATUS_DELIVERY_PENDING = "DELIVERY_PENDING"
STATUS_DELIVERED = "DELIVERED"

STATUS_FAILED = "FAILED"

# =========================================================
# VC Types
# =========================================================

VC_TYPE_SENDER_PICKUP = (
    "SenderPickupCredential"
)

VC_TYPE_RECEIVER_DELIVERY = (
    "ReceiverDeliveryCredential"
)

# =========================================================
# Actions
# =========================================================

ACTION_PICKUP_PACKAGE = (
    "PICKUP_PACKAGE"
)

ACTION_RECEIVE_PACKAGE = (
    "RECEIVE_PACKAGE"
)

# =========================================================
# Message Types
# =========================================================

MSG_CHALLENGE = "CHALLENGE"

MSG_VC_PRESENTATION = (
    "VC_PRESENTATION"
)

# =========================================================
# GPIO
# =========================================================

DEFAULT_LOCK_TIMEOUT_SECONDS = 10

# =========================================================
# TPM
# =========================================================

TPM_KEY_NAME = "delivery-key"


if __name__ == "__main__":

    print("Server URL:")
    print(SERVER_URL)

    print("Pickup VC:")
    print(VC_TYPE_SENDER_PICKUP)

    print("Delivery VC:")
    print(VC_TYPE_RECEIVER_DELIVERY)
