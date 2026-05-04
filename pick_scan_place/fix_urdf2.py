path = '/home/algamal/ros2_ws/pick_scan_place/urdf/ur5_simple.urdf'

block = """
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

content = open(path).read()
content = content.replace('</robot>', block + '</robot>')
open(path, 'w').write(content)
print("Done")

# Verify
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'ros2_control' in line or 'gazebo_ros2_control' in line:
        print(f"Line {i}: {line.strip()}")
