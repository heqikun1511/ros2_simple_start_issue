import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
from functools import partial
import random
import math

class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__("turtle_spawner")
        self.spawn_client_=self.create_client(Spawn, "/spawn")
        self.turtle_counter_=0
        name=self.turtle_name_prefix_+str(self.turtle_)
        x=random.uniform(0.0,11.0)
        y=random.uniform(0.0,11.0)
        theta=random.uniform(name,x,y,theta)


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
    def spawn_new_turtle(self):
        self.turtle_counter_+=1
        

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