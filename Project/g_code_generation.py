def contours_to_gcode(contours, feed_rate=3500.0, pen_down=30, pen_up=50, wait_ms=150):
    """
    Convert contours to G-code commands for CNC machines.
    Args:
        contours (list): List of contours, each as a numpy array of (x, y) points.
        feed_rate (float): Feed rate for G1 moves.
        pen_down (int): Servo value for pen down.
        pen_up (int): Servo value for pen up.
        wait_ms (int): Wait time in milliseconds after pen up/down.
    Returns:
        str: G-code as a string.
    """
    gcode = []
    gcode.append("G21 ; Set units to millimeters")
    gcode.append("G90 ; Use absolute positioning mode")
    gcode.append("G92 X0.00 Y0.00 Z0.00 ; Set current position as origin")
    gcode.append("")
    gcode.append("M300 S{:.0f} ; Pen down (prepare to print)".format(pen_down))
    gcode.append(f"G4 P{wait_ms} ; Wait {wait_ms}ms")
    gcode.append("M300 S{:.0f} ; Pen up (initial state)".format(pen_up))
    gcode.append(f"G4 P{wait_ms} ; Wait {wait_ms}ms")
    gcode.append("M18 ; Disengage drives")
    gcode.append("M01 ; Registration test (pause for user confirmation)")
    gcode.append("M17 ; Engage drives if registration successful")
    gcode.append("")
    for idx, contour in enumerate(contours):
        if len(contour) < 2:
            continue
        gcode.append(f"; Polyline {idx+1} consisting of {len(contour)} points")
        start = contour[0][0]
        gcode.append(f"G1 X{start[0]:.2f} Y{-start[1]:.2f} F{feed_rate:.2f}")
        gcode.append("M300 S{:.2f} ; Pen down".format(pen_down))
        gcode.append(f"G4 P{wait_ms} ; Wait {wait_ms}ms")
        for pt in contour[1:]:
            x, y = pt[0]
            gcode.append(f"G1 X{x:.2f} Y{-y:.2f} F{feed_rate:.2f}")
        # Close the contour if it's a closed shape
        if not (contour[0][0] == contour[-1][0]).all():
            x, y = contour[0][0]
            gcode.append(f"G1 X{x:.2f} Y{-y:.2f} F{feed_rate:.2f}")
        gcode.append("M300 S{:.2f} ; Pen up".format(pen_up))
        gcode.append(f"G4 P{wait_ms} ; Wait {wait_ms}ms")
        gcode.append("")
    gcode.append("; End of print job")
    gcode.append("M300 S{:.2f} ; Pen up".format(pen_up))
    gcode.append(f"G4 P{wait_ms} ; Wait {wait_ms}ms")
    gcode.append("M300 S255 ; Turn off servo")
    gcode.append("G1 X0 Y0 F{:.2f}".format(feed_rate))
    gcode.append("G1 Z0.00 F150.00 ; Raise to finished level")
    gcode.append("G1 X0.00 Y0.00 F{:.2f} ; Return to home".format(feed_rate))
    gcode.append("M18 ; Drives off")
    return '\n'.join(gcode)
