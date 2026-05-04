path = '/home/algamal/ros2_ws/pick_scan_place/urdf/ur5_simple.urdf'
lines = open(path).readlines()
new_lines = []
for line in lines:
    if 'parameters' in line:
        new_lines.append('      <parameters>/home/algamal/ros2_ws/install/pick_scan_place/share/pick_scan_place/config/ros2_controllers.yaml</parameters>\n')
    else:
        new_lines.append(line)
open(path, 'w').writelines(new_lines)
print("Done")
for l in new_lines:
    if 'parameters' in l:
        print(repr(l))
