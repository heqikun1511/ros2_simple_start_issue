from launch import LaunchDescription
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
    urdf_path = os.path.join(get_package_share_path('robot_description'), 'urdf', 'robot.xacro')
    robot_description_config = ParameterValue(Command(['xacro ', str(urdf_path)]), value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description_config}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2'
    )    
    
    
    
    
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node



        
    ])