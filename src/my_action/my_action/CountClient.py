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

        self.target = 5


    def send_goal(self):

        # Wait for the action service
        self.client.wait_for_server()

        # Create the Goal object and populate it
        goal = CountUntil.Goal()
        goal.target = self.target

        future = self.client.send_goal_async(goal)

        print("waiting for goal to be completed")

        rclpy.spin_until_future_complete(self, future)

        print("goal completed")




def main(args=None):
    rclpy.init(args=args)
    myCountClient = CountClient()
    rclpy.spin(myCountClient)


if __name__ == "__main__":
    main()
