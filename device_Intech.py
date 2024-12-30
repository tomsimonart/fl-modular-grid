#name=Intech
#url=https://github.com/tomsimonart/fl-modular-grid

"""
FL Modular Grid - Control Intech or any other midi devices
Copyright (C) 2024-2025  Tom Simonart

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from time import monotonic
from typing import Optional

import midi
import mixer
import device
import ui

try:
    from fl_classes import FlMidiMsg
except ImportError:
    pass

from mapping import Control, LedColor, mapping


def get_plugin_control(cc) -> Control:
    global mapping, last_plugin
    return mapping['plugins'].get(last_plugin, {}).get(
        cc, Control(
            button_led=LedColor.default_button(), encoder_led=LedColor.default_encoder(),
            beautify_button=False, beautify_encoder=False)
    )

def OnInit():
    print("init")

last_plugin = None
synced = set()  # For all the colors that were already set
idle_synced_default = set(list(range(32, 32+16)) + list(range(48, 48+16)) + list(range(80, 80+16)))
idle_synced = idle_synced_default.copy()
last_synced = monotonic()
control_sync = {}

def OnIdle():
    SYNC_DELTA = 0
    global last_plugin, idle_synced, mapping, last_synced
    if len(idle_synced) == 0:
        return
    if monotonic() < last_synced + SYNC_DELTA:
        return
    cc = idle_synced.pop()
    set_control_color(cc, reset_intensity=True)
    last_synced = monotonic()

def OnRefresh(flags):
    global last_plugin, synced, idle_synced
    plugin = ui.getFocusedPluginName()
    if last_plugin != plugin and plugin != "":
        print("New plugin:", plugin)
        synced.clear()
        idle_synced = idle_synced_default.copy()
        last_plugin = plugin
    
    # TODO sync back with controller, currently difficult with fl api
    # if flags & midi.HW_Dirty_RemoteLinkValues:
        # print(device.getLinkedChannel())
        # TODO get last eventID, from that, find back the midi cc and channel, sync the LED again

def get_mapped_event_id(msg: 'FlMidiMsg') -> Optional[int]:
    return get_mapped_event_id_raw(device.getPortNumber(), msg.status & 0xF, msg.controlNum)

def get_mapped_event_id_raw(port, channel, cc):
    fl_control_id = midi.EncodeRemoteControlID(port, channel, cc)
    event_id = device.findEventID(fl_control_id)
    linked_info = device.getLinkedInfo(event_id)
    if linked_info == -1:
        return None
    return event_id

def OnMidiIn(msg: 'FlMidiMsg'):
    port = device.getPortNumber()
    if port == 13:
        port_13(msg)
    else:
        return

def set_control_color(cc: int, reset_intensity: bool = False):
    global synced, last_plugin, mapping, control_sync
    if cc in synced:
        return
    synced.add(cc)

    c_map = get_plugin_control(cc)
    button_event = get_mapped_event_id_raw(device.getPortNumber(), 1, cc) 
    if button_event is not None:
        color = c_map.button_led
        set_led(1, cc, device.getLinkedValue(button_event), rgb=color.rgb, beautify=True)
    else:
        set_led(1, cc, 0)

    encoder_event = get_mapped_event_id_raw(device.getPortNumber(), 2, cc)
    if encoder_event is not None:
        color = c_map.encoder_led
        set_led(2, cc, device.getLinkedValue(encoder_event), rgb=color.rgb, beautify=True)
    else:
        set_led(2, cc, 0) 

def port_13(msg: 'FlMidiMsg'):
    """Implementation for 3x intech EN16 (0,0;0,1;1,0) + 1x TEK2 (1,1)"""
    midiChan = (msg.status & 0xF)
    event_id = get_mapped_event_id(msg)
    if event_id is not None:        
        if msg.status >> 4 == 0xB:  # CC
            set_control_color(msg.controlNum)
            if midiChan == 2:
                process_linked_params_encoders(msg, event_id)
            elif midiChan == 1:
                process_linked_params_buttons(msg, event_id)
        else:
            print(f"Unsupported midi msg type: {msg.status >> 4}")
    else:
        # Set led to off
        set_led(midiChan, msg.controlNum, 0)
        ui.setHintMsg(f"CH{midiChan} CC{msg.controlNum} - Not assigned")

def get_next_step(value, steps=3, min_=0, max_=1):
    """Get the next step for a stepped button."""
    step_diff = (max_ - min_) / steps
    step_offset = step_diff / 2
    for i in range(steps):
        ceiling = (i + 1) * step_diff
        if value <= ceiling:
            next_value = ((step_diff * (i + 1)) + step_offset) % 1.0
            print("next =", next_value)
            return next_value


def process_linked_params_buttons(msg: 'FlMidiMsg', event_id):
    c_map = get_plugin_control(msg.controlNum)
    name = device.getLinkedParamName(event_id)
    val = device.getLinkedValue(event_id)

    if msg.controlVal == 127:
        msg.controlVal = int(get_next_step(val, c_map.button.steps) * 127)
    else:
        msg.handled = True
        val = device.getLinkedValue(event_id)
        val_str = device.getLinkedValueString(event_id)
        set_led(msg.status & 0xF, msg.controlNum, val, beautify=c_map.beautify_button)
        ui.setHintMsg(f"CH{msg.status & 0xF} CC{msg.controlNum} - {name}: {val_str}")

def process_linked_params_encoders(msg: 'FlMidiMsg', event_id):
        val_name = device.getLinkedParamName(event_id)
        val_str = device.getLinkedValueString(event_id)

        msg_val = msg.controlVal
        if msg_val < 64:
            inc = -1
            speed = -(64 - msg_val)
        else:
            inc = 1
            speed = msg_val - 64
        
        msg.handled = True
        if inc == 0:
            return
        
        c_map = get_plugin_control(msg.controlNum)
        try:
            mixer.automateEvent(
                event_id,
                speed,
                midi.REC_MIDIController,
                0,
                1,
                res=1/c_map.encoder.steps,
            )
        except RuntimeError:
            msg.handled = False
            hint_msg = f"CH{msg.status & 0xF} CC{msg.controlNum} - Operation Unsafe"
            ui.setHintMsg(hint_msg)
            return
        val = device.getLinkedValue(event_id)
        set_led(msg.status & 0xF, msg.controlNum, val, beautify=c_map.beautify_encoder)

        hint_msg = "^w" if inc > 0 else "^v"
        hint_msg += f"CH{msg.status & 0xF} CC{msg.controlNum} - {val_name}: {val_str}"
        ui.setHintMsg(hint_msg)

def set_led(
        channel: int,
        cc: int,
        intensity: float,
        rgb: Optional[tuple[float, float, float]] = None,
        beautify: bool = False
    ):
    BEAUTIFY_CEIL = 115
    if beautify:
        intensity = int(intensity * BEAUTIFY_CEIL) + 127 - BEAUTIFY_CEIL
    else:
        intensity = int(intensity * 127)
    if rgb is not None:
        color = int(rgb[0] * 31) << 9 | int(rgb[1] * 31) << 4 | int(rgb[2] * 15)
    else:
        color = None
    send_cmd(channel, cc, intensity, color)


def send_cmd(layer: int, cc: int, intensity: int, color: Optional[int]):
    """Send a low-level protocol message."""
    # Intensity
    device.midiOutMsg(0xB << 4, 6 if layer == 1 else 8, cc, intensity)
    # Color
    if color is not None:
        device.midiOutMsg(0xB << 4, 7 if layer == 1 else 9, color >> 7, color & 0x7F)

