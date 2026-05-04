path = '/home/algamal/ros2_ws/pick_scan_place/urdf/ur5_simple.urdf'
content = open(path).read()

# Replace visual geometry for each link with real UR5 meshes
# We only change the <visual> block, keeping collision and inertial intact

visuals = {
    'base_link': '''    <visual>
      <origin rpy="0.0 0.0 3.141592653589793" xyz="0.0 0.0 0.0"/>
      <geometry><mesh filename="package://ur_description/meshes/ur5/visual/base.dae"/></geometry>
    </visual>''',

    'shoulder_link': '''    <visual>
      <origin rpy="0.0 0.0 3.141592653589793" xyz="0.0 0.0 0.0"/>
      <geometry><mesh filename="package://ur_description/meshes/ur5/visual/shoulder.dae"/></geometry>
    </visual>''',

    'upper_arm_link': '''    <visual>
      <origin rpy="1.5707963267948966 0.0 -1.5707963267948966" xyz="0.0 0.0 0.13585"/>
      <geometry><mesh filename="package://ur_description/meshes/ur5/visual/upperarm.dae"/></geometry>
    </visual>''',

    'forearm_link': '''    <visual>
      <origin rpy="1.5707963267948966 0.0 -1.5707963267948966" xyz="0.0 0.0 0.0165"/>
      <geometry><mesh filename="package://ur_description/meshes/ur5/visual/forearm.dae"/></geometry>
    </visual>''',

    'wrist_1_link': '''    <visual>
      <origin rpy="1.5707963267948966 0.0 0.0" xyz="0.0 0.0 -0.093"/>
      <geometry><mesh filename="package://ur_description/meshes/ur5/visual/wrist1.dae"/></geometry>
    </visual>''',

    'wrist_2_link': '''    <visual>
      <origin rpy="0.0 0.0 0.0" xyz="0.0 0.0 -0.095"/>
      <geometry><mesh filename="package://ur_description/meshes/ur5/visual/wrist2.dae"/></geometry>
    </visual>''',

    'wrist_3_link': '''    <visual>
      <origin rpy="1.5707963267948966 0.0 0.0" xyz="0.0 0.0 -0.0818"/>
      <geometry><mesh filename="package://ur_description/meshes/ur5/visual/wrist3.dae"/></geometry>
    </visual>''',
}

old_visuals = {
    'base_link': '    <visual><geometry><cylinder radius="0.075" length="0.05"/></geometry>\n      <material name="dark_gray"><color rgba="0.3 0.3 0.3 1"/></material></visual>',
    'shoulder_link': '    <visual><geometry><sphere radius="0.06"/></geometry>\n      <material name="orange"><color rgba="0.9 0.5 0.1 1"/></material></visual>',
    'upper_arm_link': '    <visual><origin xyz="0 0 0.213" rpy="0 0 0"/>\n      <geometry><cylinder radius="0.04" length="0.425"/></geometry>\n      <material name="orange"><color rgba="0.9 0.5 0.1 1"/></material></visual>',
    'forearm_link': '    <visual><origin xyz="0 0 0.196" rpy="0 0 0"/>\n      <geometry><cylinder radius="0.03" length="0.392"/></geometry>\n      <material name="orange"><color rgba="0.9 0.5 0.1 1"/></material></visual>',
    'wrist_1_link': '    <visual><geometry><sphere radius="0.035"/></geometry>\n      <material name="dark_orange"><color rgba="0.7 0.3 0.1 1"/></material></visual>',
    'wrist_2_link': '    <visual><geometry><sphere radius="0.035"/></geometry>\n      <material name="dark_orange"><color rgba="0.7 0.3 0.1 1"/></material></visual>',
    'wrist_3_link': '    <visual><geometry><sphere radius="0.03"/></geometry>\n      <material name="dark_orange"><color rgba="0.7 0.3 0.1 1"/></material></visual>',
}

for link, old_vis in old_visuals.items():
    if old_vis in content:
        content = content.replace(old_vis, visuals[link])
        print(f"Fixed visual for: {link}")
    else:
        print(f"NOT FOUND: {link}")

open(path, 'w').write(content)
print("\nDone. Visuals updated.")
