import os
base = '/home/algamal/ros2_ws/pick_scan_place'

# FIX motion_planner_node - publish READY when connected
mp = open(f'{base}/pick_scan_place/motion_planner_node.py').read()
old = "        self.get_logger().info(f'MoveGroup connected. Poses: {list(self.named_poses.keys())}')"
new = """        self.get_logger().info(f'MoveGroup connected. Poses: {list(self.named_poses.keys())}')
        ready_msg = String()
        ready_msg.data = 'READY'
        self.status_publisher.publish(ready_msg)"""
if old in mp:
    mp = mp.replace(old, new)
    open(f'{base}/pick_scan_place/motion_planner_node.py', 'w').write(mp)
    print("Fixed motion_planner_node")
else:
    print("motion_planner pattern not found")

# FIX pick_scan_place_node - wait for READY
ps = open(f'{base}/pick_scan_place/pick_scan_place_node.py').read()

# Add planner_ready flag
old2 = "        self.timer = self.create_timer(0.5, self.pipeline_loop)\n        self.get_logger().info('Pick-Scan-Place Node started.')"
new2 = "        self.planner_ready = False\n        self.timer = self.create_timer(0.5, self.pipeline_loop)\n        self.get_logger().info('Pick-Scan-Place Node started. Waiting for motion planner...')"
if old2 in ps:
    ps = ps.replace(old2, new2)
    print("Fixed pipeline - added planner_ready flag")
else:
    print("pipeline pattern 1 not found")

# Add READY handler to motion_status_callback
old3 = "        if status == 'DONE':\n            self.motion_done = True"
new3 = "        if status == 'READY':\n            self.planner_ready = True\n            self.get_logger().info('Motion planner ready - pipeline starting!')\n        elif status == 'DONE':\n            self.motion_done = True"
if old3 in ps:
    ps = ps.replace(old3, new3)
    print("Fixed pipeline - added READY handler")
else:
    print("pipeline pattern 2 not found")

# Add planner_ready check in pipeline_loop
old4 = "    def pipeline_loop(self):\n        if self.current_state == RobotState.IDLE:"
new4 = "    def pipeline_loop(self):\n        if not self.planner_ready:\n            return\n        if self.current_state == RobotState.IDLE:"
if old4 in ps:
    ps = ps.replace(old4, new4)
    print("Fixed pipeline - added ready check in loop")
else:
    print("pipeline pattern 3 not found")

open(f'{base}/pick_scan_place/pick_scan_place_node.py', 'w').write(ps)
print("\nAll done.")
