import rclpy
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
        # Publish READY repeatedly to ensure pick_scan_place_node receives it
        self.ready_count = 0
        self.create_timer(0.5, self.publish_ready)

    def publish_ready(self):
        if self.ready_count < 6:
            ready_msg = String()
            ready_msg.data = 'READY'
            self.status_publisher.publish(ready_msg)
            self.ready_count += 1

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
