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

from enum import Enum, auto
from time import monotonic
from typing import Optional

import general
import patterns
import playlist
import plugins
import transport
import channels
import midi
import mixer
import device
import ui

try:
    from fl_classes import FlMidiMsg
except ImportError:
    pass

from mapping import Control, LedColor, mapping

last_plugin = None
last_id = None
synced = set()  # For all the colors that were already set
idle_synced_default = set(
    list(range(0, (5*16)-1))
)
idle_synced = idle_synced_default.copy()
last_synced = monotonic()
control_sync = {}

def get_plugin_control(cc) -> Control:
    """Returns the mapped Control for a given cc for the last plugin used."""
    global mapping, last_plugin
    return mapping['plugins'].get(last_plugin, {}).get(
        cc, Control(
            button_led=LedColor.default_button(), encoder_led=LedColor.default_encoder(),
            beautify_button=False, beautify_encoder=False)
    )

def get_assigned_controls() -> set[int]:
    """Returns the list of all the cc's that are assigned for the last plugin used."""
    global mapping, last_plugin
    controls = mapping['plugins'].get(last_plugin, {})
    return set(controls)

def OnInit():
    print("init")

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

last_hint = None
def OnRefresh(flags):
    global last_plugin, last_id, synced, idle_synced, last_hint
    plugin = ui.getFocusedPluginName()
    id_ = ui.getFocusedFormID()
    if last_plugin != plugin and plugin != "":
        print("New plugin:", plugin)
        synced.clear()
        # Batch clear module led intensity
        for cc in range(0, len(idle_synced_default), 16):
            device.midiOutMsg(0xB << 4, 2, cc, 0)
        # Mark every non mapped controls as synced
        synced.union(get_assigned_controls())
        
        idle_synced = idle_synced_default.copy()
    elif id_ != last_id:
        print("New ID:", id_)
        synced.clear()
        # Mark every non mapped controls as synced
        synced.union(get_assigned_controls())
        idle_synced = idle_synced_default.copy()
    last_plugin = plugin
    last_id = id_
    
    # Display last hint if any, if not done here, value is not updated correctly
    if last_hint is not None:
        value_name = device.getLinkedParamName(last_hint[3])
        value_str = device.getLinkedValueString(last_hint[3])
        hint_msg = f"{last_hint[0]}CH{last_hint[1]} CC{last_hint[2]} - {value_name}: {value_str}"
        ui.setHintMsg(hint_msg)
        last_hint = None
    
    # TODO sync back with controller, currently difficult with fl api
    # if flags & midi.HW_Dirty_RemoteLinkValues:
        # print(device.getLinkedChannel())
        # TODO get last eventID, from that, find back the midi cc and channel, sync the LED again
    # def set_parameter_value(self, parameter, value):
    #     rec_event_parameter = parameter + channels.getRecEventId(channels.selectedChannel())
    #     value = int(value * midi.FromMIDI_Max)
    #     mask = midi.REC_MIDIController
    #     general.processRECEvent(rec_event_parameter, value, mask)

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
    """
    Every time this function is called, it sets the color of
    a control that did not have a color update yet after the plugin was changed.
    This method is used because syncing everything at once could result in excessive
    load on the intech modules and make FL studio lag.
    """
    global synced, last_plugin, mapping, control_sync
    if cc in synced:
        return
    synced.add(cc)

    c_map = get_plugin_control(cc)
    button_event = get_mapped_event_id_raw(device.getPortNumber(), 1, cc) 
    if button_event is not None:
        color = c_map.button_led
        intensity = device.getLinkedValue(button_event)
        if c_map.button.invert_intensity:
            intensity = 1 - intensity
        set_led(1, cc, intensity, rgb=color.rgb, beautify=True)
    else:
        set_led(1, cc, 0)

    encoder_event = get_mapped_event_id_raw(device.getPortNumber(), 2, cc)
    if encoder_event is not None:
        color = c_map.encoder_led
        intensity = device.getLinkedValue(encoder_event)
        if c_map.encoder.invert_intensity:
            intensity = 1 - intensity
        set_led(2, cc, intensity, rgb=color.rgb, beautify=True)
    else:
        set_led(2, cc, 0) 

def port_13(msg: 'FlMidiMsg'):
    """Implementation for 5x intech EN16 (0,0;0,1;0,2;1,0;1,1) + 1x TEK2 (1,2)"""
    midiChan = (msg.status & 0xF)
    event_id = get_mapped_event_id(msg)
    if midiChan == 0:
        # Mackie controls
        process_daw_controls(msg, event_id)
    elif event_id is not None:
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
        if 1 <= midiChan <= 2:  # FIXME what's this
            set_led(midiChan, msg.controlNum, 0)
        ui.setHintMsg(f"CH{midiChan} CC{msg.controlNum} - Not assigned")

        # TODO remove this section, it was testing for the special inc/dec bug of Fl studio, got fixed with a -32 offset
        # Special case for 96 & 97
        # msg_p = FlMidiMsg(msg.status, msg.data1, msg.data2)
        # int_msg = construct_int_fl_midi_msg(msg.status, msg.data1, msg.data2, 13)
        # print(int(msg))
        # print(int_msg)
        # device.processMIDICC(int_msg)

        # print(msg)
        # int_msg = construct_int_fl_midi_msg(msg.status, msg.data1, msg.data2, 13)
        # print(msg.isIncrement)
        # print("NOT ASSIGNED")
        # msg.isIncrement = 0
        # device.processMIDICC(msg)
        # device.forwardMIDICC(int_msg, 0)
        # msg.handled = True

        # msg.handled = True
        # print(msg.midiChan, msg.controlNum, msg.controlVal)

def construct_int_fl_midi_msg(status: int, data1: int, data2: int, port: int = 0) -> int:
    return status + (data1 << 8) + (data2 << 16) + (port << 24)

def toggle_window(win_id: int, focus_dependent: bool = True):
    """
    Toggle window visibility and focus.
    If focus_dependent is True then first focus the window.
    Otherwise just toggle visibility.
    """
    if focus_dependent and ui.getFocused(win_id) == True:
        ui.hideWindow(win_id) 
    elif not focus_dependent and ui.getVisible(win_id):
        ui.hideWindow(win_id)
    else:
        ui.showWindow(win_id)
        ui.setFocused(win_id)
    
class FormID(Enum):
    Mixer = 0
    ChannelRack = 1
    Playlist = 2
    PianoRoll = 3
    Browser = 4

    def is_focused(self):
        return ui.getFocusedFormID() == self.value

L_JOG = 0
R_JOG = 1
L_JOG_CC = 56
L_JOG_BTN = 32
R_JOG_CC = 57
R_JOG_BTN = 33
THRES = 1000  # Step scroll threshold (grid endless steps)
LP_THRES = 0.2  # Long press threshold (s)
daw_context = {
    '14bit_midi': {},
    'shift_key': False,
    'last_mixer_plugin': 0,
    'last_focused_mixer_plugin': None,
    'endless_state': {  # Accuracy
        L_JOG: 0,
        R_JOG: 0,
    },
    'jog_mode': {  # Mode to apply
        L_JOG: 0,
        R_JOG: 0,
    },
    'long_press': {}
}
def process_daw_controls(msg: 'FlMidiMsg', event_id):
    global daw_context

    daw_context['14bit_midi'][msg.controlNum] = msg.controlVal
    # L JOG
    if msg.controlNum == L_JOG_CC + 32:
        val = (daw_context['14bit_midi'][L_JOG_CC] << 7) + msg.controlVal
        if val < 8192:
            daw_context['endless_state'][L_JOG] -= (8192 - val)
        else:
            daw_context['endless_state'][L_JOG] += (val - 8192)
        if abs(daw_context['endless_state'][L_JOG]) >= THRES:
            jog_mode = daw_context['jog_mode'][L_JOG]
            jog_val = daw_context['endless_state'][L_JOG]
            if FormID.Playlist.is_focused():  # Playlist
                if jog_mode == 0:
                    if daw_context['shift_key']:
                        ui.next() if jog_val > 0 else ui.previous()
                    else:
                        ui.jog(1 if jog_val > 0 else -1)
                elif jog_mode == 1:
                    ui.verZoom(1 if jog_val > 0 else -1)
            if FormID.Mixer.is_focused():
                ui.jog(1 if jog_val > 0 else -1)
                daw_context['last_mixer_plugin'] = -1
            else:
                ui.jog(1 if jog_val > 0 else -1)
            # elif FormID.ChannelRack.is_focused():  # Channel rack
            #     ui.jog(1 if jog_val > 0 else -1)
                # channels.showEditor(channels.selectedChannel())
            # TODO acceleration here if we just operate thres depending on jog positive or negative value
            daw_context['endless_state'][L_JOG] = 0
    # R JOG
    elif msg.controlNum == R_JOG_CC + 32:
        # toggle_window(FormID.Mixer.value)
        val = (daw_context['14bit_midi'][R_JOG_CC] << 7) + msg.controlVal
        if val < 8192:
            daw_context['endless_state'][R_JOG] -= (8192 - val)
        else:
            daw_context['endless_state'][R_JOG] += (val - 8192)
        if abs(daw_context['endless_state'][R_JOG]) >= THRES:
            jog_mode = daw_context['jog_mode'][R_JOG]
            jog_val = daw_context['endless_state'][R_JOG]
            if FormID.ChannelRack.is_focused():
                next_pattern = patterns.patternNumber() + (1 if jog_val > 0 else -1)
                if next_pattern > 0 and not patterns.isPatternDefault(next_pattern):
                    patterns.jumpToPattern(next_pattern)
            elif FormID.Playlist.is_focused():
                if jog_mode == 0:
                    # TODO find better way to scroll as sometimes the patterns scroll and not the playlist
                    ui.down() if jog_val > 0 else ui.up()
                    # ui.scrollWindow(FormID.Playlist.value, playlist)
                elif jog_mode == 1:
                    ui.horZoom(1 if jog_val > 0 else -1)
            elif FormID.PianoRoll.is_focused():
                pass
            
            # elif FormID.Mixer.is_focused():

            # # ===========================
            # elif FormID.Mixer.is_focused():
            #     # mixer.getTrackPluginId(mixer.trackNumber())

            #     # Hide previously shown plugin
            #     if daw_context['last_focused_mixer_plugin'] is not None:
            #         # print("Hide", daw_context['last_focused_mixer_plugin'])
            #         # ui.showWindow(daw_context['last_focused_mixer_plugin'])
            #         # ui.setFocused(daw_context['last_focused_mixer_plugin'])
            #         # print("UI.", ui.getFocusedFormCaption())
            #         # ui.hideWindow(daw_context['last_focused_mixer_plugin'])
            #         mixer.focusEditor(
            #             mixer.trackNumber(),
            #             daw_context['last_mixer_plugin']
            #         )
            #         transport.globalTransport(midi.FPT_Escape, 1, 2)
            #         toggle_window(FormID.Mixer.value)

            #     for _ in range(10):
            #         try:
            #             daw_context['last_mixer_plugin'] = (daw_context['last_mixer_plugin'] + (1 if jog_val > 0 else -1)) % 10
            #             mixer.focusEditor(
            #                 mixer.trackNumber(),
            #                 daw_context['last_mixer_plugin'],
            #             )
            #             # TODO Display red rectangle around selected plugin
            #         except:
            #             pass
            #         else:

            #             # print(1, ui.getFocusedPluginName())
            #             # current_new_plugin = ui.getFocusedFormID()
            #             # toggle_window(daw_context['last_focused_mixer_plugin'])
            #             # print(2, ui.getFocusedPluginName())
            #             # toggle_window(current_new_plugin)
            #             # print(3, ui.getFocusedPluginName())
            #             # daw_context['last_focused_mixer_plugin'] = ui.getFocusedFormID()

            #             # if daw_context['last_focused_mixer_plugin'] is not None:
            #             #     print("Toggle:", daw_context['last_focused_mixer_plugin'])
            #             #     toggle_window(daw_context['last_focused_mixer_plugin'])
            #             # daw_context['last_focused_mixer_plugin'] = new_focused_form_id
            #             # print(ui.getFocusedFormID(), '-', ui.getFocusedPluginName())

            #             # Save last focused plugin
            #             daw_context['last_focused_mixer_plugin'] = ui.getFocusedFormID()

            #             # Re focus the mixer
            #             toggle_window(FormID.Mixer.value)
            #             break
            #     # TODO re-focus the mixer and de-focus the last plugin
            # # =====================

            else:  # On any other plugin
                # mixer.getTrackPluginId()
                # if daw_context['last_focused_mixer_plugin'] is not None:
                #     ui.setFocused(daw_context['last_focused_mixer_plugin'])
                #     transport.globalTransport(midi.FPT_Escape, 1)
                transport.globalTransport(midi.FPT_MixerWindowJog, 1 if jog_val > 0 else -1, 2)
                currently_selected = ui.getFocusedFormID()
                print(currently_selected)
            # TODO acceleration here if we just operate thres depending on jog positive or negative value
            daw_context['endless_state'][R_JOG] = 0

    PLAY_PAUSE_BTN = 0
    STOP_BTN = 1
    PAT_SNG_BTN = 2
    REC_BTN = 2
    SHIFT_BTN = 3
    MIXER_BTN = 4
    BROWSER_BTN = 4
    PLAYLIST_BTN = 5
    CHANRACK_BTN = 6
    PIANOROLL_BTN = 7

    def is_long_press(msg: 'FlMidiMsg', delay: float=LP_THRES):
        """Checks that a button was pressed for a minimum duration of `delay` (seconds)."""
        initial_press, value = daw_context['long_press'][msg.controlNum]
        if value != msg.controlVal and initial_press + delay < monotonic():
            return True
        return False
    
    def shift():
        return daw_context.get('shift_key', False)

    # Handle button presses
    if msg.controlVal == 127:  # Button pressed
        if msg.controlNum == PLAY_PAUSE_BTN:
            if shift():
                transport.stop()
            transport.start()
        elif msg.controlNum == STOP_BTN:
            transport.stop()
        elif msg.controlNum == SHIFT_BTN:
            daw_context['shift_key'] = True

    elif msg.controlVal == 0:  # Button released
        if msg.controlNum == MIXER_BTN:
            if shift():
                toggle_window(FormID.Browser.value, focus_dependent=False)
            else:
                if is_long_press(msg):
                    transport.globalTransport(midi.FPT_F12, midi.PME_System)
                else:
                    toggle_window(FormID.Mixer.value)
        elif msg.controlNum == CHANRACK_BTN:
            toggle_window(FormID.ChannelRack.value)
        elif msg.controlNum == PLAYLIST_BTN:
            toggle_window(FormID.Playlist.value)
        elif msg.controlNum == PIANOROLL_BTN:
            toggle_window(FormID.PianoRoll.value)
        elif msg.controlNum == PAT_SNG_BTN:
            if is_long_press(msg):
                transport.record()
            else:
                transport.setLoopMode()
        elif msg.controlNum == SHIFT_BTN:
            daw_context['shift_key'] = False
        # Jog btns
        elif msg.controlNum == L_JOG_BTN:
            if FormID.Playlist.is_focused():
                daw_context['jog_mode'][L_JOG] = (daw_context['jog_mode'][L_JOG] + 1) % 2
            elif FormID.ChannelRack.is_focused():
                channels.focusEditor(channels.selectedChannel())
                channels.showEditor(channels.selectedChannel(), 1)
            else:  # Close any other window
                channels.showEditor(channels.selectedChannel(), 0)
        elif msg.controlNum == R_JOG_BTN:
            if FormID.Playlist.is_focused():
                daw_context['jog_mode'][R_JOG] = (daw_context['jog_mode'][R_JOG] + 1) % 2
            if FormID.ChannelRack.is_focused():
                target_fx_track = channels.getTargetFxTrack(channels.selectedChannel())
                if target_fx_track != 0:
                    ui.setFocused(FormID.Mixer.value)
                    ui.showWindow(FormID.Mixer.value)
                    mixer.setTrackNumber(target_fx_track)
    msg.handled = True
    daw_context['long_press'][msg.controlNum] = (monotonic(), msg.controlVal)

def process_linked_params_buttons(msg: 'FlMidiMsg', event_id):
    global last_hint
    c_map = get_plugin_control(msg.controlNum)

    val = device.getLinkedValue(event_id)
    if msg.controlVal == 127:
        new_value = get_relative_step(val, c_map.button.steps, 1, rollover=True)
        general.processRECEvent(event_id, int(new_value * midi.FromMIDI_Max), midi.REC_MIDIController)
    msg.handled = True
    intensity = val
    if c_map.button.invert_intensity:
        intensity = 1 - intensity
    set_led(msg.status & 0xF, msg.controlNum, intensity, beautify=c_map.beautify_button)
    last_hint = ("", msg.status, msg.controlNum, event_id)

def get_relative_step(value: float, steps: int, speed: int, min_: float = 0.0, max_: float = 1.0, rollover=False) -> float:
    """Get the value at step diff for an encoder or button. Rollover disables clamp between min and max mode."""
    R_STEP_PRECISION = 5
    step_diff = (max_ - min_) / (steps - 1)
    # Get current step
    current_step = 0
    LOOP_MAX = 4095
    loop_n = 0
    value = round(value, R_STEP_PRECISION)
    while value > round(step_diff * current_step, R_STEP_PRECISION):
        if loop_n == LOOP_MAX:  # Avoid infinite loops
            raise Exception("Infinite loop in stepper")
        current_step += 1
        loop_n += 1 
    
    if rollover and current_step + speed >= steps:
        speed = -1 * (current_step + speed - 1)
    elif current_step + speed >= steps:
        speed = steps - current_step - 1
    elif current_step + speed < 0:
        speed = 0 - current_step
    clamped_value = round((current_step + speed) * step_diff, R_STEP_PRECISION)
    return clamped_value

anti_ghost = monotonic()
anti_ghost_cc = None
anti_ghost_direction = 0  # -1 = counter clockwise, 1 = clockwise
ANTI_GHOST_DELAY = 0.13
def process_linked_params_encoders(msg: 'FlMidiMsg', event_id):
    global anti_ghost, anti_ghost_direction, anti_ghost_cc, last_hint
    c_map = get_plugin_control(msg.controlNum)
    msg_val = msg.controlVal
    if msg_val < 64:
        inc = -1
        speed = -(64 - msg_val)
    else:
        inc = 1
        speed = msg_val - 64
    
    if inc == 0:
        msg.handled = True
        return
    
    # Filter unwanted kickbacks / ghost movements
    if anti_ghost_direction != inc and monotonic() < anti_ghost + ANTI_GHOST_DELAY and msg.controlNum == anti_ghost_cc:
        msg.handled = True
        return
    anti_ghost = monotonic()
    anti_ghost_direction = inc
    anti_ghost_cc = msg.controlNum

    if c_map.encoder.accel:
        diff = speed
    else:
        diff = inc
    
    if c_map.encoder.invert:
        diff = -diff
    try:
        if c_map.encoder.steps >= 255:
            mixer.automateEvent(
                event_id,
                diff,
                midi.REC_MIDIController,
                0,
                1,
                res=1 / (c_map.encoder.steps - 1),
            )
            msg.handled = True
        else:  # Stepped mode
            val = device.getLinkedValue(event_id)
            new_value = get_relative_step(val, c_map.encoder.steps, diff)
            general.processRECEvent(event_id, int(new_value * midi.FromMIDI_Max), midi.REC_MIDIController)
            msg.handled = True
    except RuntimeError:
        msg.handled = False
        hint_msg = f"CH{msg.status & 0xF} CC{msg.controlNum} - Operation Unsafe"
        ui.setHintMsg(hint_msg)
        return
    
    val = device.getLinkedValue(event_id)
    intensity = val
    if c_map.encoder.invert_intensity:
        intensity = 1 - intensity
    set_led(msg.status & 0xF, msg.controlNum, intensity, beautify=c_map.beautify_encoder)

    hint_status = "^w" if inc > 0 else "^v"
    last_hint = (hint_status, msg.status, msg.controlNum, event_id)

def set_led(
        channel: int,
        cc: int,
        intensity: float,
        rgb: Optional[tuple[float, float, float]] = None,
        beautify: bool = False
    ):
    BEAUTIFY_CEIL = 114
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

