path = '/home/algamal/ros2_ws/pick_scan_place/pick_scan_place/pick_scan_place_node.py'
content = open(path).read()

old = "        self.timer = self.create_timer(0.5, self.pipeline_loop)"
new = "        self.ready = False\n        self.create_timer(5.0, self.set_ready)\n        self.timer = self.create_timer(0.5, self.pipeline_loop)"

content = content.replace(old, new)

old = "    def pipeline_loop(self):\n        if self.current_state == RobotState.IDLE:"
new = "    def set_ready(self):\n        self.ready = True\n        self.get_logger().info('Pipeline ready - starting.')\n\n    def pipeline_loop(self):\n        if not self.ready:\n            return\n        if self.current_state == RobotState.IDLE:"

content = content.replace(old, new)
open(path, 'w').write(content)
print("Done")

