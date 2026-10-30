import rclpy
from rclpy.node import Node

from rclpy.action import ActionServer, GoalResponse
from my_interfaces.action import CountUntil

import time

class CountServer(Node):

    def __init__(self):
        super().__init__("count_server")

        # Create the action server
        self.server = ActionServer(self, CountUntil, "count_until", execute_callback=self.execute_callback, goal_callback=self.goal_callback)


    def goal_callback(self, goal_request):
        # Accept if target is greater than 0 and less than or equal to 10, otherwise reject
        if goal_request.target <= 0 or goal_request.target > 10:
            self.get_logger().info(f"Received goal request with target: {goal_request.target}. Goal rejected.")
            return GoalResponse.REJECT
        self.get_logger().info(f"Received goal request with target: {goal_request.target}")
        return GoalResponse.ACCEPT


    # Não foi implementado o cancelamento da ação, então não é necessário implementar o callback de cancelamento
    # O cancelamento da ação é feito pelo cliente, que envia uma solicitação de cancelamento para o servidor de ações. O servidor de ações então verifica se a ação pode ser cancelada e, se puder, cancela a ação e retorna uma resposta para o cliente. Se a ação não puder ser cancelada, o servidor de ações retorna uma resposta indicando que a ação não pôde ser cancelada.

    def execute_callback(self, goal_handle):

        # Read the request
        target = goal_handle.request.target
        simulate_failure = goal_handle.request.simulate_failure

        # Create the variable to return
        result = CountUntil.Result()
        result.reached = 0

        feedback_msg = CountUntil.Feedback()

        # Counting loop
        while result.reached < target:
            time.sleep(1)
            result.reached += 1

            # Publish the feedback
            feedback_msg.current = result.reached
            goal_handle.publish_feedback(feedback_msg)

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
