"""
qr_scanner_node.py
==================
Handles QR code detection for the pick-scan-place pipeline.

Two modes:
1. REAL MODE — if zbar_ros is available, subscribes to /barcode and
   forwards decoded symbols to /qr_result as before.

2. AUTO-SIM MODE (active when zbar_ros is not available) — the plain
   orange pick_object in Gazebo Classic has no QR texture, so a real
   camera scan will never produce a result. Instead, this node watches
   /robot_state and when it sees AWAITING_QR it waits a short delay
   (simulating scan time) then publishes a hardcoded category so the
   pipeline can continue automatically without any manual commands.

   The simulated category cycles through FOOD → HOME → ELECTRONICS on
   successive picks so you can observe all three bin placements in one
   continuous run. Change AUTO_SIM_CATEGORIES to fix it to one value.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

try:
    from zbar_ros.msg import Symbol as ZbarSymbol
    ZBAR_AVAILABLE = True
except ImportError:
    ZBAR_AVAILABLE = False

# Categories to cycle through in simulation mode.
# Edit this list to change what gets "scanned" each cycle.
AUTO_SIM_CATEGORIES = ['FOOD', 'HOME', 'ELECTRONICS']

# How long (seconds) to wait at SCAN pose before publishing the result.
# Gives the arm time to settle and makes the demo look deliberate.
AUTO_SIM_DELAY = 2.0


class QRScannerNode(Node):

    def __init__(self):
        super().__init__('qr_scanner_node')

        self.publisher_ = self.create_publisher(String, '/qr_result', 10)
        self._scan_timer = None
        self._already_triggered = False
        self._cycle_index = 0

        if ZBAR_AVAILABLE:
            self.create_subscription(
                ZbarSymbol, '/barcode', self.zbar_callback, 10)
            self.get_logger().info(
                'QR Scanner: REAL mode — using zbar_ros/msg/Symbol')
        else:
            # Auto-sim: watch the pipeline state and trigger on AWAITING_QR.
            self.create_subscription(
                String, '/robot_state', self.state_callback, 10)
            self.get_logger().warn(
                'QR Scanner: AUTO-SIM mode — zbar_ros not found. '
                f'Will auto-publish after {AUTO_SIM_DELAY}s at scan pose. '
                f'Cycle: {AUTO_SIM_CATEGORIES}')

    # ------------------------------------------------------------------ #
    # Real mode                                                            #
    # ------------------------------------------------------------------ #

    def zbar_callback(self, msg):
        if msg.data.strip():
            self._publish(msg.data.strip())

    # ------------------------------------------------------------------ #
    # Auto-sim mode                                                        #
    # ------------------------------------------------------------------ #

    def state_callback(self, msg):
        state = msg.data.strip().upper()

        if state == 'AWAITING_QR' and not self._already_triggered:
            self._already_triggered = True
            self.get_logger().info(
                f'Arm at scan pose — publishing QR result in '
                f'{AUTO_SIM_DELAY}s...')
            # One-shot timer: fires once after the delay then cancels itself.
            self._scan_timer = self.create_timer(
                AUTO_SIM_DELAY, self._auto_publish)

        elif state in ['IDLE', 'PICKING']:
            # Reset for the next cycle.
            self._already_triggered = False
            if self._scan_timer is not None:
                self._scan_timer.cancel()
                self._scan_timer = None

    def _auto_publish(self):
        """Called once after AUTO_SIM_DELAY when arm is at scan pose."""
        if self._scan_timer is not None:
            self._scan_timer.cancel()
            self._scan_timer = None

        category = AUTO_SIM_CATEGORIES[
            self._cycle_index % len(AUTO_SIM_CATEGORIES)]
        self._cycle_index += 1
        self.get_logger().info(f'Auto-sim QR result: {category}')
        self._publish(category)

    # ------------------------------------------------------------------ #
    # Shared                                                               #
    # ------------------------------------------------------------------ #

    def _publish(self, data):
        out = String()
        out.data = data
        self.publisher_.publish(out)
        self.get_logger().info(f'QR published: {data}')


def main(args=None):
    rclpy.init(args=args)
    node = QRScannerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
