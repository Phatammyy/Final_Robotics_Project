from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_path = get_package_share_directory('pick_scan_place')
    ur_moveit_config = get_package_share_directory('ur_moveit_config')
    world_file = os.path.join(pkg_path, 'worlds', 'pick_scan_place.world')
    urdf_file = os.path.join(pkg_path, 'urdf', 'ur5_simple.urdf')
    ur_moveit_launch = os.path.join(ur_moveit_config, 'launch', 'ur_moveit.launch.py')
    robot_description = ParameterValue(Command(['cat ', urdf_file]), value_type=str)
    return LaunchDescription([
        ExecuteProcess(
            cmd=['gazebo', '--verbose', world_file,
                 '-s', 'libgazebo_ros_factory.so',
                 '-s', 'libgazebo_ros_init.so'],
            output='screen'
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='world_to_base',
            arguments=['0', '0', '0', '0', '0', '0', 'world', 'base_link'],
            output='screen'
        ),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
             output='screen'),
        TimerAction(period=5.0, actions=[
            Node(package='gazebo_ros', executable='spawn_entity.py',
                 arguments=['-entity', 'ur5', '-topic', 'robot_description',
                             '-x', '0.0', '-y', '0.0', '-z', '0.0',
                             '-R', '0.0', '-P', '0.0', '-Y', '0.0'],
                 output='screen')
        ]),
        TimerAction(period=10.0, actions=[
            Node(package='controller_manager', executable='spawner',
                 arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
                 output='screen')
        ]),
        TimerAction(period=11.0, actions=[
            Node(package='controller_manager', executable='spawner',
                 arguments=['joint_trajectory_controller', '--controller-manager', '/controller_manager'],
                 output='screen')
        ]),
        TimerAction(period=13.0, actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(ur_moveit_launch),
                launch_arguments={
                    'ur_type': 'ur5',
                    'use_fake_hardware': 'false',
                    'use_sim_time': 'true',
                    'launch_rviz': 'true',
                }.items()
            )
        ]),
        TimerAction(period=20.0, actions=[
            Node(
                package='zbar_ros',
                executable='barcode_reader',
                name='barcode_reader',
                remappings=[('image', '/scan_camera/scan_camera/image_raw')],
                output='screen'
            ),
            Node(package='pick_scan_place', executable='qr_scanner',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='decision',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='conveyor',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='object_tracker',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='motion_planner',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='pick_scan_place',
                 parameters=[{'use_sim_time': True}], output='screen'),
        ]),
    ])
