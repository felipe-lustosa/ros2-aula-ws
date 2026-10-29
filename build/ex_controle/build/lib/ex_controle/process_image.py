import time
import math
import cv2

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError


class ImageProcessing(Node):

    def __init__(self):
        super().__init__("process_laser")

        # Bridge (ROS2 <-> OpenCV)
        self.bridge = CvBridge()
        
        # Subscribe to read the laserscan
        self.pose_sub = self.create_subscription(Image, "/head_front_camera/image", self.image_callback, 1)

        self.image_pub = self.create_publisher(Image, "/my_image", 1)



    def image_callback(self, msg):
        image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

        # red_mask = cv2.inRange(image, (0, 0, 100), (80, 80, 255))
        # image[red_mask > 0] = (255, 0, 0)

        height, width, channels = image.shape

        for y in range(height):
            for x in range(width):
                b, g, r = image[y, x]

                if b < 10 and g < 10 and 160 < r < 205:
                    image[y, x] = 128, 200, 50

        # print(height, width, channels)
        # cv2.imshow("camera", image)
        # cv2.waitKey(1)

        img_ros = self.bridge.cv2_to_imgmsg(image, encoding="bgr8")
        self.image_pub.publish(img_ros)

def main(args=None):

    # Star the node
    rclpy.init(args=args)
    
    # Instantiate a laser from class
    mylaser = ImageProcessing()
    
    rclpy.spin(mylaser)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()