path = '/home/algamal/ros2_ws/pick_scan_place/worlds/pick_scan_place.world'

world = """<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="pick_scan_place_world">

    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>

    <!-- BIN A (FOOD) - red - arm rotates left (pan=+1.2) to reach -->
    <model name="bin_a">
      <static>true</static>
      <pose>0.65 0.45 0.15 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>0.25 0.25 0.3</size></box></geometry>
          <material><ambient>1 0 0 1</ambient></material>
        </visual>
        <collision name="collision">
          <geometry><box><size>0.25 0.25 0.3</size></box></geometry>
        </collision>
      </link>
    </model>

    <!-- BIN B (HOME) - green - arm stays centered (pan=0.0) -->
    <model name="bin_b">
      <static>true</static>
      <pose>0.65 0.0 0.15 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>0.25 0.25 0.3</size></box></geometry>
          <material><ambient>0 0.8 0 1</ambient></material>
        </visual>
        <collision name="collision">
          <geometry><box><size>0.25 0.25 0.3</size></box></geometry>
        </collision>
      </link>
    </model>

    <!-- BIN C (ELECTRONICS) - blue - arm rotates right (pan=-1.2) -->
    <model name="bin_c">
      <static>true</static>
      <pose>0.65 -0.45 0.15 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>0.25 0.25 0.3</size></box></geometry>
          <material><ambient>0 0 1 1</ambient></material>
        </visual>
        <collision name="collision">
          <geometry><box><size>0.25 0.25 0.3</size></box></geometry>
        </collision>
      </link>
    </model>

    <!-- PICK OBJECT - orange box the arm picks up -->
    <model name="pick_object">
      <pose>0.35 0.0 0.05 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>0.06 0.06 0.06</size></box></geometry>
          <material><ambient>1 0.5 0 1</ambient></material>
        </visual>
        <collision name="collision">
          <geometry><box><size>0.06 0.06 0.06</size></box></geometry>
        </collision>
        <inertial>
          <mass>0.1</mass>
          <inertia>
            <ixx>0.0001</ixx><ixy>0</ixy><ixz>0</ixz>
            <iyy>0.0001</iyy><iyz>0</iyz><izz>0.0001</izz>
          </inertia>
        </inertial>
      </link>
    </model>

  </world>
</sdf>
"""

open(path, 'w').write(world)
print("World file updated successfully.")
