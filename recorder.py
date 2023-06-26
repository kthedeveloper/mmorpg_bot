import mouse
import keyboard
import time
import json


class ActionRecorder:
    def __init__(self):
        self.actions = []
        self.start_time = None
        self.last_mouse_pos = None
        self.mouse_click_event = True

    def record_mouse_move(self, event):
        if isinstance(event, mouse.MoveEvent):

            x, y = event.x, event.y

            timestamp = time.time() - self.start_time

            if self.last_mouse_pos is not None:
                dx = x - self.last_mouse_pos[0]
                dy = y - self.last_mouse_pos[1]
                action = {'type': 'mouse_move', 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'timestamp': timestamp}
                self.actions.append(action)

            self.last_mouse_pos = (x, y)

    def record_mouse_click(self, event):
        if isinstance(event, mouse.ButtonEvent):
            button = event.button

            timestamp = time.time() - self.start_time
            action = {'type': 'mouse_click', 'button': button, 'pressed': self.mouse_click_event,
                      'timestamp': timestamp}
            self.actions.append(action)
            if self.mouse_click_event:
                self.mouse_click_event = False
            else:
                self.mouse_click_event = True

    def record_mouse_wheel(self, event):
        if isinstance(event, mouse.WheelEvent):
            x, y = self.last_mouse_pos
            dx = event.delta
            dy = 0
            timestamp = time.time() - self.start_time
            action = {'type': 'mouse_wheel', 'x': x, 'y': y, 'dx': dx, 'dy': dy, 'timestamp': timestamp}
            self.actions.append(action)

    def record_keyboard_event(self, event):
        if event.event_type == 'down':
            timestamp = time.time() - self.start_time
            action = {'type': 'keyboard', 'event': event.name, 'timestamp': timestamp}
            self.actions.append(action)

    def record_actions(self):
        self.actions = []
        self.start_time = time.time()
        self.last_mouse_pos = None

        mouse.hook(self.record_mouse_move)
        mouse.hook(self.record_mouse_click)
        mouse.hook(self.record_mouse_wheel)
        keyboard.hook(self.record_keyboard_event)

        input("Press Enter to stop recording...")

        mouse.unhook(self.record_mouse_move)
        mouse.unhook(self.record_mouse_click)
        mouse.unhook(self.record_mouse_wheel)
        keyboard.unhook(self.record_keyboard_event)

        return self.actions

    def save_actions_to_json(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.actions, file, indent=4)