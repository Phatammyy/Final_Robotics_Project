import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from gazebo_msgs.srv import SetEntityState
from gazebo_msgs.msg import EntityState
from geometry_msgs.msg import Pose
from moveit_msgs.srv import GetPositionFK
from moveit_msgs.msg import RobotState as MoveItRobotState
import threading

SPAWN_X = -0.15
SPAWN_Y =  0.45
SPAWN_Z =  0.05
GRIP_OFFSET_Z = -0.05

CARRY_STATES = {'PICKING', 'SCANNING', 'AWAITING_QR', 'PLACING', 'DROPPING'}


class ObjectTrackerNode(Node):

    def __init__(self):
        super().__init__('object_tracker_node')
        self.carrying = False
        self.fk_pending = False
        self.current_joints = {}
        self.lock = threading.Lock()

        self.create_subscription(String,     '/robot_state',  self.state_callback, 10)
        self.create_subscription(JointState, '/joint_states', self.joint_callback, 10)

        self.set_state_client = self.create_client(SetEntityState, '/gazebo/set_entity_state')
        self.fk_client        = self.create_client(GetPositionFK,  '/compute_fk')

        self.create_timer(0.1, self.update)
        self.get_logger().info('Object Tracker Node started.')

    def state_callback(self, msg):
        state = msg.data.strip().upper()
        if state in CARRY_STATES:
            if not self.carrying:
                self.carrying = True
                self.get_logger().info('Object tracking: ON')
        elif state == 'IDLE':
            self.carrying = False
            self.fk_pending = False
            self._teleport(SPAWN_X, SPAWN_Y, SPAWN_Z)
            self.get_logger().info('Object tracking: OFF — reset to spawn')

    def joint_callback(self, msg):
        with self.lock:
            for i, name in enumerate(msg.name):
                self.current_joints[name] = msg.position[i]

    def update(self):
        if not self.carrying:
            return
        if self.fk_pending:
            return
        if not self.current_joints:
            return
        if not self.fk_client.service_is_ready():
            return
        if not self.set_state_client.service_is_ready():
            return

        req = GetPositionFK.Request()
        req.header.frame_id = 'base_link'
        req.fk_link_names = ['tool0']

        rs = MoveItRobotState()
        joints = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
                  'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        with self.lock:
            for j in joints:
                if j in self.current_joints:
                    rs.joint_state.name.append(j)
                    rs.joint_state.position.append(self.current_joints[j])

        req.robot_state = rs
        self.fk_pending = True
        future = self.fk_client.call_async(req)
        future.add_done_callback(self._fk_done)

    def _fk_done(self, future):
        self.fk_pending = False
        try:
            result = future.result()
            if result.error_code.val != 1:
                return
            p = result.pose_stamped[0].pose.position
            self._teleport(p.x, p.y, p.z + GRIP_OFFSET_Z)
        except Exception as e:
            self.get_logger().error(f'FK error: {e}')

    def _teleport(self, x, y, z):
        if not self.set_state_client.service_is_ready():
            return
        req = SetEntityState.Request()
        state = EntityState()
        state.name = 'pick_object'
        state.reference_frame = 'world'
        pose = Pose()
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z
        pose.orientation.w = 1.0
        state.pose = pose
        req.state = state
        self.set_state_client.call_async(req)


def main(args=None):
    rclpy.init(args=args)
    from rclpy.executors import MultiThreadedExecutor
    node = ObjectTrackerNode()
    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)
    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
