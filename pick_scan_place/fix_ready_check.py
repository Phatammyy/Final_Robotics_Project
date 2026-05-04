path = '/home/algamal/ros2_ws/pick_scan_place/pick_scan_place/pick_scan_place_node.py'
lines = open(path).readlines()
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'def pipeline_loop(self):' in line:
        new_lines.append('        if not self.planner_ready:\n')
        new_lines.append('            return\n')
open(path, 'w').writelines(new_lines)
print("Done")

# Verify
content = open(path).read()
idx = content.find('def pipeline_loop')
print(content[idx:idx+150])
