import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan

from visualization_msgs.msg import Marker

import time
import math

class Laser(Node):

    def __init__(self):
        super().__init__("process_laser")
        
        # Subscribe to read the laserscan
        self.pose_sub = self.create_subscription(LaserScan, "/scan_raw", self.laser_callback, 1)

        # Publisher for rviz marker
        self.publisher = self.create_publisher(Marker, '/closest_point', 1)
        self.marker_msg = Marker()

        self.marker_msg.header.frame_id = 'base_laser_link'
        self.marker_msg.header.stamp = self.get_clock().now().to_msg()

        self.marker_msg.ns = 'target'
        self.marker_msg.id = 0
        self.marker_msg.type = Marker.SPHERE
        self.marker_msg.action = Marker.ADD

        # Desired position in base_link coordinates [metres]
        self.marker_msg.pose.position.x = 0.0
        self.marker_msg.pose.position.y = 0.0
        self.marker_msg.pose.position.z = 0.0
        self.marker_msg.pose.orientation.w = 1.0

        # Sphere diameter [metres]
        self.marker_msg.scale.x = 0.05
        self.marker_msg.scale.y = 0.05
        self.marker_msg.scale.z = 0.05

        # Red, fully opaque
        self.marker_msg.color.r = 0.0
        self.marker_msg.color.g = 1.0
        self.marker_msg.color.b = 0.0
        self.marker_msg.color.a = 1.0

    def laser_callback(self, msg):

        angle_min  = msg.angle_min
        angle_max = msg.angle_max
        angle_increment = msg.angle_increment

        nbPoints = math.ceil((angle_max - angle_min) / angle_increment) + 1

        print(math.degrees(angle_min), math.degrees(angle_max), math.degrees(angle_increment),nbPoints)

        # Look for the closest point
        min_range = 1000 #float("Inf")
        min_index = 0
        for (i,r) in enumerate(msg.ranges):
            if r < min_range:
                min_range = r
                min_index = i

        print(min_range, min_index)
        
        # Convert polar to Ecuclidian coordinates
        min_a = angle_min + min_index*angle_increment
        min_x = math.cos(min_a)*min_range
        min_y = math.sin(min_a)*min_range

        print(min_x, min_y)

        # Update the marker with the result of the calculation
        self.marker_msg.pose.position.x = min_x
        self.marker_msg.pose.position.y = min_y

        # Publish the marker
        self.publisher.publish(self.marker_msg)

def main(args=None):

    # Star the node
    rclpy.init(args=args)
    
    # Instantiate a laser from class
    mylaser = Laser()
    
    rclpy.spin(mylaser)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()