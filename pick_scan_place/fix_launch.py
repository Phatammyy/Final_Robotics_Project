path = '/home/algamal/ros2_ws/pick_scan_place/launch/robot.launch.py'
content = open(path).read()

old = "robot_description = ParameterValue(Command(['cat ', urdf_file]), value_type=str)"

new = """robot_description = ParameterValue(
    Command([
        'xacro ',
        '/home/algamal/ros2_ws/install/ur_description/share/ur_description/urdf/ur.urdf.xacro',
        ' ur_type:=ur5',
        ' name:=ur',
    ]),
    value_type=str
)"""

if old in content:
    content = content.replace(old, new)
    open(path, 'w').write(content)
    print("Done - line replaced successfully")
else:
    print("ERROR - line not found, no changes made")
