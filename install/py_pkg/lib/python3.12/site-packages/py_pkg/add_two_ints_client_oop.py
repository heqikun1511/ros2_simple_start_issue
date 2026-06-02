#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class Addtwoints(Node):
    def __init__(self):
        super().__init__("py_test")
        self.client = self.create_client(AddTwoInts, "add_two_ints")    
    def call_add_two_ints(self,a,b):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("service not available, waiting again...")

        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client.call_async(request)  # 异步调用服务，只发送一次请求
        rclpy.spin_until_future_complete(self, future)  # 等待该请求完成
        response = future.result()  # 从该请求的 future 获取结果
        self.get_logger().info(f"Result of add_two_ints: {response.sum}")  # 输出服务调用结果
       

def main(args=None):
    rclpy.init(args=args)
    node = Addtwoints()
    node.call_add_two_ints(2, 8)
    node.call_add_two_ints(3, 7)
    node.call_add_two_ints(4, 6)
    rclpy.shutdown()

if __name__=="__main__":
    main()