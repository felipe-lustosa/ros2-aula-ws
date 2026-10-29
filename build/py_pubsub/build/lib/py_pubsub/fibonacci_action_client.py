import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci

import time

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self._action_client = ActionClient(self, Fibonacci, 'fibonacci')


    # def send_goal(self, order):
    #     goal_msg = Fibonacci.Goal()
    #     goal_msg.order = order

    #     self._action_client.wait_for_server()

    #     return self._action_client.send_goal_async(goal_msg)

    def send_goal(self, order):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)

        self._send_goal_future.add_done_callback(self.goal_response_callback)



def main ( args = None ) :
    rclpy.init(args=args)

    action_client = FibonacciActionClient()

    future = action_client.send_goal(10)

    rclpy.spin_until_future_complete(action_client, future)


if __name__ == ' __main__ ':
    main()