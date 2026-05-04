# robot_states.py
# This file defines all possible states for the robot during the pick-scan-place pipeline.
# Each state represents a specific phase of the robot's operation.

class RobotState:
    """Enum-like class defining all robot operation states."""
    
    IDLE        = "IDLE"        # Robot is waiting for a new task
    MOVING      = "MOVING"      # Robot is moving to a target position
    PICKING     = "PICKING"     # Robot is picking up an object
    SCANNING    = "SCANNING"    # Robot is scanning the QR code
    PLACING     = "PLACING"     # Robot is placing the object in a bin
    CONVEYOR_ON = "CONVEYOR_ON" # Conveyor belt is running
    CONVEYOR_OFF= "CONVEYOR_OFF"# Conveyor belt is stopped
    ERROR       = "ERROR"       # An error has occurred
    COMPLETED   = "COMPLETED"   # Task completed successfully