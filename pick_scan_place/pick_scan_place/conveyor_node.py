# conveyor_node.py
# This node controls the conveyor belt during the pick-scan-place pipeline.
# It listens for conveyor commands (START/STOP) and publishes the belt velocity.
# The conveyor must stop before the robot picks an object.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64


class ConveyorNode(Node):
    """Node that controls the conveyor belt speed based on commands."""

    def __init__(self):
        super().__init__('conveyor_node')

        # Subscribe to conveyor command topic
        self.subscription = self.create_subscription(
            String,
            '/conveyor_command',
            self.command_callback,
            10
        )

        # Publisher to set conveyor belt velocity in Gazebo
        self.velocity_publisher = self.create_publisher(
            Float64,
            '/conveyor/velocity',
            10
        )

        # Publisher to report current conveyor status
        self.status_publisher = self.create_publisher(
            String,
            '/conveyor_status',
            10
        )

        # Track current conveyor state
        self.is_running = False

        self.get_logger().info('Conveyor Node started. Belt is stopped.')

    def command_callback(self, msg):
        """Called when a conveyor command is received (START or STOP)."""

        command = msg.data.strip().upper()

        if command == 'START':
            # Start the conveyor belt at a fixed speed
            self.set_belt_velocity(0.5)
            self.is_running = True
            self.get_logger().info('Conveyor belt STARTED')
            self.publish_status('RUNNING')

        elif command == 'STOP':
            # Stop the conveyor belt completely before robot picks
            self.set_belt_velocity(0.0)
            self.is_running = False
            self.get_logger().info('Conveyor belt STOPPED')
            self.publish_status('STOPPED')

        else:
            self.get_logger().warn(f'Unknown conveyor command: {command}')

    def set_belt_velocity(self, velocity):
        """Publishes a velocity value to the conveyor belt controller."""
        vel_msg = Float64()
        vel_msg.data = velocity
        self.velocity_publisher.publish(vel_msg)

    def publish_status(self, status):
        """Publishes the current conveyor status for other nodes to read."""
        status_msg = String()
        status_msg.data = status
        self.status_publisher.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ConveyorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()