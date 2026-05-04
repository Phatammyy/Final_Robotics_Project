import os
base = '/home/algamal/ros2_ws/pick_scan_place'

# FIX 1: motion_planner_node - publish 'READY' when connected
motion_planner = open(f'{base}/pick_scan_place/motion_planner_node.py').read()
old = "        self.get_logger().info(f'MoveGroup connected. Poses: {list(self.named_poses.keys())}')"
new = """        self.get_logger().info(f'MoveGroup connected. Poses: {list(self.named_poses.keys())}')
        # Publish READY so pick_scan_place_node knows it can start
        ready_msg = String()
        ready_msg.data = 'READY'
        self.status_publisher.publish(ready_msg)"""
if old in motion_planner:
    motion_planner = motion_planner.replace(old, new)
    open(f'{base}/pick_scan_place/motion_planner_node.py', 'w').write(motion_planner)
    print("Fixed motion_planner_node.py")
else:
    print("ERROR: motion_planner pattern not found")

# FIX 2: pick_scan_place_node - wait for READY before starting
pipeline = open(f'{base}/pick_scan_place/pick_scan_place_node.py').read()
old2 = "        self.timer = self.create_timer(0.5, self.pipeline_loop)\n        self.get_logger().info('Pick-Scan-Place Node started.')"
new2 = """        self.planner_ready = False
        self.timer = self.create_timer(0.5, self.pipeline_loop)
        self.get_logger().info('Pick-Scan-Place Node started. Waiting for motion planner...')"""
old3 = "    def pipeline_loop(self):\n        if self.current_state == RobotState.IDLE:"
new3 = """    def pipeline_loop(self):
        if not self.planner_ready:
            return
        if self.current_state == RobotState.IDLE:"""
old4 = "        if status == 'DONE':\n            self.motion_done = True"
new4 = """        if status == 'READY':
            self.planner_ready = True
            self.get_logger().info('Motion planner ready - pipeline starting!')
        elif status == 'DONE':
            self.motion_done = True"""

if old2 in pipeline:
    pipeline = pipeline.replace(old2, new2)
    print("Fixed pipeline node - added planner_ready flag")
else:
    print("ERROR: pipeline pattern 1 not found")

if old3 in pipeline:
    pipeline = pipeline.replace(old3, new3)
    print("Fixed pipeline node - added ready check")
else:
    print("ERROR: pipeline pattern 2 not found")

if old4 in pipeline:
    pipeline = pipeline.replace(old4, new4)
    print("Fixed pipeline node - added READY handler")
else:
    print("ERROR: pipeline pattern 3 not found")

open(f'{base}/pick_scan_place/pick_scan_place_node.py', 'w').write(pipeline)

# FIX 3: Replace URDF with mesh backup + ros2_control block
mesh_urdf = open(f'{base}/urdf/ur5_mesh_backup.urdf').read()
ros2_control_block = """
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
      <parameters>/home/algamal/ros2_ws/install/pick_scan_place/share/pick_scan_place/config/ros2_controllers.yaml</parameters>
    </plugin>
  </gazebo>
"""
mesh_urdf = mesh_urdf.replace('</robot>', ros2_control_block + '</robot>')
open(f'{base}/urdf/ur5_simple.urdf', 'w').write(mesh_urdf)
print("Fixed URDF - mesh with ros2_control block")
print("\nAll fixes applied.")
