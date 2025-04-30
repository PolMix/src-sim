## Pol_bringup
This package is responsible for turning on all core sensors of the robot: IMU, GPS

#### Odom logger `odom_logger.py`
Used to receive and write /odom topic messages into a csv file for further analysis.
Usage: after EKF node is operating `ros2 run pol_bringup odom_logger.py`