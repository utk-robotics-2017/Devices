import threading
from input_devices.inputs import devices

class GamePad:
    def __init__(self, number):
        self.device = devices.gamepads[number]
        self.thumbstickDeadzone = 8000.0
        self.thumbstickMax = 32768.0
        self.triggerDeadzone = 5.0
        self.triggerMax = 255.0
        self.leftStick = { "x": 0, "y": 0 }
        self.rightStick = { "x": 0, "y": 0 }
        self.leftTrigger = 0
        self.rightTrigger = 0
        self.buttons = {
            "D_Up": 0,
            "D_Down": 0,
            "D_Left": 0,
            "D_Right": 0,
            "Start": 0,
            "Select": 0,
            "Left_Thumb": 0,
            "Right_Thumb": 0,
            "Left_Bumper": 0,
            "Right_Bumper": 0,
            "A": 0,
            "B": 0,
            "X": 0,
            "Y": 0
        }
        self.updateThread = threading.Thread(target=self.update)
        self.updateThread.daemon = True
        self.updateThread.start()

    def update(self):
        while True:
            events = self.device.read()
            for event in events:

                #Face buttons
                if event.ev_type == "Key":
                    if event.code == "BTN_SOUTH":
                        self.buttons["A"] = event.state
                    elif event.code == "BTN_EAST":
                        self.buttons["B"] = event.state
                    elif event.code == "BTN_NORTH":
                        self.buttons["Y"] = event.state
                    elif event.code == "BTN_WEST":
                        self.buttons["X"] = event.state
                    elif event.code == "BTN_THUMBL":
                        self.buttons["Left_Thumb"] = event.state
                    elif event.code == "BTN_THUMBR":
                        self.buttons["Right_Thumb"] = event.state
                    elif event.code == "BTN_TL":
                        self.buttons["Left_Bumper"] = event.state
                    elif event.code == "BTN_TR":
                        self.buttons["Right_Bumper"] = event.state
                    elif event.code == "BTN_SELECT":
                        self.buttons["Start"] = event.state
                    elif event.code == "BTN_START":
                        self.buttons["Select"] = event.state

                #Thumbsticks, triggers, d-pad
                if event.ev_type == "Absolute":

                    #Thumbsticks
                    if (event.code == "ABS_X" or \
                        event.code == "ABS_Y" or \
                        event.code == "ABS_RX" or \
                        event.code == "ABS_RY"):

                        mod = 1
                        if event.state < 0:
                            mod = -1
                        val = (event.state * mod - self.thumbstickDeadzone) / (self.thumbstickMax - self.thumbstickDeadzone)
                        val = max(min(val, 1), 0) * mod

                        if event.code == "ABS_X":
                            self.leftStick["x"] = val
                        elif event.code == "ABS_Y":
                            self.leftStick["y"] = val
                        elif event.code == "ABS_RX":
                            self.rightStick["x"] = val
                        elif event.code == "ABS_RY":
                            self.rightStick["y"] = val

                    #Triggers
                    elif (event.code == "ABS_Z" or \
                          event.code == "ABS_RZ"):

                        val = (event.state - self.triggerDeadzone) / (self.triggerMax - self.triggerDeadzone)
                        val = max(min(val, 1), 0)

                        if event.code == "ABS_Z":
                            self.leftTrigger = val
                        elif event.code == "ABS_RZ":
                            self.rightTrigger = val

                    #D-Pad Up and Down
                    elif event.code == "ABS_HAT0Y":
                        if event.state == 1:
                            self.buttons["D_Down"] = 1
                        elif event.state == -1:
                            self.buttons["D_Up"] = 1
                        else:
                            self.buttons["D_Up"] = 0
                            self.buttons["D_Down"] = 0

                    #D-Pad Left and Right
                    elif event.code == "ABS_HAT0X":
                        if event.state == 1:
                            self.buttons["D_Right"] = 1
                        elif event.state == -1:
                            self.buttons["D_Left"] = 1
                        else:
                            self.buttons["D_Right"] = 0
                            self.buttons["D_Left"] = 0
