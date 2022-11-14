"""
KEY BINDINGS FOR ADAFRUIT RP2040 MACRO PAD
0 = Zoom Mute Toggle
1 = Zoom Camrea Toggle
2 = Sleep Display
3 = LEFT ARROW
4 = DOWN ARROW
5 = RIGHT ARROW
6 = PREVIOUS TRACK
7 = PAUSE/PLAY
8 = NEXT TRACK
9 = COPY
10 = PASTE
11 = UNDO
ENCODER = VOLUME/MUTE
"""
from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode
from rainbowio import colorwheel
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.sequence import AnimationSequence
import os


macropad = MacroPad()


tone = 131
last_position = 0

# Text of Display "                     "
text_lines = macropad.display_text(title="        mute/volume >")
text_lines[0].text = "Zmute   Zcamera sleep"
text_lines[1].text = "left    down    right"
text_lines[2].text = "<<    pause/play   >>"
text_lines[3].text = "copy    paste    undo"
text_lines.show()

# NeoPixels
macropad.pixels.brightness = 0.5
rainbow = Rainbow(macropad.pixels, speed=0.1, period=15, step=2)
rainbow_chase = RainbowChase(macropad.pixels, speed=0.3, size=1, spacing=0, step=24, reverse=False)
rainbow_comet = RainbowComet(macropad.pixels, speed=0.2, tail_length=3, colorwheel_offset=85, bounce=True,)
rainbow_sparkle = RainbowSparkle(macropad.pixels, speed=0.5, num_sparkles=4, period=30, step=1)

#animations = AnimationSequence(
#    RainbowChase(macropad.pixels, speed=0.2, size=4, spacing=1),
#    rainbow,
#    rainbow_chase,
#    rainbow_comet,
#    rainbow_sparkle,
#    advance_interval=10,
#    auto_clear=True,
#)

while True:
    key_event = macropad.keys.events.get()
    #animations.animate()
    #AnimationSequence(RainbowChase(macropad.pixels, speed=0.2, size=4, spacing=1)).animate()
    #rainbow.animate()
    #rainbow_comet.animate()
    #rainbow_chase.animate()
    rainbow_sparkle.animate()
    if key_event:
        if key_event.pressed:
            macropad.pixels[key_event.key_number] = colorwheel(200)
            macropad.start_tone(tone)
        else:
            macropad.pixels.fill((0, 0, 0))
            macropad.stop_tone()

    if key_event:
        if key_event.pressed:
            if key_event.key_number == 0: #Toggle Zoom Mic
                macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.COMMAND, macropad.Keycode.A)
                macropad.pixels.brightness = 0.0
                macropad.keyboard.release_all()
            if key_event.key_number == 1: #Toggle Zoom Camera
                macropad.keyboard.press(macropad.Keycode.SHIFT, macropad.Keycode.COMMAND, macropad.Keycode.V)
                macropad.pixels.brightness = 0.0
                macropad.keyboard.release_all()
            if key_event.key_number == 2: #Sleep Display 
                macropad.pixels.brightness = 0.0
                macropad.keyboard.press(macropad.Keycode.OPTION, macropad.Keycode.COMMAND, macropad.Keycode.POWER)
                macropad.keyboard.release_all()
            if key_event.key_number == 3: #LEFT ARROW
                macropad.keyboard.press(macropad.Keycode.LEFT_ARROW)
                macropad.keyboard.release_all()
            if key_event.key_number == 4: #DOWN ARROW
                macropad.keyboard.press(macropad.Keycode.DOWN_ARROW)
                macropad.keyboard.release_all()
            if key_event.key_number == 5: #RIGHT ARROW
                macropad.keyboard.press(macropad.Keycode.RIGHT_ARROW)
                macropad.keyboard.release_all()
            if key_event.key_number == 6: #PREVIOUS TRACK
                macropad.consumer_control.send(
                macropad.ConsumerControlCode.SCAN_PREVIOUS_TRACK
                )
            if key_event.key_number == 7: #PAUSE PLAY TRACK
                macropad.consumer_control.send(
                macropad.ConsumerControlCode.PLAY_PAUSE
                )
            if key_event.key_number == 8: #NEXT TRACK
                macropad.consumer_control.send(
                macropad.ConsumerControlCode.SCAN_NEXT_TRACK
                )
            if key_event.key_number == 9: #COPY
                macropad.keyboard.press(macropad.Keycode.COMMAND, macropad.Keycode.C)
                macropad.keyboard.release_all()
            if key_event.key_number == 10: #PASTE
                macropad.keyboard.press(macropad.Keycode.COMMAND, macropad.Keycode.V)
                macropad.keyboard.release_all()
            if key_event.key_number == 11: #UNDO
                macropad.keyboard.press(macropad.Keycode.COMM, macropad.Keycode.Z)
                macropad.keyboard.release_all()

    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed: #MUTE
        macropad.consumer_control.send(
        macropad.ConsumerControlCode.MUTE
                )
        macropad.pixels.brightness = 0.5


    current_position = macropad.encoder

    if macropad.encoder > last_position: #VOLUME UP
        macropad.consumer_control.send(
        macropad.ConsumerControlCode.VOLUME_INCREMENT
                )

    if macropad.encoder < last_position: #VOLUME DOWN
        macropad.consumer_control.send(
        macropad.ConsumerControlCode.VOLUME_DECREMENT
                )

    last_position = current_position
