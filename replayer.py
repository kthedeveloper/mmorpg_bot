import mouse
import keyboard
import time


class ActionReplayer:
    def __init__(self, actions):
        self.actions = actions
        self.start_time = None
        self.last_mouse_pos = None

    def replay_mouse_move(self, action):
        x = action['x']
        y = action['y']
        dx = action['dx']
        dy = action['dy']
        delay = action['timestamp'] - (time.time() - self.start_time)

        if delay > 0:
            time.sleep(delay)

        if self.last_mouse_pos is not None:
            mouse.move(self.last_mouse_pos[0] + dx, self.last_mouse_pos[1] + dy)
        else:
            mouse.move(x, y)

        self.last_mouse_pos = (x, y)

    def replay_mouse_click(self, action):
        button = action['button']
        pressed = action['pressed']
        delay = action['timestamp'] - (time.time() - self.start_time)

        if delay > 0:
            time.sleep(delay)

        if pressed:
            mouse.press(button=button)
        else:
            mouse.release(button=button)

    def replay_keyboard_event(self, action):
        event = action['event']
        delay = action['timestamp'] - (time.time() - self.start_time)

        if delay > 0:
            time.sleep(delay)

        keyboard.press_and_release(event)

    def replay_mouse_wheel(self, action):
        dx = action['dx']
        dy = action['dy']
        delay = action['timestamp'] - (time.time() - self.start_time)

        if delay > 0:
            time.sleep(delay)

        mouse.wheel(delta=dx)

    def replay_actions(self):
        self.start_time = time.time()
        self.last_mouse_pos = None

        for i, action in enumerate(self.actions):
            if action['type'] == 'mouse_move':
                self.replay_mouse_move(action)
            elif action['type'] == 'mouse_click':
                self.replay_mouse_click(action)
            elif action['type'] == 'keyboard':
                self.replay_keyboard_event(action)
            elif action['type'] == 'mouse_wheel':
                self.replay_mouse_wheel(action)
            """if action['event'] == 'alt':
                keyboard.press_and_release(f'alt+{self.actions[i+1]["event"]}')"""

        print("Replay complete.")
