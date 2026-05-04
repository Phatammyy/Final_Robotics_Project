path = '/home/algamal/ros2_ws/pick_scan_place/urdf/ur5_simple.urdf'
content = open(path).read()

# Fix joint origins to match official UR5 kinematics
fixes = [
    # shoulder_pan: parent should be base_link, origin correct
    # shoulder_lift: origin correct
    # elbow: X axis not Y axis
    ('    <origin xyz=\"0 -0.425 0\" rpy=\"0 0 0\"/><axis xyz=\"0 0 1\"/>',
     '    <origin xyz=\"-0.425 0 0\" rpy=\"0 0 0\"/><axis xyz=\"0 0 1\"/>'),
    # wrist_1: fix origin
    ('    <origin xyz=\"0 -0.392 0\" rpy=\"1.5708 0 0\"/><axis xyz=\"0 0 1\"/>',
     '    <origin xyz=\"-0.39225 0 0.10915\" rpy=\"0 0 0\"/><axis xyz=\"0 0 1\"/>'),
    # wrist_2: fix origin
    ('    <origin xyz=\"0 0 0.109\" rpy=\"-1.5708 0 0\"/><axis xyz=\"0 0 1\"/>',
     '    <origin xyz=\"0 -0.09465 0\" rpy=\"1.5708 0 0\"/><axis xyz=\"0 0 1\"/>'),
    # wrist_3: fix origin
    ('    <origin xyz=\"0 0.093 0\" rpy=\"1.5708 0 0\"/><axis xyz=\"0 0 1\"/>',
     '    <origin xyz=\"0 0.0823 0\" rpy=\"1.5708 3.14159 3.14159\"/><axis xyz=\"0 0 1\"/>'),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"Fixed: {old.strip()[:50]}")
    else:
        print(f"NOT FOUND: {old.strip()[:50]}")

open(path, 'w').write(content)
print("Done")
