"""
rpi5_car/car_state.py

Local state machine for the delivery car.
"""

from enum import Enum
from typing import Optional


class CarState(str, Enum):
    IDLE = "IDLE"
    WAITING_FOR_PICKUP = "WAITING_FOR_PICKUP"
    PACKAGE_ONBOARD = "PACKAGE_ONBOARD"
    WAITING_FOR_RECEIVER = "WAITING_FOR_RECEIVER"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"


class DeliveryCarState:
    def __init__(self):
        self.state: CarState = CarState.IDLE
        self.current_delivery_id: Optional[str] = None
        self.current_package_id: Optional[str] = None

    def assign_delivery(
        self,
        delivery_id: str,
        package_id: str,
    ) -> None:
        self.current_delivery_id = delivery_id
        self.current_package_id = package_id
        self.state = CarState.WAITING_FOR_PICKUP

    def mark_picked_up(self) -> None:
        self.state = CarState.PACKAGE_ONBOARD

    def start_delivery(self) -> None:
        self.state = CarState.WAITING_FOR_RECEIVER

    def mark_delivered(self) -> None:
        self.state = CarState.DELIVERED

    def mark_failed(self) -> None:
        self.state = CarState.FAILED

    def reset(self) -> None:
        self.state = CarState.IDLE
        self.current_delivery_id = None
        self.current_package_id = None

    def to_dict(self) -> dict:
        return {
            "state": self.state.value,
            "current_delivery_id": self.current_delivery_id,
            "current_package_id": self.current_package_id,
        }


if __name__ == "__main__":
    car_state = DeliveryCarState()

    print("Initial:")
    print(car_state.to_dict())

    car_state.assign_delivery(
        delivery_id="DELIVERY_001",
        package_id="PKG_001",
    )

    print("After assignment:")
    print(car_state.to_dict())

    car_state.mark_picked_up()
    print("After pickup:")
    print(car_state.to_dict())

    car_state.start_delivery()
    print("Waiting for receiver:")
    print(car_state.to_dict())

    car_state.mark_delivered()
    print("Delivered:")
    print(car_state.to_dict())
