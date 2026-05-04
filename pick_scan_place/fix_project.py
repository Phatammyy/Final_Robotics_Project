import os

base = '/home/algamal/ros2_ws/pick_scan_place'

files = {}

files['config/ros2_controllers.yaml'] = """controller_manager:
  ros__parameters:
    update_rate: 100
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster
    joint_trajectory_controller:
      type: joint_trajectory_controller/JointTrajectoryController

joint_trajectory_controller:
  ros__parameters:
    joints:
      - shoulder_pan_joint
      - shoulder_lift_joint
      - elbow_joint
      - wrist_1_joint
      - wrist_2_joint
      - wrist_3_joint
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity
    state_publish_rate: 100.0
    action_monitor_rate: 20.0
    allow_partial_joints_goal: false
"""

files['urdf/ur5_simple.urdf'] = """<?xml version="1.0"?>
<robot name="ur5">
  <link name="base_link">
    <visual><geometry><cylinder radius="0.075" length="0.05"/></geometry>
      <material name="dark_gray"><color rgba="0.3 0.3 0.3 1"/></material></visual>
    <collision><geometry><cylinder radius="0.075" length="0.05"/></geometry></collision>
    <inertial><mass value="4.0"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/></inertial>
  </link>
  <link name="shoulder_link">
    <visual><geometry><sphere radius="0.06"/></geometry>
      <material name="orange"><color rgba="0.9 0.5 0.1 1"/></material></visual>
    <collision><geometry><sphere radius="0.06"/></geometry></collision>
    <inertial><mass value="3.7"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.01"/></inertial>
  </link>
  <link name="upper_arm_link">
    <visual><origin xyz="0 0 0.213" rpy="0 0 0"/>
      <geometry><cylinder radius="0.04" length="0.425"/></geometry>
      <material name="orange"><color rgba="0.9 0.5 0.1 1"/></material></visual>
    <collision><origin xyz="0 0 0.213" rpy="0 0 0"/>
      <geometry><cylinder radius="0.04" length="0.425"/></geometry></collision>
    <inertial><mass value="8.393"/>
      <inertia ixx="0.02" ixy="0" ixz="0" iyy="0.02" iyz="0" izz="0.01"/></inertial>
  </link>
  <link name="forearm_link">
    <visual><origin xyz="0 0 0.196" rpy="0 0 0"/>
      <geometry><cylinder radius="0.03" length="0.392"/></geometry>
      <material name="orange"><color rgba="0.9 0.5 0.1 1"/></material></visual>
    <collision><origin xyz="0 0 0.196" rpy="0 0 0"/>
      <geometry><cylinder radius="0.03" length="0.392"/></geometry></collision>
    <inertial><mass value="2.275"/>
      <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.005"/></inertial>
  </link>
  <link name="wrist_1_link">
    <visual><geometry><sphere radius="0.035"/></geometry>
      <material name="dark_orange"><color rgba="0.7 0.3 0.1 1"/></material></visual>
    <collision><geometry><sphere radius="0.035"/></geometry></collision>
    <inertial><mass value="1.219"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.005"/></inertial>
  </link>
  <link name="wrist_2_link">
    <visual><geometry><sphere radius="0.035"/></geometry>
      <material name="dark_orange"><color rgba="0.7 0.3 0.1 1"/></material></visual>
    <collision><geometry><sphere radius="0.035"/></geometry></collision>
    <inertial><mass value="1.219"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.005"/></inertial>
  </link>
  <link name="wrist_3_link">
    <visual><geometry><sphere radius="0.03"/></geometry>
      <material name="dark_orange"><color rgba="0.7 0.3 0.1 1"/></material></visual>
    <collision><geometry><sphere radius="0.03"/></geometry></collision>
    <inertial><mass value="0.1879"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/></inertial>
  </link>
  <link name="tool0">
    <visual><geometry><box size="0.02 0.06 0.08"/></geometry>
      <material name="gray"><color rgba="0.5 0.5 0.5 1"/></material></visual>
    <collision><geometry><box size="0.02 0.06 0.08"/></geometry></collision>
    <inertial><mass value="0.1"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/></inertial>
  </link>
  <joint name="shoulder_pan_joint" type="revolute">
    <parent link="base_link"/><child link="shoulder_link"/>
    <origin xyz="0 0 0.089" rpy="0 0 0"/><axis xyz="0 0 1"/>
    <limit lower="-6.2832" upper="6.2832" effort="150.0" velocity="3.15"/>
  </joint>
  <joint name="shoulder_lift_joint" type="revolute">
    <parent link="shoulder_link"/><child link="upper_arm_link"/>
    <origin xyz="0 0 0" rpy="1.5708 0 0"/><axis xyz="0 0 1"/>
    <limit lower="-6.2832" upper="6.2832" effort="150.0" velocity="3.15"/>
  </joint>
  <joint name="elbow_joint" type="revolute">
    <parent link="upper_arm_link"/><child link="forearm_link"/>
    <origin xyz="0 -0.425 0" rpy="0 0 0"/><axis xyz="0 0 1"/>
    <limit lower="-3.1416" upper="3.1416" effort="150.0" velocity="3.15"/>
  </joint>
  <joint name="wrist_1_joint" type="revolute">
    <parent link="forearm_link"/><child link="wrist_1_link"/>
    <origin xyz="0 -0.392 0" rpy="1.5708 0 0"/><axis xyz="0 0 1"/>
    <limit lower="-6.2832" upper="6.2832" effort="28.0" velocity="3.2"/>
  </joint>
  <joint name="wrist_2_joint" type="revolute">
    <parent link="wrist_1_link"/><child link="wrist_2_link"/>
    <origin xyz="0 0 0.109" rpy="-1.5708 0 0"/><axis xyz="0 0 1"/>
    <limit lower="-6.2832" upper="6.2832" effort="28.0" velocity="3.2"/>
  </joint>
  <joint name="wrist_3_joint" type="revolute">
    <parent link="wrist_2_link"/><child link="wrist_3_link"/>
    <origin xyz="0 0.093 0" rpy="1.5708 0 0"/><axis xyz="0 0 1"/>
    <limit lower="-6.2832" upper="6.2832" effort="28.0" velocity="3.2"/>
  </joint>
  <joint name="tool_joint" type="fixed">
    <parent link="wrist_3_link"/><child link="tool0"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>
  <ros2_control name="GazeboSystem" type="system">
    <hardware>
      <plugin>gazebo_ros2_control/GazeboSystem</plugin>
    </hardware>
    <joint name="shoulder_pan_joint">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="shoulder_lift_joint">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">-1.5708</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="elbow_joint">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="wrist_1_joint">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">-1.5708</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="wrist_2_joint">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
    <joint name="wrist_3_joint">
      <command_interface name="position"/>
      <state_interface name="position"><param name="initial_value">0.0</param></state_interface>
      <state_interface name="velocity"/>
    </joint>
  </ros2_control>
  <gazebo>
    <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
      <parameters>$(find pick_scan_place)/config/ros2_controllers.yaml</parameters>
    </plugin>
  </gazebo>
</robot>
"""

files['launch/robot.launch.py'] = """from launch import LaunchDescription
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
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
             output='screen'),
        TimerAction(period=5.0, actions=[
            Node(package='gazebo_ros', executable='spawn_entity.py',
                 arguments=['-entity', 'ur5', '-topic', 'robot_description',
                             '-x', '0.0', '-y', '-0.5', '-z', '1.3',
                             '-R', '0.0', '-P', '0.0', '-Y', '1.5708'],
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
            Node(package='pick_scan_place', executable='qr_scanner',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='decision',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='conveyor',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='motion_planner',
                 parameters=[{'use_sim_time': True}], output='screen'),
            Node(package='pick_scan_place', executable='pick_scan_place',
                 parameters=[{'use_sim_time': True}], output='screen'),
        ]),
    ])
"""

files['pick_scan_place/pick_scan_place_node.py'] = """import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pick_scan_place.robot_states import RobotState

class PickScanPlaceNode(Node):
    def __init__(self):
        super().__init__('pick_scan_place_node')
        self.current_state = RobotState.IDLE
        self.target_bin = None
        self.motion_done = False
        self.qr_received = False
        self.create_subscription(String, '/bin_selection', self.bin_selection_callback, 10)
        self.create_subscription(String, '/conveyor_status', self.conveyor_status_callback, 10)
        self.create_subscription(String, '/motion_status', self.motion_status_callback, 10)
        self.conveyor_pub = self.create_publisher(String, '/conveyor_command', 10)
        self.state_pub = self.create_publisher(String, '/robot_state', 10)
        self.motion_pub = self.create_publisher(String, '/motion_command', 10)
        self.timer = self.create_timer(0.5, self.pipeline_loop)
        self.get_logger().info('Pick-Scan-Place Node started.')

    def bin_selection_callback(self, msg):
        self.target_bin = msg.data
        self.qr_received = True

    def conveyor_status_callback(self, msg):
        self.get_logger().info(f'Conveyor: {msg.data}')

    def motion_status_callback(self, msg):
        status = msg.data.strip().upper()
        if status == 'DONE':
            self.motion_done = True
        elif status == 'FAILED':
            self.get_logger().error('Motion FAILED - resetting.')
            self.transition_to(RobotState.IDLE)

    def send_motion(self, command):
        self.motion_done = False
        msg = String()
        msg.data = command
        self.motion_pub.publish(msg)
        self.get_logger().info(f'Motion sent: {command}')

    def send_conveyor(self, command):
        msg = String()
        msg.data = command
        self.conveyor_pub.publish(msg)

    def transition_to(self, new_state):
        self.get_logger().info(f'{self.current_state} -> {new_state}')
        self.current_state = new_state
        msg = String()
        msg.data = new_state
        self.state_pub.publish(msg)

    def pipeline_loop(self):
        if self.current_state == RobotState.IDLE:
            self.send_conveyor('STOP')
            self.send_motion('HOME')
            self.transition_to(RobotState.PICKING)
        elif self.current_state == RobotState.PICKING:
            if not self.motion_done:
                return
            self.send_motion('PICK')
            self.transition_to(RobotState.SCANNING)
        elif self.current_state == RobotState.SCANNING:
            if not self.motion_done:
                return
            self.send_motion('SCAN')
            self.transition_to('AWAITING_QR')
        elif self.current_state == 'AWAITING_QR':
            if not self.motion_done:
                return
            if not self.qr_received:
                return
            self.qr_received = False
            self.transition_to(RobotState.PLACING)
        elif self.current_state == RobotState.PLACING:
            if not self.motion_done:
                return
            self.send_motion(self.target_bin)
            self.transition_to(RobotState.CONVEYOR_ON)
        elif self.current_state == RobotState.CONVEYOR_ON:
            if not self.motion_done:
                return
            self.send_conveyor('START')
            self.send_motion('HOME')
            self.transition_to(RobotState.COMPLETED)
        elif self.current_state == RobotState.COMPLETED:
            if not self.motion_done:
                return
            self.target_bin = None
            self.motion_done = False
            self.transition_to(RobotState.IDLE)

def main(args=None):
    rclpy.init(args=args)
    node = PickScanPlaceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
"""

files['pick_scan_place/qr_scanner_node.py'] = """import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from zbar_ros.msg import Symbol as ZbarSymbol
    ZBAR_AVAILABLE = True
except ImportError:
    ZBAR_AVAILABLE = False

class QRScannerNode(Node):
    def __init__(self):
        super().__init__('qr_scanner_node')
        self.publisher_ = self.create_publisher(String, '/qr_result', 10)
        if ZBAR_AVAILABLE:
            self.create_subscription(ZbarSymbol, '/barcode', self.zbar_callback, 10)
            self.get_logger().info('QR Scanner using zbar_ros/msg/Symbol')
        else:
            self.create_subscription(String, '/barcode', self.string_callback, 10)
            self.get_logger().warn('zbar_ros not found - using String fallback')

    def zbar_callback(self, msg):
        if msg.data.strip():
            self._publish(msg.data.strip())

    def string_callback(self, msg):
        if msg.data.strip():
            self._publish(msg.data.strip())

    def _publish(self, data):
        self.get_logger().info(f'QR detected: {data}')
        out = String()
        out.data = data
        self.publisher_.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = QRScannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
"""

files['pick_scan_place/motion_planner_node.py'] = """import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import Constraints, JointConstraint
import yaml, os
from ament_index_python.packages import get_package_share_directory

class MotionPlannerNode(Node):
    def __init__(self):
        super().__init__('motion_planner_node')
        self.named_poses = self.load_named_poses()
        self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
        self.create_subscription(String, '/motion_command', self.motion_command_callback, 10)
        self.status_publisher = self.create_publisher(String, '/motion_status', 10)
        self.get_logger().info('Waiting for MoveGroup...')
        while not self.move_group_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().warn('MoveGroup not available yet - retrying...')
        self.get_logger().info(f'MoveGroup connected. Poses: {list(self.named_poses.keys())}')

    def load_named_poses(self):
        try:
            pkg_path = get_package_share_directory('pick_scan_place')
            yaml_path = os.path.join(pkg_path, 'config', 'named_poses.yaml')
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
            return data.get('named_poses', {})
        except Exception as e:
            self.get_logger().error(f'Failed to load named_poses.yaml: {e}')
            return {}

    def motion_command_callback(self, msg):
        command = msg.data.strip().upper()
        pose_key = command.lower()
        if pose_key in self.named_poses:
            self.move_to_pose(pose_key)
        else:
            self.get_logger().warn(f'Unknown command: {command}')
            self.publish_status('FAILED')

    def move_to_pose(self, pose_name):
        self.get_logger().info(f'Planning to: {pose_name}')
        joint_values = self.named_poses[pose_name]['joints']
        goal = MoveGroup.Goal()
        goal.request.group_name = 'ur_manipulator'
        goal.request.num_planning_attempts = 10
        goal.request.allowed_planning_time = 5.0
        goal.request.max_velocity_scaling_factor = 0.3
        goal.request.max_acceleration_scaling_factor = 0.3
        constraints = Constraints()
        constraints.name = pose_name
        for joint_name, joint_value in joint_values.items():
            jc = JointConstraint()
            jc.joint_name = joint_name
            jc.position = float(joint_value)
            jc.tolerance_above = 0.01
            jc.tolerance_below = 0.01
            jc.weight = 1.0
            constraints.joint_constraints.append(jc)
        goal.request.goal_constraints.append(constraints)
        future = self.move_group_client.send_goal_async(goal, feedback_callback=self.feedback_callback)
        future.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info('Executing...')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal REJECTED.')
            self.publish_status('FAILED')
            return
        future = goal_handle.get_result_async()
        future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        error_code = future.result().result.error_code.val
        if error_code == 1:
            self.get_logger().info('Motion SUCCEEDED.')
            self.publish_status('DONE')
        else:
            self.get_logger().error(f'Motion FAILED. Code: {error_code}')
            self.publish_status('FAILED')

    def publish_status(self, status):
        msg = String()
        msg.data = status
        self.status_publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MotionPlannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
"""

files['setup.py'] = """from setuptools import setup
import os
from glob import glob

package_name = 'pick_scan_place'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'), glob('worlds/*.world')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='algamal',
    maintainer_email='fatima25169@gmail.com',
    description='ROS 2 pick-scan-place pipeline',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'qr_scanner      = pick_scan_place.qr_scanner_node:main',
            'decision        = pick_scan_place.decision_node:main',
            'conveyor        = pick_scan_place.conveyor_node:main',
            'pick_scan_place = pick_scan_place.pick_scan_place_node:main',
            'motion_planner  = pick_scan_place.motion_planner_node:main',
        ],
    },
)
"""

os.makedirs(os.path.join(base, 'config'), exist_ok=True)

for path, content in files.items():
    full_path = os.path.join(base, path)
    with open(full_path, 'w') as f:
        f.write(content)
    print(f'Written: {path}')

print('\nAll files written successfully.')
