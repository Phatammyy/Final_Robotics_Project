base = '/home/algamal/ros2_ws/pick_scan_place'

# Add to setup.py
setup = open(f'{base}/setup.py').read()
old = "            'motion_planner  = pick_scan_place.motion_planner_node:main',"
new = "            'motion_planner  = pick_scan_place.motion_planner_node:main',\n            'object_tracker  = pick_scan_place.object_tracker_node:main',"
if old in setup:
    setup = setup.replace(old, new)
    open(f'{base}/setup.py', 'w').write(setup)
    print("Fixed setup.py")
else:
    print("ERROR: setup.py pattern not found")

# Add to launch file
launch = open(f'{base}/launch/robot.launch.py').read()
old2 = "            Node(package='pick_scan_place', executable='motion_planner',"
new2 = "            Node(package='pick_scan_place', executable='object_tracker',\n                 parameters=[{'use_sim_time': True}], output='screen'),\n            Node(package='pick_scan_place', executable='motion_planner',"
if old2 in launch:
    launch = launch.replace(old2, new2)
    open(f'{base}/launch/robot.launch.py', 'w').write(launch)
    print("Fixed launch file")
else:
    print("ERROR: launch pattern not found")

print("Done.")
