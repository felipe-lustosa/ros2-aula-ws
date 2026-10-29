import rclpy
from rclpy.node import Node

from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

import math

import time

class MobileController(Node):
    def __init__(self):
        super().__init__("tiago_controller")

        self.twist_pub = self.create_publisher(TwistStamped, "/mobile_base_controller/cmd_vel", 1)
        self.pose_pub = self.create_subscription(Odometry, "/mobile_base_controller/odom", self.pose_callback, 1)

        self.cmd = TwistStamped()
        self.x_goal = 2
        self.y_goal = 2
        self.theta_goal = math.radians(90)

        self.state = 0

        time.sleep(1)

    def pose_callback(self, msg: Odometry):
        # print(msg.pose.pose)
        # print("---")

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation

        roll, pitch, yaw = euler_from_quaternion([q.x, q.y, q.z, q.w])

        print(f"Pose: {x}, {y}, {math.degrees(yaw)}")

        theta = yaw

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
            self.cmd.twist.linear.x = 0.0
            self.cmd.twist.angular.z = K_theta * e_theta

            if abs(e_theta) < angular_tolerance:
                self.state = 1

        if self.state == 1:
            self.get_logger().info("Distance")
            self.cmd.twist.linear.x = K_dist * e_dist
            self.cmd.twist.angular.z = 0.0

            if e_dist < distance_tolerance:
                self.state = 2

        if self.state == 2:
            self.get_logger().info("Final orientation")
            self.cmd.twist.linear.x = 0.0
            self.cmd.twist.angular.z = K_theta * e_theta_final

            if abs(e_theta_final) < angular_tolerance:
                self.state = 3

        if self.state == 3:
            self.get_logger().info("Stop")
            self.cmd.twist.linear.x = 0.0
            self.cmd.twist.angular.z = 0.0

        self.twist_pub.publish(self.cmd)

        self.get_logger().info(f"x={x}, y={y}, theta={theta}")

def main(args=None):

    rclpy.init(args=args)

    my_controller = MobileController()

    rclpy.spin(my_controller)
    rclpy.shutdown()
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