import rclpy
from rclpy.node import Node

from rclpy.action import ActionClient
from my_interfaces.action import CountUntil

import time

class CountClient(Node):

    def __init__(self):
        super().__init__("count_client")

        # Create the action client
        self.client = ActionClient(self, CountUntil, "count_until")

        self.target = 8


    def send_goal(self):

        # Wait for the action service
        self.client.wait_for_server()

        # Create the Goal object and populate it
        goal = CountUntil.Goal()
        goal.target = self.target

        future = self.client.send_goal_async(goal, feedback_callback=self.feedback_callback)

        # print("waiting for goal to be accepted")
        # rclpy.spin_until_future_complete(self, future)
        # print("goal accepted")

        # Add a callback to handle the response from the action server
        future.add_done_callback(self.goal_response_callback)


    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f"Feedback: {feedback.current}")


    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info("Goal rejected")
            rclpy.shutdown()
            return

        self.get_logger().info("Goal accepted")

        # Wait for the result
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)


    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f"Result: {result.reached}, Message: {result.message}")
        # rclpy.shutdown()



def main(args=None):
    rclpy.init(args=args)
    myCountClient = CountClient()
    myCountClient.send_goal()
    rclpy.spin(myCountClient)

    myCountClient.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
