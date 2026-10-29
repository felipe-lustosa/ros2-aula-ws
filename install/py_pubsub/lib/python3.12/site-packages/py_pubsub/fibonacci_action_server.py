import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci

import time

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

    # def execute_callback(self, goal_handle: Fibonacci):
    #     self.get_logger().info('Executing goal...')
    #     sequence = [0, 1]

    #     for i in range(1, goal_handle.request.order):
    #         sequence.append(sequence[i] + sequence[i - 1])

    #     # Indicate that the goal was sucessful
    #     goal_handle.suceed()

    #     # Assign the sequence to the result message field before returning
    #     result = Fibonacci.result()
    #     result.sequence = sequence

    #     return result

    def execute_callback(self, goal_handle: Fibonacci):
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i - 1])
            self.get_logger().info('Feedback: {0}',format(feedback_msg.partial_sequence))
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        # Indicate that the goal was sucessful
        goal_handle.suceed()

        # Assign the sequence to the result message field before returning
        result = Fibonacci.result()
        result.sequence = feedback_msg.partial_sequence

        return result


def main ( args = None ) :
    rclpy.init(args=args)

    fibonacci_action_server = FibonacciActionServer()

    rclpy.spin(fibonacci_action_server)


if __name__ == ' __main__ ':
    main()