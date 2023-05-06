#! /usr/bin/python3
import uinput
from inputs import get_gamepad

from keys import KEYS
from config import get_config, get_modifiers

MODE_PREFIX = "mode_"

mode = "mode_D_NORTH"
mode_listening = 0


def press_a(device):
    key = uinput.KEY_1
    device.emit(key, 1)
    device.emit(key, 0)


def get_key_by_value(d, value):
    for k, v in d.items():
        if v == value:
            return k
    return None


def handle_modifier(modifier, state, device):
    global mode_listening

    if modifier == "ctrl":
        key = uinput.KEY_LEFTCTRL
    elif modifier == "shift":
        key = uinput.KEY_LEFTSHIFT
    elif modifier == "shift":
        key = uinput.KEY_LEFTALT
    elif modifier == "mode":
        mode_listening = state
        if mode_listening == 0:
            for key in KEYS:
                device.emit(key, 0)
        return
    else:
        return

    device.emit(key, state)


def handle_button(code, state, device, config):
    global mode

    if mode == "":
        return

    if mode not in config:
        print(f"mode {mode} is not defined")
        return

    config_mode = config[mode]

    if code not in config_mode:
        print(f"{code} is not defined in {mode}")
        return

    try:
        key = getattr(uinput, config_mode[code])
        device.emit(key, state)
    except Exception as e:
        print(code)
        print(e)


def update_mode(event):
    global mode
    if event.state == 0:
        return
    if "BTN" in event.code:
        mode = MODE_PREFIX + event.code
    elif "ABS_HAT" in event.code:
        if event.code == "ABS_HAT0Y":
            if event.state == -1:
                mode = MODE_PREFIX + "D_NORTH"
            elif event.state == 1:
                mode = MODE_PREFIX + "D_SOUTH"
        if event.code == "ABS_HAT0X":
            if event.state == -1:
                mode = MODE_PREFIX + "D_WEST"
            elif event.state == 1:
                mode = MODE_PREFIX + "D_EAST"
    print(f"mode changed to {mode}")


def handle_key(event, device, config):
    # print(event.ev_type, event.code, event.state)
    if "BTN" in event.code:
        handle_button(event.code, event.state, device, config)
    elif "ABS_HAT" in event.code:
        if event.code == "ABS_HAT0Y":
            if event.state == -1:
                handle_button("D_NORTH", 1, device, config)
            elif event.state == 1:
                handle_button("D_SOUTH", 1, device, config)
            else:
                handle_button("D_NORTH", 0, device, config)
                handle_button("D_SOUTH", 0, device, config)
        if event.code == "ABS_HAT0X":
            if event.state == -1:
                handle_button("D_WEST", 1, device, config)
            elif event.state == 1:
                handle_button("D_EAST", 1, device, config)
            else:
                handle_button("D_WEST", 0, device, config)
                handle_button("D_EAST", 0, device, config)


def key_press(device, key):
    device.emit(key, 1)
    device.emit(key, 0)


def handle_mode(event, modifiers, device):
    modifier = get_key_by_value(modifiers, event.code)
    if modifier is None and "THUMB" not in event.code:
        update_mode(event)
    elif event.code == "BTN_TR2":
        device.emit(uinput.KEY_SPACE, event.state)
        # key_press(device, uinput.KEY_SPACE)
    elif event.code == "BTN_TR":
        device.emit(uinput.KEY_BACKSPACE, event.state)
        # key_press(device, uinput.KEY_BACKSPACE)
    elif event.code == "BTN_TL2":
        device.emit(uinput.KEY_ENTER, event.state)
        # key_press(device, uinput.KEY_ENTER)
    elif event.code == "BTN_THUMBR":
        device.emit(uinput.KEY_TAB, event.state)
        # key_press(device, uinput.KEY_TAB)
    else:
        print(event.ev_type, event.code, event.state)


def main():
    global mode
    global mode_listening

    device = uinput.Device(KEYS)

    config = get_config()
    modifiers = get_modifiers(config)
    print(modifiers)

    while 1:
        events = get_gamepad()
        for event in events:
            if not event.ev_type == "Sync":
                modifier = get_key_by_value(modifiers, event.code)
                if (modifier is not None) or ("THUMB" in event.code):
                    if mode_listening and modifier != "mode":
                        handle_mode(event, modifiers, device)
                    else:
                        handle_modifier(modifier, event.state, device)
                elif "BTN" in event.code or "HAT" in event.code:
                    if mode_listening:
                        handle_mode(event, modifiers, device)
                    else:
                        handle_key(event, device, config)


if __name__ == "__main__":
    main()
