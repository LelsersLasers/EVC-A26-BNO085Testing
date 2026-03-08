"""
BNO085 IMU data reader for NVIDIA Jetson Orin Nano Super
Reads orientation, acceleration, gyro, and magnetic field data via I2C
"""

import math
import time

import board  # type: ignore
import busio  # type: ignore
import adafruit_bno08x  # type: ignore
from adafruit_bno08x.i2c import BNO08X_I2C  # type: ignore

# --- Initialize I2C and sensor ---
i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)

# --- Enable desired sensor reports ---
bno.enable_feature(adafruit_bno08x.BNO_REPORT_ACCELEROMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GYROSCOPE)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_MAGNETOMETER)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_ROTATION_VECTOR)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_LINEAR_ACCELERATION)
bno.enable_feature(adafruit_bno08x.BNO_REPORT_GRAVITY)

print("BNO085 IMU initialized. Reading data...\n")


try:
    while True:
        # Rotation vector (quaternion) - fused orientation
        quat_i, quat_j, quat_k, quat_real = bno.quaternion
        print(f"Quaternion  - i: {quat_i:+.4f}  j: {quat_j:+.4f}  k: {quat_k:+.4f}  real: {quat_real:+.4f}")

        # Accelerometer (m/s²) - includes gravity
        accel_x, accel_y, accel_z = bno.acceleration
        print(f"Accel (m/s²)- x: {accel_x:+.4f}  y: {accel_y:+.4f}  z: {accel_z:+.4f}")

        # Linear acceleration (m/s²) - gravity removed
        lin_x, lin_y, lin_z = bno.linear_acceleration
        print(f"Linear Acc  - x: {lin_x:+.4f}  y: {lin_y:+.4f}  z: {lin_z:+.4f}")
    
        # Gyroscope (rad/s)
        gyro_x, gyro_y, gyro_z = bno.gyro
        print(f"Gyro (rad/s)- x: {gyro_x:+.4f}  y: {gyro_y:+.4f}  z: {gyro_z:+.4f}")

        mag_x, mag_y, mag_z = bno.magnetic
        print(f"Mag (µT)    - x: {mag_x:+.4f}  y: {mag_y:+.4f}  z: {mag_z:+.4f}")

        # Gravity vector (m/s²)
        grav_x, grav_y, grav_z = bno.gravity
        print(f"Gravity     - x: {grav_x:+.4f}  y: {grav_y:+.4f}  z: {grav_z:+.4f}")
        
        print("-" * 60)
        time.sleep(0.1)  # 10 Hz update rate

except KeyboardInterrupt:
    print("\nStopped.")