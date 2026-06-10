import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from functools import partial


class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.spawn_client_=self.create_client(Spawn, "/spawn")


    def call_spawn_service(self,turtle_name,x,y,theta):
        while not self.spawn_client_.wait_for_service(1.0):
            self.get_logger().warn("waiting")
        
        request=Spawn.Request()
        request.x=x
        request.y=y
        request.theta=theta
        request.name=turtle_name

        future=self.spawn_client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_spawn_service, request=request))

    def callback_call_spawn_service(self,future,request):
        response = future.result()
        if response.name!="":
            self.get_logger().info("new turtle has been generate"+ response.name)




def main(args=None):
    rclpy.init()
    node = TurtleSpawnerNode()
    node.call_spawn_service("test",3.0,3.0,3.0)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__=="__main__":
    main()