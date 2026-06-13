"""
rpi5_car/gpio_lock.py

SG90 servo lock controller.

Tested hardware setting:
- GPIO19, physical pin 35
- unlock angle = -60
- lock angle = 60
"""

import time


class LockController:
    def __init__(
        self,
        simulation: bool = True,
        gpio_pin: int = 19,
        locked_angle: float = 60.0,
        unlocked_angle: float = -60.0,
        min_angle: float = -90.0,
        max_angle: float = 90.0,
    ):
        self.simulation = simulation
        self.gpio_pin = gpio_pin
        self.locked_angle = locked_angle
        self.unlocked_angle = unlocked_angle
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.locked = True
        self.servo = None

        if not self.simulation:
            try:
                from gpiozero import AngularServo

                self.servo = AngularServo(
                    gpio_pin,
                    min_angle=min_angle,
                    max_angle=max_angle,
                    min_pulse_width=0.0005,
                    max_pulse_width=0.0025,
                )

            except Exception as exc:
                raise RuntimeError(
                    f"Failed to initialize SG90 servo on GPIO {gpio_pin}: {exc}"
                )

        self.lock()

    def _set_angle(self, angle: float) -> None:
        if self.simulation:
            print(f"[SIM] Servo angle -> {angle}")
            return

        self.servo.angle = angle
        time.sleep(0.5)

    def lock(self) -> None:
        self._set_angle(self.locked_angle)
        self.locked = True

        if self.simulation:
            print("[SIM] Box locked")
        else:
            print(f"[SERVO] Box locked at {self.locked_angle}°")

    def unlock(self, seconds: int = 5) -> None:
        self._set_angle(self.unlocked_angle)
        self.locked = False

        if self.simulation:
            print("[SIM] Box unlocked")
        else:
            print(f"[SERVO] Box unlocked at {self.unlocked_angle}°")

        time.sleep(seconds)
        self.lock()

    def is_locked(self) -> bool:
        return self.locked

    def close(self) -> None:
        if self.servo is not None:
            self.servo.detach()


if __name__ == "__main__":
    lock = LockController(
        simulation=False,
        gpio_pin=19,
        locked_angle=60,
        unlocked_angle=-60,
    )

    print("Initial locked:", lock.is_locked())

    lock.unlock(seconds=2)

    print("Final locked:", lock.is_locked())

    lock.close()
