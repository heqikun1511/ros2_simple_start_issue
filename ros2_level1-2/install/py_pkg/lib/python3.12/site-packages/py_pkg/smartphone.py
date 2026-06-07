#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class SmartphoneNode(Node):
    def __init__(self):
        super().__init__("smartphone")
        self.subscriber=self.create_subscription(String,"news",self.robot_callback,10)
        self.get_logger().info("smart phone has been started")
        self.message_count = 0

    def robot_callback(self, msg: String):
        self.message_count += 1
        self.get_logger().info(f"[消息 #{self.message_count}] {msg.data}")
        self.get_logger().info(f"[消息 #{self.message_count}] {msg.data}")
        self.get_logger().info(f"[消息 #{self.message_count}] {msg.data}")
        self.get_logger().info(f"[消息 #{self.message_count}] {msg.data}")
        self.get_logger().info(f"[消息 #{self.message_count}] {msg.data}")
def main(args=None):
    rclpy.init(args=args)
    node = SmartphoneNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()
