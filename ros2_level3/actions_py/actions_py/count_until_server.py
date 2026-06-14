import rclpy
import time
import threading
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse#目标相应枚举     取消相应枚举
from rclpy.action.server import ServerGoalHandle      #服务端目标句柄
from rclpy.executors import MultiThreadedExecutor          #多线程执行
from robot_interface.action import CountUntil           #自定义接口


class CountUntilServerNode(Node):
    def __init__(self):
        super().__init__("count_until_server")
        self.goal_lock_ = threading.Lock()
        self.goal_handle_ = None#初始化
        self.count_until_server_ = ActionServer(
            self,
            CountUntil,
            "count_until",
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
        )
        self.get_logger().info("action has been started")

    def goal_callback(self, goal_request: CountUntil.Goal):
        self.get_logger().info("receive goal")
        # validate the goal
        with self.goal_lock_:
            if self.goal_handle_ is not None:
                self.get_logger().info("a goal is already executing, reject this goal")
                return GoalResponse.REJECT
            if goal_request.target_number <= 0:
                self.get_logger().info("reject the goal")
                return GoalResponse.REJECT
        self.get_logger().info("accept the goal")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("cancel request received")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        with self.goal_lock_:
            self.goal_handle_ = goal_handle
        # Get request from goal
        target_number = goal_handle.request.target_number
        period = goal_handle.request.period

        # Execute the action
        self.get_logger().info("executing the goal")
        feedback = CountUntil.Feedback()
        counter = 0

        try:
            for i in range(target_number):
                if goal_handle.is_cancel_requested:
                    self.get_logger().info("goal was canceled")
                    goal_handle.canceled()
                    result = CountUntil.Result()
                    result.reached_number = counter
                    return result

                counter += 1
                self.get_logger().info(str(counter))
                feedback.current_number = counter
                goal_handle.publish_feedback(feedback)
                time.sleep(period)

            # Set final state
            goal_handle.succeed()
            result = CountUntil.Result()
            result.reached_number = counter
            return result
        finally:
            with self.goal_lock_:
                self.goal_handle_ = None


def main(args=None):
    rclpy.init(args=args)
    node = CountUntilServerNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info("server shutting down")
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
    