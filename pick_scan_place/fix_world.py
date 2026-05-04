path = '/home/algamal/ros2_ws/pick_scan_place/worlds/pick_scan_place.world'
world = """<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="pick_scan_place_world">

    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>

    <!-- BIN A (FOOD) - red - to the left -->
    <model name="bin_a">
      <static>true</static>
      <pose>0.5 0.5 0.15 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
          <material><ambient>1 0 0 1</ambient></material>
        </visual>
        <collision name="collision">
          <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
        </collision>
      </link>
    </model>

    <!-- BIN B (HOME) - green - center -->
    <model name="bin_b">
      <static>true</static>
      <pose>0.7 0.0 0.15 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
          <material><ambient>0 1 0 1</ambient></material>
        </visual>
        <collision name="collision">
          <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
        </collision>
      </link>
    </model>

    <!-- BIN C (ELECTRONICS) - blue - to the right -->
    <model name="bin_c">
      <static>true</static>
      <pose>0.5 -0.5 0.15 0 0 0</pose>
      <link name="link">
        <visual name="visual">
          <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
          <material><ambient>0 0 1 1</ambient></material>
        </visual>
        <collision name="collision">
          <geometry><box><size>0.3 0.3 0.3</size></box></geometry>
        </collision>
      </link>
    </model>

  </world>
</sdf>
"""
open(path, 'w').write(world)
print("World file updated.")
