"""
platform_server/models.py

Pydantic models for the platform server.

This file defines:
1. sender registration format
2. receiver registration format
3. car registration format
4. delivery creation format
5. VC verification request format
6. delivery result format
"""
from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field


# =========================================================
# Registration Models
# =========================================================

class SenderRegistration(BaseModel):
    sender_id: str = Field(..., examples=["sender_001"])
    sender_pubkey: str = Field(..., examples=["sender-public-key-placeholder"])
    display_name: Optional[str] = Field(default=None, examples=["Alice Seller"])


class ReceiverRegistration(BaseModel):
    receiver_id: str = Field(..., examples=["receiver_001"])
    receiver_pubkey: str = Field(..., examples=["receiver-public-key-placeholder"])
    display_name: Optional[str] = Field(default=None, examples=["Bob Receiver"])


class CarRegistration(BaseModel):
    car_id: str = Field(..., examples=["CAR_RPI5_001"])
    car_pubkey: str = Field(..., examples=["car-public-key-placeholder"])
    description: Optional[str] = Field(default=None, examples=["RPi5 autonomous delivery car"])


# =========================================================
# Delivery Models
# =========================================================

class DeliveryRequest(BaseModel):
    delivery_id: str = Field(..., examples=["DELIVERY_001"])
    sender_id: str = Field(..., examples=["sender_001"])
    receiver_id: str = Field(..., examples=["receiver_001"])
    package_id: str = Field(..., examples=["PKG_001"])
    car_id: str = Field(..., examples=["CAR_RPI5_001"])
    expiration_hours: int = Field(default=24, ge=1, le=168)


class DeliveryRecord(BaseModel):
    delivery_id: str
    sender_id: str
    receiver_id: str
    package_id: str
    car_id: str
    status: Literal[
        "CREATED",
        "PICKUP_PENDING",
        "PICKED_UP",
        "DELIVERY_PENDING",
        "DELIVERED",
        "FAILED",
        "CANCELLED",
    ] = "CREATED"
    sender_pickup_vc: Optional[Dict[str, Any]] = None
    receiver_delivery_vc: Optional[Dict[str, Any]] = None


# =========================================================
# Verification / Revocation Models
# =========================================================

class VerifyVCRequest(BaseModel):
    vc: Dict[str, Any]


class RevokeVCRequest(BaseModel):
    vc_id: str
    reason: Optional[str] = None


class RevocationStatus(BaseModel):
    vc_id: str
    revoked: bool
    reason: Optional[str] = None


# =========================================================
# Delivery Result Models
# =========================================================

class DeliveryResult(BaseModel):
    delivery_id: str
    car_id: str
    status: Literal[
        "PICKUP_SUCCESS",
        "PICKUP_FAILED",
        "DELIVERY_SUCCESS",
        "DELIVERY_FAILED",
    ]
    detail: Optional[str] = None
