import rclpy
from rclpy.node import Node

from rclpy.action import ActionServer
from my_interfaces.action import CountUntil

import time

class CountServer(Node):

    def __init__(self):
        super().__init__("count_server")

        # Create the action server
        self.server = ActionServer(self, CountUntil, "count_until", execute_callback=self.execute_callback)


    def execute_callback(self, goal_handle):

        # Read the request
        target = goal_handle.request.target
        simulate_failure = goal_handle.request.simulate_failure

        # Create the variable to return
        result = CountUntil.Result()
        result.reached = 0

        # Counting loop
        while result.reached < target:
            time.sleep(1)
            result.reached += 1

        result.message = "Target reached"

        # Update the goal status
        goal_handle.succeed()

        print("Action completed")

        return result


def main(args=None):
    rclpy.init(args=args)
    myCountServer = CountServer()
    rclpy.spin(myCountServer)


if __name__ == "__main__":
    main()
