import time
import vgamepad as vg
import keyboard
import threading
import random
gamepad = vg.VX360Gamepad()
w = False
s = False
d = False
a = False
running = False
enabled = False
reallyenabled = True
hookw = None
hooks = None
hookerw = None
hookers = None
hookd = None
hookerd = None
hooka = None
hookera = None
loop_running = False
loop_thread = None
prevx,prevy = None,None
def loop(x, y):
    global loop_running
    while loop_running:
        time.sleep(1 / 240)
        currentx = (x != 0 and x - random.uniform(0, 0.03) * (x / abs(x))) or x
        currenty = (y != 0 and y - random.uniform(0, 0.03) * (y / abs(y))) or y
        gamepad.left_joystick_float(currentx, currenty)
        gamepad.update()
    print('stopped')

def updatemovement(x, y):
    global loop_running, loop_thread,prevx,prevy
    if prevy == y and prevx == x:
        return
    prevx = x
    prevy = y
    if not loop_running:
        print("Starting loop")
        loop_running = True
        loop_thread = threading.Thread(target=loop, args=(x, y), daemon=True)
        loop_thread.start()

    elif x == 0.0 and y == 0.0:
        print("Stopping loop")
        loop_running = False
        time.sleep(0.01)
        gamepad.left_joystick_float(0.0, 0.0)
        gamepad.update()
    else:
        print("Restarting loop with new values")
        loop_running = False
        time.sleep(0.01)
        loop_running = True
        loop_thread = threading.Thread(target=loop, args=(x, y), daemon=True)
        loop_thread.start()

def switch(e):
    global reallyenabled
    if not reallyenabled:
        return
    global hookw, hooks, hookerw, hookers, hooka, hookera, hookd, hookerd, enabled
    enabled = not enabled
    if enabled:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        hookw = keyboard.on_press_key("w", on_w_press, suppress=True)
        hooks = keyboard.on_release_key("w", on_w_release, suppress=True)
        hookerw = keyboard.on_press_key("s", on_s_press, suppress=True)
        hookers = keyboard.on_release_key("s", on_s_release, suppress=True)
        hooka = keyboard.on_press_key("a", on_a_press, suppress=True)
        hookera = keyboard.on_release_key("a", on_a_release, suppress=True)
        hookd = keyboard.on_press_key("d", on_d_press, suppress=True)
        hookerd = keyboard.on_release_key("d", on_d_release, suppress=True)
    else:
        keyboard.unhook_all()
        keyboard.on_press_key("r", switch,suppress=False)
        keyboard.on_press_key("f2", on_f2)
        keyboard.on_press_key('/',lambda _: realswitch(False))
        keyboard.on_press_key('enter',lambda _: realswitch(True))
    print(f"Enabled?{enabled}")

def spam_x():
    global running
    while running:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        print("Pressed X")
        time.sleep(0.2)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
        gamepad.update()
        print("Released X")
        time.sleep(0.2)

def on_f2(e):
    global running
    running = not running
    if running:
        threading.Thread(target=spam_x, daemon=True).start()

def on_w_press(e):
    global w
    w = True

def on_w_release(e):
    global w
    w = False

def on_s_press(e):
    global s
    s = True

def on_s_release(e):
    global s
    s = False

def on_d_press(e):
    global d
    d = True

def on_d_release(e):
    global d
    d = False

def on_a_press(e):
    global a
    a = True

def on_a_release(e):
    global a
    a = False

def joystick_update_loop():
    while True:
        if enabled:
            x = 0.0
            y = 0.0
            if w:
                y += 1.0
            if s:
                y -= 1.0
            if d:
                x += 1.0
            if a:
                x -= 1.0
            updatemovement(x,y)
        else:
            updatemovement(0,0)
        gamepad.update()
        time.sleep(0.01)
def realswitch(state):
    print(state)
    global reallyenabled, enabled
    if enabled:
        switch(None)
    reallyenabled = state
    

keyboard.on_press_key("r", switch,suppress=False)
keyboard.on_press_key("f2", on_f2)
keyboard.on_press_key('/',lambda _: realswitch(False))
keyboard.on_press_key('enter',lambda _: realswitch(True))

threading.Thread(target=joystick_update_loop, daemon=True).start()


keyboard.wait()
