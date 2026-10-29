import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import math

import time

class MobileController(Node):
    def __init__(self):
        super().__init__("turtle_controller")

        self.twist_pub = self.create_publisher(Twist, "/turtle1/cmd_vel", 1)
        self.pose_pub = self.create_subscription(Pose, "/turtle1/pose", self._pose_callback, 1)

        self.cmd = Twist()
        self.x_goal = 8
        self.y_goal = 4
        self.theta_goal = math.radians(90)

        self.state = 0

        time.sleep(1)

    def _pose_callback(self, msg: Pose):
        x = msg.x
        y = msg.y
        theta = msg.theta

        e_x = self.x_goal - x
        e_y = self.y_goal - y
        theta_maneuver = math.atan2(e_y, e_x)

        e_theta = theta_maneuver - theta
        e_theta_final = self.theta_goal - theta

        e_dist = math.sqrt((e_x ** 2) + (e_y ** 2))

        angular_tolerance = math.radians(0.1)
        distance_tolerance = 0.01

        K_theta = 1
        K_dist = 0.1

        if self.state == 0:
            self.get_logger().info("Maneuver")
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = K_theta * e_theta

            if abs(e_theta) < angular_tolerance:
                self.state = 1

        if self.state == 1:
            self.get_logger().info("Distance")
            self.cmd.linear.x = K_dist * e_dist
            self.cmd.angular.z = 0.0

            if e_dist < distance_tolerance:
                self.state = 2

        if self.state == 2:
            self.get_logger().info("Final orientation")
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = K_theta * e_theta_final

            if abs(e_theta_final) < angular_tolerance:
                self.state = 3

        if self.state == 3:
            self.get_logger().info("Stop")
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
        # if abs(e_theta) > angular_tolerance and e_dist > distance_tolerance:
        #     self.get_logger().info(f"Maneuver")
        #     self.cmd.linear.x = 0.0
        #     self.cmd.angular.z = K_theta * e_theta
        # elif e_dist > distance_tolerance:
        #     self.get_logger().info(f"Distance")
        #     self.cmd.linear.x = e_dist * K_dist
        #     self.cmd.angular.z = 0.0
        # else:
        #     self.get_logger().info(f"Final Orientation")
        #     self.cmd.linear.x = 0.0
        #     self.cmd.angular.z = K_theta * e_theta_final

        self.twist_pub.publish(self.cmd)

        self.get_logger().info(f"x={x}, y={y}, theta={theta}")

def main(args=None):

    rclpy.init(args=args)

    my_controller = MobileController()

    rclpy.spin(my_controller)
    # my_controller.cmd.linear.x = 0.5 # m/s
    # my_controller.twist_pub.publish(my_controller.cmd)

    # time.sleep(1)

    # my_controller.cmd.linear.x = 0.0 # m/s
    # my_controller.twist_pub.publish(my_controller.cmd)

    # time.sleep(1)


if __name__ == "__main__":
    main()