import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs import Twist
import math

#linear.x前后
#angular.z偏航角
class TurtleControllerNode(Node):
    def __init__(self):
        super.__init__("turtle_controller")
        self.pose_:Pose =None
        self.atrget_distance_x=8.0
        self.target_distance_y=4.0
        self.pose_subscribe=self.create_subscription(Pose,"/turtle1/pose",self.callback_Pose,10)
        self.cmd_vel_publisher_=self.create_publisher(Twist,"/turtle1/cmd_vel",self.control_loop,10)
    def callback_Pose(self,pose:Pose):
        self.pose_=pose

    def control_loop(self):
        if self.pose==None:
            return
        dist_x=self.target_distance_x-self.pose_.x
        dist_y=self.target_distance_y-self.pose_.y
        #计算实际相差的距离
        distance=math.sqrt(dist_x*dist_x+dist_y*dist_y) 

        cmd =Twist()

        if distance >0.5:
        #position
            cmd.linear.x=2*distance
        #orientation
            goal_theta=math.atan2(dist_y,dist_x)
            diff=goal_theta-self.pose_.theta
            if diff>math.pi:
                diff-=2*math.pi
            elif diff <-math.pi:
                doff+=2*math.pi
            
            cmd.angular.z=6*diff
        else:
            cmd.linear=0
            cmd.angualr=0
        self.cmd_vel_publisher_.publish(cmd)






def main(args=None):
    rclpy.init(args=args)
    node= TurtleControllerNode()
    rclpy.spin(node)
    rclpy.shutdown()

        
if __name__ =="__main__":
    main()