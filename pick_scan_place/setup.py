from setuptools import setup
import os
from glob import glob

package_name = 'pick_scan_place'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        (os.path.join('share', package_name, 'worlds'),
            glob('worlds/*.world')),
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.urdf')),
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='algamal',
    maintainer_email='fatima25169@gmail.com',
    description='ROS 2 UR5 pick-scan-place pipeline with MoveIt 2 and Gazebo',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'qr_scanner      = pick_scan_place.qr_scanner_node:main',
            'decision        = pick_scan_place.decision_node:main',
            'conveyor        = pick_scan_place.conveyor_node:main',
            'pick_scan_place = pick_scan_place.pick_scan_place_node:main',
            'motion_planner  = pick_scan_place.motion_planner_node:main',
            'object_tracker  = pick_scan_place.object_tracker_node:main',
        ],
    },
)
