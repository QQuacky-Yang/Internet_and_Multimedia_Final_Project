"""
rpi5_car/gpio_lock.py

Lock controller.

Current:
    Safe simulation mode

Future:
    Real Raspberry Pi 5 GPIO control using gpiozero.
"""

import time


class LockController:
    def __init__(self, simulation: bool = True):
        self.simulation = simulation
        self.locked = True

    def lock(self) -> None:
        self.locked = True

        if self.simulation:
            print("[SIM] Box locked")
        else:
            # Future:
            # GPIO pin LOW / relay off
            print("[HW] Box locked")

    def unlock(self, seconds: int = 5) -> None:
        self.locked = False

        if self.simulation:
            print("[SIM] Box unlocked")
        else:
            # Future:
            # GPIO pin HIGH / relay on
            print("[HW] Box unlocked")

        time.sleep(seconds)
        self.lock()

    def is_locked(self) -> bool:
        return self.locked


if __name__ == "__main__":
    lock = LockController(simulation=True)

    print("Initial locked:", lock.is_locked())

    lock.unlock(seconds=2)

    print("Final locked:", lock.is_locked())
