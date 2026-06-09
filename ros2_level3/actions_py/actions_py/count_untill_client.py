import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from robot_interface.action import CountUntil


class CountUntilClient(Node):
    def __init__(self):
        super().__init__("count_until_client")
        self.action_client_ = ActionClient(self, CountUntil, "count_until")
        self.goal_handle_: ClientGoalHandle = None

    def send_goal(self, target_number, period):
        self.action_client_.wait_for_server()

        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period

        self.get_logger().info("Sending goal")
        self.send_goal_future = self.action_client_.send_goal_async(
            goal,
            feedback_callback=self.goal_feedback_callback,
        )
        self.send_goal_future.add_done_callback(self.goal_response_callback)

        # Create a timer to cancel the goal after 2 seconds
        self.timer_ = self.create_timer(2.0, self.cancel_goal)

    def goal_feedback_callback(self, feedback):
        current_number = feedback.feedback.current_number
        self.get_logger().info(f"Feedback: {current_number}")

    def goal_response_callback(self, future):
        self.goal_handle_ = future.result()
        if self.goal_handle_.accepted:
            self.get_logger().info("Goal got accepted")
            self.goal_handle_.get_result_async().add_done_callback(
                self.goal_result_callback)
        else:
            self.get_logger().warn("Goal got rejected")

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f"Success: reached_number = {result.reached_number}")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().info("Goal got aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info("Goal got canceled")
        rclpy.shutdown()

    def cancel_goal(self):
        self.get_logger().info("Send a cancel request")
        if self.goal_handle_ is not None:
            self.goal_handle_.cancel_goal_async()
        self.timer_.cancel()




def main(args=None):
    rclpy.init(args=args)
    node = CountUntilClient()
    node.send_goal(6, 1.0)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("client shutting down")
    finally:
        if rclpy.ok():
            rclpy.shutdown()



    

