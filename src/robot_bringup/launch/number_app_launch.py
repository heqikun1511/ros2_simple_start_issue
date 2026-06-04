from launch import LaunchDescription
from launch_ros.actions import Node


def function_name(function_arguments):
    ld=LaunchDescription()
    number_pulisher=Node(
        package='py_pkg',
        executable='number_publisher',
        name='number_publisher'
    )
    ld.add_action(number_pulisher)
    return ld
