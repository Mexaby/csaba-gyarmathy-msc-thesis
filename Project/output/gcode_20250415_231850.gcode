G21 ; Set units to millimeters
G90 ; Use absolute positioning mode
G92 X0.00 Y0.00 Z0.00 ; Set current position as origin

M300 S30 ; Pen down (prepare to print)
G4 P150 ; Wait 150ms
M300 S50 ; Pen up (initial state)
G4 P150 ; Wait 150ms
M18 ; Disengage drives
M01 ; Registration test (pause for user confirmation)
M17 ; Engage drives if registration successful

; Polyline 1 consisting of 4 points
G1 X0.00 Y0.00 F3500.00
M300 S30.00 ; Pen down
G4 P150 ; Wait 150ms
G1 X0.00 Y511.00 F3500.00
G1 X511.00 Y511.00 F3500.00
G1 X511.00 Y0.00 F3500.00
G1 X0.00 Y0.00 F3500.00
M300 S50.00 ; Pen up
G4 P150 ; Wait 150ms

; End of print job
M300 S50.00 ; Pen up
G4 P150 ; Wait 150ms
M300 S255 ; Turn off servo
G1 X0 Y0 F3500.00
G1 Z0.00 F150.00 ; Raise to finished level
G1 X0.00 Y0.00 F3500.00 ; Return to home
M18 ; Drives off