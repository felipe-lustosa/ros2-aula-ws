import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from time import sleep

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscribe')
        self.subscription = self.create_subscription(String, 'topic', self.listener_callback, 1)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        sleep(1)


def main (args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()