import rclpy
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

import math

import time

class MobileController(Node):
    def __init__(self):
        super().__init__("arm_controller")

        self.arm_pub = self.create_publisher(JointTrajectory, "/head_controller/joint_trajectory", 1)
        self.cmd = JointTrajectory()
        self.cmd.joint_names = [
            'head_1_joint',
            'head_2_joint',
        ]

        time.sleep(1)
        

def main(args=None):

    rclpy.init(args=args)

    my_controller = MobileController()

    point = JointTrajectoryPoint()
    
    point.positions = [math.radians(90), 0.0]
    point.time_from_start = Duration(sec=5)

    point2 = JointTrajectoryPoint()
    
    point2.positions = [math.radians(20), 0.0]
    point2.time_from_start = Duration(sec=10)

    my_controller.cmd.points = [point, point2]

    my_controller.arm_pub.publish(my_controller.cmd)

    time.sleep(5)

    # rclpy.spin(my_controller)
    # rclpy.shutdown()

    # time.sleep(0.5)


if __name__ == "__main__":
    main()