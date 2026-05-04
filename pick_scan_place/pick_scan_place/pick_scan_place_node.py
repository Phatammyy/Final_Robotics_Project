"""
pick_scan_place_node.py
=======================
Runs exactly 3 motions per cycle:
  1. PICK  — arm moves to pick position, object tracking starts
  2. SCAN  — arm moves to scan position, QR auto-triggers after 2s
  3. PLACE — arm moves to bin determined by QR result

Then resets and repeats.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class PickScanPlaceNode(Node):

    def __init__(self):
        super().__init__('pick_scan_place_node')

        self.state = 'IDLE'
        self.target_bin = None
        self.motion_done = False
        self.qr_received = False
        self.pipeline_started = False
        self.motion_dispatched = False

        self.create_subscription(String, '/bin_selection',  self.bin_cb,    10)
        self.create_subscription(String, '/motion_status',  self.motion_cb, 10)

        self.state_pub  = self.create_publisher(String, '/robot_state',    10)
        self.motion_pub = self.create_publisher(String, '/motion_command', 10)

        self.create_timer(0.5, self.loop)
        self.get_logger().info('Pick-Scan-Place node started.')

    # ------------------------------------------------------------------ #

    def bin_cb(self, msg):
        self.target_bin = msg.data.strip()
        self.qr_received = True
        self.get_logger().info(f'QR received → {self.target_bin}')

    def motion_cb(self, msg):
        status = msg.data.strip().upper()
        if status == 'READY':
            if not self.pipeline_started:
                self.pipeline_started = True
                self.get_logger().info('Planner ready — starting pipeline.')
        elif status == 'DONE':
            self.motion_done = True
            self.motion_dispatched = False
            self.get_logger().info('Motion done.')
        elif status == 'FAILED':
            self.get_logger().error('Motion failed — resetting.')
            self.motion_dispatched = False
            self.pipeline_started = False
            self._go('IDLE')

    def _send(self, command):
        """Send a motion command exactly once."""
        if self.motion_dispatched:
            return
        self.motion_done = False
        self.motion_dispatched = True
        msg = String()
        msg.data = command
        self.motion_pub.publish(msg)
        self.get_logger().info(f'Sending: {command}')

    def _go(self, new_state):
        self.get_logger().info(f'{self.state} → {new_state}')
        self.state = new_state
        self.motion_dispatched = False
        msg = String()
        msg.data = new_state
        self.state_pub.publish(msg)

    # ------------------------------------------------------------------ #

    def loop(self):
        if not self.pipeline_started:
            return

        # ── Step 1: PICK ──────────────────────────────────────────────
        if self.state == 'IDLE':
            self._go('PICKING')
            self._send('pick')

        # ── Step 2: SCAN ──────────────────────────────────────────────
        elif self.state == 'PICKING':
            if not self.motion_done:
                return
            # Object is now "in gripper" — tracker activates on SCANNING
            self._go('SCANNING')
            self._send('scan')

        # ── Wait for QR ───────────────────────────────────────────────
        elif self.state == 'SCANNING':
            if not self.motion_done:
                return
            self._go('AWAITING_QR')

        elif self.state == 'AWAITING_QR':
            if not self.qr_received:
                return
            self.qr_received = False
            self._go('PLACING')

        # ── Step 3: PLACE ─────────────────────────────────────────────
        elif self.state == 'PLACING':
            self._send(self.target_bin)
            self._go('DROPPING')

        elif self.state == 'DROPPING':
            if not self.motion_done:
                return
            # Cycle complete — reset for next round
            self.target_bin = None
            self.motion_done = False
            self.pipeline_started = False
            self._go('IDLE')


def main(args=None):
    rclpy.init(args=args)
    node = PickScanPlaceNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
