path = '/home/algamal/ros2_ws/pick_scan_place/pick_scan_place/pick_scan_place_node.py'
content = open(path).read()

# Remove the old ready check and set_ready timer leftovers
content = content.replace('        if not self.ready:\n            return\n', '')
content = content.replace('        self.ready = False\n        self.create_timer(10.0, self.set_ready)\n', '')
content = content.replace('        self.ready = False\n        self.create_timer(5.0, self.set_ready)\n', '')
content = content.replace('    def set_ready(self):\n        if not self.ready:\n            self.ready = True\n            self.get_logger().info(\'Pipeline ready - starting.\')\n\n', '')

open(path, 'w').write(content)
print("Done")

# Verify pipeline_loop area
idx = content.find('def pipeline_loop')
print(content[idx:idx+200])
