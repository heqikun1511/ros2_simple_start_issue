import rclpy
import time
from rclpy.node import Node
from robot_interface.action import CountUntil
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle


class MyCustomNode(Node):
    def __init__(self):
        super().__init__("count_until_server")
        self.count_until_server_ = ActionServer(
            self, CountUntil, "count_until",
            execute_callback=self.execute_callback
        )
        self.get_logger().info("action has been started")

    def execute_callback(self, goal_handle: ServerGoalHandle):
        # Get request from goal
        target_number = goal_handle.request.target_number
        period = goal_handle.request.period
        # Execute the action
        self.get_logger().info("executing the goal")
        counter = 0
        for i in range(target_number):
            counter += 1
            self.get_logger().info(str(counter))
            time.sleep(period)

        # Set final state
        goal_handle.succeed()
        result = CountUntil.Result()
        result.reached_number = counter
        return result


def main():
    rclpy.init()
    node = MyCustomNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()


if __name__ =="__main__":
    main()