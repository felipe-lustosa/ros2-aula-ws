import rclpy
from rclpy.node import Node

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

import time

class MobileController(Node):
    def __init__(self):
        super().__init__("arm_controller")

        self.arm_pub = self.create_publisher(JointTrajectory, "/arm_controller/joint_trajectory", 1)
        self.cmd = JointTrajectory()
        self.cmd.joint_names = [
            'arm_1_joint',
            'arm_2_joint',
            'arm_3_joint',
            'arm_4_joint',
            'arm_5_joint',
            'arm_6_joint',
            'arm_7_joint'
        ]

        time.sleep(1)
        

def main(args=None):

    rclpy.init(args=args)

    my_controller = MobileController()

    point = JointTrajectoryPoint()
    point.positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    point.time_from_start = Duration(sec=5)

    my_controller.cmd.points = [point]

    my_controller.arm_pub.publish(my_controller.cmd)

    time.sleep(5)

    # rclpy.spin(my_controller)
    # rclpy.shutdown()

    # end_time = time.time() + 10

    # while time.time() < end_time:
    #     my_controller.cmd.twist.linear.x = -0.5 # m/s
    #     my_controller.twist_pub.publish(my_controller.cmd)

    # time.sleep(1)

    # my_controller.cmd.twist.linear.x = 0.0 # m/s
    # my_controller.twist_pub.publish(my_controller.cmd)

    # time.sleep(0.5)


if __name__ == "__main__":
    main()