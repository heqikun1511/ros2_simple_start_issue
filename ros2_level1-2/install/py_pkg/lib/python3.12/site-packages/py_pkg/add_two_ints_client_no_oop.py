#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts



def main(args=None):
    rclpy.init(args=args)
    node = Node("add_two_ints_client")
    client = node.create_client(AddTwoInts, "add_two_ints")
    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().warn("service not available, waiting again...")

    request = AddTwoInts.Request()
    request.a = 2
    request.b = 8

    client.call_async(request)#异步调用服务，作用是发送请求后不阻塞当前线程，可以继续执行其他操作
    rclpy.spin_until_future_complete(node, client.call_async(request))  #等待服务调用完成，作用是阻塞当前线程直到服务调用完成并返回结果
    response = client.call_async(request).result()  #获取服务调用的结果，作用是从异步调用中获取结果，如果服务调用成功则返回结果对象，否则可能抛出异常
    node.get_logger().info(f"Result of add_two_ints: {response.sum}")#输出服务调用的结果，作用是将服务调用的结果（两个整数的和）打印到日志中，方便用户查看
    rclpy.shutdown()

if __name__=="__main__":
    main()
