"""
platform_server/app.py

Main FastAPI server for the VC delivery platform.
"""

from fastapi import FastAPI, HTTPException

from platform_server.models import (
    SenderRegistration,
    ReceiverRegistration,
    CarRegistration,
    DeliveryRequest,
    DeliveryRecord,
    VerifyVCRequest,
    RevokeVCRequest,
    DeliveryResult,
)

from platform_server.sender_registry import (
    register_sender as registry_register_sender,
    get_sender,
    list_senders,
)

from platform_server.receiver_registry import (
    register_receiver as registry_register_receiver,
    get_receiver,
    list_receivers,
)

from platform_server.car_registry import (
    register_car as registry_register_car,
    get_car,
    list_cars,
)

from platform_server.delivery_db import (
    create_delivery as db_create_delivery,
    get_delivery,
    list_deliveries,
    update_delivery_status,
    attach_sender_pickup_vc,
    attach_receiver_delivery_vc,
)

from platform_server.issuer import (
    create_sender_pickup_vc,
    create_receiver_delivery_vc,
    verify_vc,
    export_platform_public_key,
)

from platform_server.revocation import (
    revoke_vc,
    get_revocation_status,
    list_revoked_vcs,
)


app = FastAPI(
    title="VC Delivery Platform",
    version="0.2.0",
)


@app.get("/")
def root():
    return {
        "message": "VC Delivery Platform Running",
        "version": "0.2.0",
    }


# =========================================================
# Registry APIs
# =========================================================

@app.post("/register_sender")
def register_sender(data: SenderRegistration):
    try:
        return registry_register_sender(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/register_receiver")
def register_receiver(data: ReceiverRegistration):
    try:
        return registry_register_receiver(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/register_car")
def register_car(data: CarRegistration):
    try:
        return registry_register_car(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/senders")
def get_senders():
    return list_senders()


@app.get("/receivers")
def get_receivers():
    return list_receivers()


@app.get("/cars")
def get_cars():
    return list_cars()


# =========================================================
# Delivery APIs
# =========================================================

@app.post("/create_delivery")
def create_delivery(data: DeliveryRequest):
    sender = get_sender(data.sender_id)
    receiver = get_receiver(data.receiver_id)
    car = get_car(data.car_id)

    if sender is None:
        raise HTTPException(status_code=404, detail="Sender not found")

    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")

    if car is None:
        raise HTTPException(status_code=404, detail="Car not found")

    sender_vc = create_sender_pickup_vc(
        sender_id=data.sender_id,
        sender_pubkey=sender["sender_pubkey"],
        package_id=data.package_id,
        car_id=data.car_id,
        delivery_id=data.delivery_id,
        expiration_hours=data.expiration_hours,
    )

    receiver_vc = create_receiver_delivery_vc(
        receiver_id=data.receiver_id,
        receiver_pubkey=receiver["receiver_pubkey"],
        package_id=data.package_id,
        car_id=data.car_id,
        delivery_id=data.delivery_id,
        expiration_hours=data.expiration_hours,
    )

    record = DeliveryRecord(
        delivery_id=data.delivery_id,
        sender_id=data.sender_id,
        receiver_id=data.receiver_id,
        package_id=data.package_id,
        car_id=data.car_id,
        status="PICKUP_PENDING",
        sender_pickup_vc=sender_vc,
        receiver_delivery_vc=receiver_vc,
    )

    try:
        db_create_delivery(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return record


@app.get("/delivery/{delivery_id}")
def read_delivery(delivery_id: str):
    delivery = get_delivery(delivery_id)

    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return delivery


@app.get("/deliveries")
def read_deliveries():
    return list_deliveries()


@app.get("/vc/sender/{delivery_id}")
def get_sender_pickup_vc(delivery_id: str):
    delivery = get_delivery(delivery_id)

    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return {
        "delivery_id": delivery_id,
        "sender_pickup_vc": delivery.sender_pickup_vc,
    }


@app.get("/vc/receiver/{delivery_id}")
def get_receiver_delivery_vc(delivery_id: str):
    delivery = get_delivery(delivery_id)

    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")

    return {
        "delivery_id": delivery_id,
        "receiver_delivery_vc": delivery.receiver_delivery_vc,
    }


@app.get("/manifest/{car_id}")
def get_car_manifest(car_id: str):
    result = []

    for delivery in list_deliveries().values():
        if delivery.car_id == car_id:
            result.append({
                "delivery_id": delivery.delivery_id,
                "sender_id": delivery.sender_id,
                "receiver_id": delivery.receiver_id,
                "package_id": delivery.package_id,
                "car_id": delivery.car_id,
                "status": delivery.status,
            })

    return {
        "car_id": car_id,
        "manifest": result,
    }


@app.post("/delivery_result")
def submit_delivery_result(data: DeliveryResult):
    delivery = get_delivery(data.delivery_id)

    if delivery is None:
        raise HTTPException(status_code=404, detail="Delivery not found")

    if delivery.car_id != data.car_id:
        raise HTTPException(status_code=403, detail="Car mismatch")

    if data.status == "PICKUP_SUCCESS":
        update_delivery_status(data.delivery_id, "PICKED_UP")

    elif data.status == "PICKUP_FAILED":
        update_delivery_status(data.delivery_id, "FAILED")

    elif data.status == "DELIVERY_SUCCESS":
        update_delivery_status(data.delivery_id, "DELIVERED")

    elif data.status == "DELIVERY_FAILED":
        update_delivery_status(data.delivery_id, "FAILED")

    return {
        "status": "recorded",
        "delivery": get_delivery(data.delivery_id),
    }


# =========================================================
# VC / Revocation APIs
# =========================================================

@app.post("/verify_vc")
def verify_vc_endpoint(data: VerifyVCRequest):
    return {
        "valid": verify_vc(data.vc),
    }


@app.post("/revoke_vc")
def revoke_vc_endpoint(data: RevokeVCRequest):
    return revoke_vc(
        vc_id=data.vc_id,
        reason=data.reason,
    )


@app.get("/revocation/{vc_id}")
def check_revocation(vc_id: str):
    return get_revocation_status(vc_id)


@app.get("/revocations")
def get_revocations():
    return list_revoked_vcs()


@app.get("/platform_public_key")
def get_platform_public_key():
    return {
        "platform_public_key": export_platform_public_key(),
    }
