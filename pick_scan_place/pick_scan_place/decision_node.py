# decision_node.py
# This node receives decoded QR code data and decides which bin
# the object should be placed in based on the QR content.
# QR codes encode the object category: FOOD, HOME, or ELECTRONICS
# Each category maps to a specific bin (BIN_A, BIN_B, or BIN_C).

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DecisionNode(Node):
    """Node that reads QR data and decides the correct placement bin."""

    def __init__(self):
        super().__init__('decision_node')

        # Subscribe to the QR result topic from qr_scanner_node
        self.subscription = self.create_subscription(
            String,
            '/qr_result',
            self.qr_result_callback,
            10
        )

        # Publisher to send bin selection to the pick_scan_place_node
        self.publisher_ = self.create_publisher(String, '/bin_selection', 10)

        # Define bin mapping based on QR code content
        # FOOD     → BIN_A
        # HOME     → BIN_B
        # ELECTRONICS → BIN_C
        # Unknown QR content defaults to BIN_A
        self.bin_map = {
            'FOOD':         'BIN_A',
            'HOME':         'BIN_B',
            'ELECTRONICS':  'BIN_C',
        }

        self.get_logger().info('Decision Node started. Waiting for QR results...')
        self.get_logger().info('Bin mapping: FOOD→BIN_A, HOME→BIN_B, ELECTRONICS→BIN_C')

    def qr_result_callback(self, msg):
        """Called when a QR result is received. Determines correct bin."""

        # Clean and standardize the QR data
        qr_data = msg.data.strip().upper()
        self.get_logger().info(f'Received QR data: {qr_data}')

        # Look up the bin for this QR code
        # Default to BIN_A if QR content is not recognized
        bin_choice = self.bin_map.get(qr_data, 'BIN_A')
        self.get_logger().info(f'Decision: Place object in {bin_choice}')

        # Publish the bin selection for the pipeline node
        bin_msg = String()
        bin_msg.data = bin_choice
        self.publisher_.publish(bin_msg)


def main(args=None):
    rclpy.init(args=args)
    node = DecisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()