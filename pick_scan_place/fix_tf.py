path = '/home/algamal/ros2_ws/pick_scan_place/launch/robot.launch.py'
content = open(path).read()

old = "        Node(package='robot_state_publisher', executable='robot_state_publisher',"
new = """        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='world_to_base',
            arguments=['0', '0', '0', '0', '0', '0', 'world', 'base_link'],
            output='screen'
        ),
        Node(package='robot_state_publisher', executable='robot_state_publisher',"""

if old in content:
    content = content.replace(old, new)
    open(path, 'w').write(content)
    print("Fixed - added world->base_link static transform")
else:
    print("ERROR: pattern not found")
