import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg_share = get_package_share_directory('robot_description')

    # 使用 xacro 处理机器人模型
    from xacro import process_file
    xacro_file = os.path.join(pkg_share, 'urdf', 'my_robot_urdf.xacro')
    robot_description = process_file(xacro_file).toxml()

    # 启动 Gazebo
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-v', '4', 'empty.sdf'],
        output='screen'
    )

    # 生成机器人的 ROS-Gazebo 桥接
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'my_robot',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.05',
        ],
        output='screen'
    )

    # 发布机器人状态
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # 关节状态发布器（GUI 界面）
    joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # RViz 可视化
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg_share, 'urdf', 'my_robot.rviz')]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_entity,
        joint_state_publisher,
        rviz
    ])
  