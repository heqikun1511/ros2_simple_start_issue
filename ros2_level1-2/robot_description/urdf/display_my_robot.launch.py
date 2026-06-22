from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description':
                    open('/home/amoy/ros2_ws/ros2_level1-2/urdf/my_robot.urdf').read()
            }]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', '/home/amoy/ros2_ws/ros2_level1-2/urdf/my_robot.rviz']
        )
    ])
