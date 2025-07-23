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
from dataclasses import dataclass, field
from enum import Enum, auto


@dataclass
class LedColor:
    r: float = 0
    g: float = 0
    b: float = 0

    @property
    def rgb(self):
        return self.r, self.g, self.b

    def __str__(self):
        return f"({self.r}, {self.g}, {self.b})"
    
    @classmethod
    def off(cls):
        return cls(0, 0, 0)
    
    @classmethod
    def default_button(cls):
        return cls(1, 0, 0)
    
    @classmethod
    def default_encoder(cls):
        return cls(0, 0, 1)
    
    @classmethod
    def white(cls):
        return cls(1, 1, 1)
    
    @classmethod
    def grey(cls):
        return cls(0.5, 0.5, 0.5)

    @classmethod
    def red(cls):
        return cls(1, 0, 0)

    @classmethod
    def green(cls):
        return cls(0, 1, 0)
    
    @classmethod
    def blue(cls):
        return cls(0, 0, 1)
    
    @classmethod
    def yellow(cls):
        return cls(1, 1, 0)
    
    @classmethod
    def cyan(cls):
        return cls(0, 1, 1)
    
    @classmethod
    def magenta(cls):
        return cls(1, 0, 1)
    
    @classmethod
    def orange(cls):
        return cls(1, 0.5, 0)
    
    @classmethod
    def purple(cls):
        return cls(0.5, 0, 1)
    
    @classmethod
    def pink(cls):
        return cls(1, 0, 0.5)
    
    @classmethod
    def teal(cls):
        return cls(0, 1, 0.5)
    
    @classmethod
    def lime(cls):
        return cls(0.5, 1, 0)
    
    @classmethod
    def azure(cls):
        return cls(0, 0.5, 1)
    
    @classmethod
    def brown(cls):
        return cls(0.5, 0.25, 0)
    
    @classmethod
    def lightgreen(cls):
        return cls(0.5, 1, 0.5)


@dataclass
class CtrlEncoder():
    steps: int = 255
    accel: bool = True
    invert: bool = False
    invert_intensity: bool = False

@dataclass
class CtrlButton():
    steps: int = 2
    invert_intensity: bool = False

@dataclass
class Control:
    button_led: LedColor = field(default_factory=LedColor.off)
    encoder_led: LedColor = field(default_factory=LedColor.off)
    beautify_button: bool = True
    beautify_encoder: bool = True
    encoder: CtrlEncoder = field(default_factory=CtrlEncoder)
    button: CtrlButton = field(default_factory=CtrlButton)

mapping = {
    "plugins": {

        "Tube-Tech SMC 2B": {
            # First part (cross controls)
            0: Control(button_led=LedColor.white()),
            4: Control(encoder_led=LedColor.blue()),
            8: Control(encoder_led=LedColor.blue()),
            # Row 1
            1: Control(encoder_led=LedColor.blue()),
            2: Control(encoder_led=LedColor.blue()),
            3: Control(encoder_led=LedColor.blue()),
            16: Control(encoder_led=LedColor.blue()),
            17: Control(encoder_led=LedColor.blue()),
            # Row 2
            5: Control(encoder_led=LedColor.blue()),
            6: Control(encoder_led=LedColor.blue()),
            7: Control(encoder_led=LedColor.blue()),
            20: Control(encoder_led=LedColor.blue()),
            21: Control(encoder_led=LedColor.blue()),
            # Row 3
            9: Control(encoder_led=LedColor.blue()),
            10: Control(encoder_led=LedColor.blue()),
            11: Control(encoder_led=LedColor.blue()),
            24: Control(encoder_led=LedColor.blue()),
            25: Control(encoder_led=LedColor.blue()),
            # Side chain / Control channel
            12: Control(button_led=LedColor.white()),
            13: Control(button_led=LedColor.red()),
            14: Control(button_led=LedColor.red()),
            15: Control(button_led=LedColor.red()),
            # Mute
            28: Control(button_led=LedColor.white()),
            29: Control(button_led=LedColor.white()),
            30: Control(button_led=LedColor.white()),
            # Balance, Output, in/ext, dry/wet
            19: Control(encoder_led=LedColor.blue()),
            23: Control(encoder_led=LedColor.blue()),
            27: Control(button_led=LedColor.red(), button=CtrlButton(invert_intensity=True)),
            31: Control(encoder_led=LedColor.blue()),
        },

        "Tube-Tech CL 1B mk II": {
            # Controls
            8: Control(encoder_led=LedColor.blue()),
            9: Control(encoder_led=LedColor.blue()),
            10: Control(encoder_led=LedColor.blue()),
            11: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3)),
            12: Control(encoder_led=LedColor.blue()),
            13: Control(encoder_led=LedColor.blue()),
            14: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3)),
            15: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=2)),
            # On off
            28: Control(button_led=LedColor.red()),
            # Sidechain 
            48: Control(button_led=LedColor.white(), button=CtrlButton(steps=2)),
            49: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            51: Control(encoder_led=LedColor.blue()),
        },

        "Tube-Tech Equalizers mk II": {
            # Lows
            0: Control(encoder_led=LedColor.blue()),
            1: Control(encoder_led=LedColor.blue()),
            4: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=4, accel=False)),
            # Mid
            5: Control(encoder_led=LedColor.cyan()),
            6: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=10, accel=False)),
            2: Control(encoder_led=LedColor.cyan()),
            # Atten
            3: Control(encoder_led=LedColor.blue()),
            16: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)), 
            # Output Gain
            20: Control(encoder_led=LedColor.blue(), button_led=LedColor.red(), beautify_button=False),
            # MEQ Peak L
            8: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)), 
            9: Control(encoder_led=LedColor.blue()), 
            # MEQ DIP
            10: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=11, accel=False)), 
            11: Control(encoder_led=LedColor.cyan()), 
            # MEQ Peak H
            24: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)), 
            25: Control(encoder_led=LedColor.blue()), 
            # MEQ Output Gain
            26: Control(encoder_led=LedColor.blue(), button_led=LedColor.red(), beautify_button=False),
        },

        "UADx SSL E Channel Strip": {
            # Line & Mic
            0: Control(button_led=LedColor.white(), encoder_led=LedColor.white(), beautify_button=False),
            1: Control(button_led=LedColor.white()),
            4: Control(button_led=LedColor.grey(), encoder_led=LedColor.red(), beautify_button=False),
            5: Control(button_led=LedColor.red()),
            # Dynamics (comp)
            8: Control(encoder_led=LedColor.white()),
            9: Control(encoder_led=LedColor.white(), button_led=LedColor.yellow(), beautify_button=False),
            12: Control(encoder_led=LedColor.white(), button_led=LedColor.red(), beautify_button=False),
            # Dynamics (exp/gate)
            13: Control(encoder_led=LedColor.green()),
            48: Control(encoder_led=LedColor.green()),
            49: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            52: Control(encoder_led=LedColor.green(), button_led=LedColor.red(), beautify_button=False),
            # Dynamics buttons
            53: Control(button_led=LedColor.green()),
            56: Control(button_led=LedColor.red()),
            57: Control(button_led=LedColor.yellow()),
            # Filters
            60: Control(encoder_led=LedColor.grey(), button_led=LedColor.red(), beautify_button=False, beautify_encoder=False),
            61: Control(encoder_led=LedColor.grey(), button_led=LedColor.yellow(), beautify_button=False, beautify_encoder=False),
            # EQ
            2: Control(encoder_led=LedColor.red()),
            3: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False),
            6: Control(encoder_led=LedColor.green()),
            7: Control(encoder_led=LedColor.green()),
            10: Control(encoder_led=LedColor.green()),
            11: Control(button_led=LedColor.yellow()),
            14: Control(encoder_led=LedColor.blue()),
            15: Control(encoder_led=LedColor.blue()),
            50: Control(encoder_led=LedColor.blue()),
            51: Control(encoder_led=LedColor.brown(), button_led=LedColor.grey(), beautify_button=False),
            54: Control(encoder_led=LedColor.brown()),
            # EQ buttons
            55: Control(button_led=LedColor.green()),
            58: Control(button_led=LedColor.red()),
            59: Control(button_led=LedColor.yellow()),
            # Power
            62: Control(button_led=LedColor(1, 1, 0.5)),
            # Fader & Output
            20: Control(button_led=LedColor.green()),
            24: Control(encoder_led=LedColor.white()),
            28: Control(encoder_led=LedColor.white()),
        },

        "UADx API Vision Channel Strip": {
            # 212L
            0: Control(encoder_led=LedColor.red(), button_led=LedColor.red(), beautify_button=False),
            4: Control(encoder_led=LedColor.green(), button_led=LedColor.green(), beautify_button=False),
            8: Control(button_led=LedColor.red()),
            12: Control(button_led=LedColor.green()),
            # 215L
            48: Control(encoder_led=LedColor.orange()),
            52: Control(button_led=LedColor.green()),
            56: Control(encoder_led=LedColor.orange()),
            60: Control(button_led=LedColor.green()),
            # 235L
            1: Control(encoder_led=LedColor.yellow(), button_led=LedColor.white(), button=CtrlButton(steps=3)),
            5: Control(encoder_led=LedColor.white(), button_led=LedColor.white()),
            9: Control(encoder_led=LedColor.white(), button_led=LedColor.white()),
            13: Control(button_led=LedColor.green()),
            # 225L
            49: Control(encoder_led=LedColor.red(), button_led=LedColor.white(), button=CtrlButton(steps=3)),
            53: Control(encoder_led=LedColor.teal(), button_led=LedColor.white()),
            57: Control(encoder_led=LedColor.white(), button_led=LedColor.white()),
            61: Control(button_led=LedColor.green()),
            # 550L
            2: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11)),
            6: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7), button_led=LedColor.cyan()),
            10: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11)),
            14: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7)),
            50: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11)),
            54: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7), button_led=LedColor.cyan()),
            58: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11), button_led=LedColor.green()),
            62: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7), button_led=LedColor.green()),
            59: Control(button_led=LedColor.green()),
            63: Control(button_led=LedColor.green()),
            # 560L
            3: Control(encoder_led=LedColor.white()),
            7: Control(encoder_led=LedColor.white()),
            11: Control(encoder_led=LedColor.white()),
            15: Control(encoder_led=LedColor.white()),
            51: Control(encoder_led=LedColor.red()),
            55: Control(encoder_led=LedColor.white()),
            16: Control(encoder_led=LedColor.white()),
            20: Control(encoder_led=LedColor.white()),
            24: Control(encoder_led=LedColor.white()),
            28: Control(encoder_led=LedColor.white()),
            # Fader
            21: Control(encoder_led=LedColor.white()),
            25: Control(button_led=LedColor.orange()),
            29: Control(button_led=LedColor.red()),
        },

        "Chandler Limited Germanium Comp": {
            # Left / Mid
            0: Control(button_led=LedColor(1, 1, 0.5)),
            1: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            2: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            3: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            16: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            17: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            18: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            19: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            22: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            23: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            # Right / Side
            8: Control(button_led=LedColor(1, 1, 0.5)),
            9: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            10: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            11: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            24: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            25: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            26: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            27: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            30: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            31: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)), 
            # Side panel
            12: Control(button_led=LedColor.white()),
            13: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            14: Control(button_led=LedColor.cyan()),
            15: Control(button_led=LedColor.cyan()),
            28: Control(button_led=LedColor.cyan()),
            29: Control(button_led=LedColor.cyan()),
            51: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
        },

        "UADx SSL G Bus Compressor": {
            0: Control(encoder_led=LedColor.white()),
            1: Control(encoder_led=LedColor.white()),
            4: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=6, accel=False)),
            5: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=5, accel=False)),
            8: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            9: Control(button_led=LedColor.yellow()),
            12: Control(encoder_led=LedColor.white()),
            13: Control(encoder_led=LedColor.white()),
            48: Control(encoder_led=LedColor.white()),
            49: Control(button_led=LedColor.yellow()),
        },
        
        "UADx 1176AE Compressor": {
            8: Control(encoder_led=LedColor.white()),
            9: Control(encoder_led=LedColor.white()),
            10: Control(encoder_led=LedColor.purple()),
            14: Control(encoder_led=LedColor.purple(), button_led=LedColor.yellow(), beautify_button=False),
            11: Control(button_led=LedColor.white(), button=CtrlButton(steps=11)),
            24: Control(button_led=LedColor.white(), button=CtrlButton(steps=4)),
            28: Control(button_led=LedColor.yellow()),
            # HR / Mix
            5: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            13: Control(encoder_led=LedColor.yellow()),
        },

        "UADx 1176 Rev A Compressor": {
            8: Control(encoder_led=LedColor.white()),
            9: Control(encoder_led=LedColor.white()),
            10: Control(encoder_led=LedColor.purple()),
            14: Control(encoder_led=LedColor.purple(), button_led=LedColor.yellow(), beautify_button=False),
            11: Control(button_led=LedColor.white(), button=CtrlButton(steps=11)),
            24: Control(button_led=LedColor.white(), button=CtrlButton(steps=4)),
            28: Control(button_led=LedColor.yellow()),
            # HR / Mix
            5: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            13: Control(encoder_led=LedColor.yellow()),
        },

        "UADx 1176LN Rev E Compressor": {
            8: Control(encoder_led=LedColor.white()),
            9: Control(encoder_led=LedColor.white()),
            10: Control(encoder_led=LedColor.purple()),
            14: Control(encoder_led=LedColor.purple(), button_led=LedColor.yellow(), beautify_button=False),
            11: Control(button_led=LedColor.white(), button=CtrlButton(steps=11)),
            24: Control(button_led=LedColor.white(), button=CtrlButton(steps=4)),
            28: Control(button_led=LedColor.yellow()),
            # HR / Mix
            5: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            13: Control(encoder_led=LedColor.yellow()),
        },

        "UADx LA-2 Compressor": {
            8: Control(encoder_led=LedColor.yellow()),
            9: Control(encoder_led=LedColor.yellow()),
            10: Control(encoder_led=LedColor.white()),
            11: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=3, accel=False)),
            24: Control(encoder_led=LedColor.white()),
            25: Control(button_led=LedColor.red()),
        },

        "UADx LA-2A Gray Compressor": {
            8: Control(button_led=LedColor.red()),
            9: Control(encoder_led=LedColor.red()),
            10: Control(encoder_led=LedColor.white()),
            11: Control(encoder_led=LedColor.yellow()),
            24: Control(encoder_led=LedColor.white()),
            21: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=3, accel=False)),
            25: Control(button_led=LedColor.red()),
        },

        "UADx LA-2A Silver Compressor": {
            8: Control(button_led=LedColor.blue()),
            9: Control(encoder_led=LedColor.blue()),
            10: Control(encoder_led=LedColor.white()),
            11: Control(encoder_led=LedColor.blue()),
            24: Control(encoder_led=LedColor.white()),
            21: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=3, accel=False)),
            25: Control(button_led=LedColor.red()),
        },

        "UADx API 2500 Bus Compressor": {
            # Power / Mix
            5: Control(button_led=LedColor.yellow()),
            6: Control(encoder_led=LedColor.white()),
            # Compressor
            8: Control(encoder_led=LedColor.white()),
            9: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            10: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            11: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            24: Control(encoder_led=LedColor.white()),
            # Source / Headroom
            22: Control(button_led=LedColor.white()),
            23: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=7, accel=False)),
            # Tone
            25: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            26: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            27: Control(button_led=LedColor.white()),
            # Link
            14: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=7, accel=False)),
            15: Control(button_led=LedColor.green(), button=CtrlButton(steps=4)),
            # Output
            28: Control(button_led=LedColor.white()),
            29: Control(button_led=LedColor.white()),
            30: Control(button_led=LedColor.red()),
            31: Control(encoder_led=LedColor.red()), 
        },

        "UADx dbx 160 Compressor": {
            8: Control(encoder_led=LedColor.yellow()), 
            9: Control(encoder_led=LedColor.yellow()), 
            10: Control(encoder_led=LedColor.yellow()), 
            12: Control(button_led=LedColor.white()),
            13: Control(button_led=LedColor.white()),
            15: Control(encoder_led=LedColor.white()), 
        },

        "UADx Verve Analog Machines": {
            12: Control(encoder_led=LedColor.white()),
            13: Control(encoder_led=LedColor.white()),
            14: Control(encoder_led=LedColor.white()),
        },

        "NFuse": {
            # IO
            56: Control(button_led=LedColor.yellow()),
            60: Control(button_led=LedColor.yellow()),
            61: Control(button_led=LedColor.yellow()),
            62: Control(button_led=LedColor.yellow()),
            63: Control(button_led=LedColor.yellow()),
            # F Levels
            48: Control(encoder_led=LedColor.white()),
            49: Control(encoder_led=LedColor.white()),
            52: Control(encoder_led=LedColor.white()),
            # F Sat
            0: Control(encoder_led=LedColor.green()),
            1: Control(encoder_led=LedColor.green()),
            # F EQ
            4: Control(encoder_led=LedColor.purple()),
            5: Control(encoder_led=LedColor.pink()),
            8: Control(encoder_led=LedColor.purple()),
            9: Control(encoder_led=LedColor.pink()),
            # F Comp 1
            2: Control(encoder_led=LedColor.orange()),
            3: Control(encoder_led=LedColor.orange()),
            6: Control(encoder_led=LedColor.orange()),
            7: Control(encoder_led=LedColor.orange()),
            11: Control(encoder_led=LedColor.orange()),
            # F Comp 2
            10: Control(encoder_led=LedColor.brown()),
            14: Control(encoder_led=LedColor.brown()),
            15: Control(encoder_led=LedColor.brown()),
            # F Stereo
            12: Control(encoder_led=LedColor.cyan()),
            13: Control(encoder_led=LedColor.cyan()),
            # N Levels
            50: Control(encoder_led=LedColor.teal()),
            51: Control(encoder_led=LedColor.teal()),
            54: Control(encoder_led=LedColor.teal()),
            # N Sat
            16: Control(encoder_led=LedColor.teal()),
            17: Control(encoder_led=LedColor.yellow(), button_led=LedColor.pink(), beautify_button=False),
            55: Control(encoder_led=LedColor.grey()),
            # N EQ
            20: Control(encoder_led=LedColor.teal()),
            21: Control(encoder_led=LedColor.yellow()),
            24: Control(encoder_led=LedColor.teal()),
            25: Control(encoder_led=LedColor.yellow()),
            # N Comp 1
            18: Control(encoder_led=LedColor.teal()),
            19: Control(encoder_led=LedColor.yellow()),
            22: Control(encoder_led=LedColor.teal()),
            23: Control(encoder_led=LedColor.yellow()),
            27: Control(encoder_led=LedColor.grey()),
            26: Control(button_led=LedColor.pink()),
            53: Control(encoder_led=LedColor.grey()),
            # N Stereo
            28: Control(encoder_led=LedColor.teal()),
            29: Control(encoder_led=LedColor.yellow()),
        },

        "UADx Empirical Labs Distressor": {
            # Controls
            12: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            13: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            14: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            15: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            28: Control(encoder_led=LedColor.white()),
            # Buttons
            8: Control(button_led=LedColor.red()),
            9: Control(button_led=LedColor.white(), button=CtrlButton(steps=8)),
            10: Control(button_led=LedColor.white(), button=CtrlButton(steps=8)),
            11: Control(button_led=LedColor.white(), button=CtrlButton(steps=6)),
        },

        "UADx Manley Variable Mu Compressor": {
            # L side
            12: Control(button_led=LedColor.white()),
            13: Control(button_led=LedColor.white()),
            14: Control(button_led=LedColor.white()),
            10: Control(button_led=LedColor.white()),
            # Mid
            11: Control(button_led=LedColor.yellow()),
            4: Control(button_led=LedColor.pink()),
            22: Control(button_led=LedColor.pink()),
            # R side
            24: Control(button_led=LedColor.white()),
            28: Control(button_led=LedColor.white()),
            29: Control(button_led=LedColor.white()),
            30: Control(button_led=LedColor.white()),
            # Main L + R
            1: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=5, accel=False)),
            2: Control(encoder_led=LedColor.purple()),
            3: Control(encoder_led=LedColor.purple()),
            16: Control(encoder_led=LedColor.purple()),
            17: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=5, accel=False)),
            5: Control(encoder_led=LedColor.purple()),
            6: Control(encoder_led=LedColor.purple()),
            7: Control(encoder_led=LedColor.purple()),
            20: Control(encoder_led=LedColor.purple()),
            21: Control(encoder_led=LedColor.purple()),
            # Headroom
            51: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=9, accel=False)),
        },

        "UADx Manley Massive Passive EQ": {
            # Top
            0: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            1: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            2: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            3: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            16: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            17: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            18: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            19: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            # dB & Shelf bell
            4: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            5: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            6: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            7: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            20: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            21: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            22: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            23: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            # Bandwidth
            8: Control(encoder_led=LedColor.purple()),
            9: Control(encoder_led=LedColor.purple()),
            10: Control(encoder_led=LedColor.purple()),
            11: Control(encoder_led=LedColor.purple()),
            24: Control(encoder_led=LedColor.purple()),
            25: Control(encoder_led=LedColor.purple()),
            26: Control(encoder_led=LedColor.purple()),
            27: Control(encoder_led=LedColor.purple()),
            # Freq
            12: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            13: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            14: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            15: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            28: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            29: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            30: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            31: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            # Mid panel
            48: Control(button_led=LedColor.blue()),
            49: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=2, accel=False)),
            50: Control(button_led=LedColor.blue()),
            53: Control(button_led=LedColor.white()),
            52: Control(encoder_led=LedColor.purple()),
            54: Control(encoder_led=LedColor.purple()),
            56: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            58: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            60: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            62: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
        },

        "UADx Manley Massive Passive MST": {
            # Top
            0: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            1: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            2: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            3: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            16: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            17: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            18: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            19: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            # dB & Shelf bell
            4: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            5: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            6: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            7: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            20: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            21: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            22: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            23: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            # Bandwidth
            8: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            9: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            10: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            11: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            24: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            25: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            26: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            27: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            # Freq
            12: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            13: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            14: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            15: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            28: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            29: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            30: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            31: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            # Mid panel
            48: Control(button_led=LedColor.blue()),
            49: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=2, accel=False)),
            50: Control(button_led=LedColor.blue()),
            53: Control(button_led=LedColor.white()),
            52: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            54: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            56: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            58: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            60: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            62: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
        },

        "UADx Manley Tube Preamp": {
            4: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=2)),
            8: Control(encoder_led=LedColor.purple()),
            6: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=5)),
            10: Control(encoder_led=LedColor.purple()),
            1: Control(button_led=LedColor.blue()),
            5: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            9: Control(button_led=LedColor.white()),
            13: Control(button_led=LedColor.white()),
            49: Control(button_led=LedColor.white()),
        },

        "UADx LA-3A Compressor": {
            4: Control(encoder_led=LedColor.red()),
            7: Control(encoder_led=LedColor.red()),
            9: Control(encoder_led=LedColor.red()),
            10: Control(encoder_led=LedColor.red()),
            12: Control(button_led=LedColor.red(), button=CtrlButton(steps=3)),
            15: Control(button_led=LedColor.red()),
        },

        "UADx Fairchild 670 Compressor": {
            0: Control(button_led=LedColor.orange()),
            1: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            2: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            3: Control(encoder_led=LedColor.red()),
            16: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=6, accel=False)),
            5: Control(encoder_led=LedColor.yellow()),
            20: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=2, accel=False)),
            9: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            10: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            11: Control(encoder_led=LedColor.red()),
            24: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=6, accel=False)),
            13: Control(encoder_led=LedColor.yellow()),
            # Lower panel
            48: Control(encoder_led=LedColor.red()),
            49: Control(encoder_led=LedColor.red()),
            50: Control(button_led=LedColor.white()),
            51: Control(button_led=LedColor.white()),
            52: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            53: Control(encoder_led=LedColor.white()),
            54: Control(encoder_led=LedColor.white()),
            55: Control(encoder_led=LedColor.blue()),
        },

        "UADx Fairchild 660 Compressor": { 
            0: Control(button_led=LedColor.orange()),
            1: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            2: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            3: Control(encoder_led=LedColor.red()),
            16: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=6, accel=False)),
            4: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            5: Control(encoder_led=LedColor.yellow()),
            8: Control(encoder_led=LedColor.red()),
            9: Control(encoder_led=LedColor.white()),
            10: Control(encoder_led=LedColor.red()),
            24: Control(encoder_led=LedColor.blue()),
        },

        "SSL Native Bus Compressor 2": {
            0: Control(encoder_led=LedColor.blue()),
            1: Control(encoder_led=LedColor.blue()),
            4: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            5: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            8: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            9: Control(button_led=LedColor.yellow(), button=CtrlButton(invert_intensity=True)),
            12: Control(encoder_led=LedColor.blue()),
            13: Control(encoder_led=LedColor.blue()),
            # Side panel
            10: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)),
            14: Control(button_led=LedColor.yellow()),
            15: Control(button_led=LedColor.yellow()),
        },

        "Maag EQ4": {
            12: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=21, accel=False)),
            13: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            14: Control(encoder_led=LedColor.green(), encoder=CtrlEncoder(steps=21, accel=False)),
            15: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            28: Control(encoder_led=LedColor.orange(), encoder=CtrlEncoder(steps=21, accel=False)),
            29: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=21, accel=False)),
            30: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            31: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=21, accel=False)),
            48: Control(button_led=LedColor.green()),
        },

        "SPL PQ": {
            # L LF
            0: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False, encoder=CtrlEncoder(steps=41)),
            4: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False, encoder=CtrlEncoder(steps=41)),
            8: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False, encoder=CtrlEncoder(steps=41)),
        },

        "Pre 1973": {
            # L
            0: Control(encoder_led=LedColor.cyan()),
            4: Control(encoder_led=LedColor.cyan()),
            5: Control(encoder_led=LedColor.cyan()),
            8: Control(encoder_led=LedColor.cyan()),
            9: Control(encoder_led=LedColor.cyan()),
            12: Control(encoder_led=LedColor.blue()),
            48: Control(button_led=LedColor.yellow()),
            49: Control(button_led=LedColor.yellow()),
            # R
            2: Control(encoder_led=LedColor.cyan()),
            6: Control(encoder_led=LedColor.cyan()),
            7: Control(encoder_led=LedColor.cyan()),
            10: Control(encoder_led=LedColor.cyan()),
            11: Control(encoder_led=LedColor.cyan()),
            14: Control(encoder_led=LedColor.blue()),
            50: Control(button_led=LedColor.yellow()),
            51: Control(button_led=LedColor.yellow()),
            # AMP L
            17: Control(encoder_led=LedColor.red()),
            21: Control(encoder_led=LedColor.blue()),
            25: Control(button_led=LedColor.cyan()),
            # AMP R
            18: Control(encoder_led=LedColor.red()),
            22: Control(encoder_led=LedColor.blue()),
            26: Control(button_led=LedColor.cyan()),
            # Link / LR / MS
            29: Control(button_led=LedColor.yellow()),
            30: Control(button_led=LedColor.white()),
            # Bypass
            31: Control(button_led=LedColor.cyan(), button=CtrlButton(invert_intensity=True)),
        },

        "Comp TUBE-STA": {
            8: Control(encoder_led=LedColor.orange()),
            11: Control(encoder_led=LedColor.orange()),
            9: Control(encoder_led=LedColor.white()),
            5: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            10: Control(button_led=LedColor.red()),
            15: Control(encoder_led=LedColor.white()),
            # Advanced
            48: Control(button_led=LedColor.red()),
            52: Control(encoder_led=LedColor.white()),
            53: Control(encoder_led=LedColor.orange(), encoder=CtrlEncoder(steps=5, accel=False)),
            54: Control(button_led=LedColor.red()),
            55: Control(button_led=LedColor.green()), 
            56: Control(encoder_led=LedColor.white()),
            57: Control(encoder_led=LedColor.white()),
            58: Control(encoder_led=LedColor.white()),
            59: Control(encoder_led=LedColor.white()),
        },

        "Pre TridA": {
            # L Top
            1: Control(button_led=LedColor.yellow()),
            2: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            3: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            6: Control(encoder_led=LedColor.pink()),
            7: Control(encoder_led=LedColor.pink()),
            # L Bottom
            10: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            11: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            13: Control(button_led=LedColor.yellow()),
            14: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            15: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            # R Top
            16: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            17: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            18: Control(button_led=LedColor.yellow()),
            20: Control(encoder_led=LedColor.pink()),
            21: Control(encoder_led=LedColor.pink()),
            # R Bottom
            24: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            25: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            28: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            29: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            30: Control(button_led=LedColor.yellow()),
            # Drive
            49: Control(encoder_led=LedColor.pink()),
            50: Control(encoder_led=LedColor.pink()),
            53: Control(button_led=LedColor.red()),
            54: Control(button_led=LedColor.red()),
            57: Control(button_led=LedColor.green()),
            58: Control(button_led=LedColor.green()),
            61: Control(encoder_led=LedColor.purple()),
            62: Control(encoder_led=LedColor.purple()),
            59: Control(button_led=LedColor.yellow()),
            63: Control(button_led=LedColor.yellow()),
        },

        "Tube-Tech Blue Tone": {
            9: Control(encoder_led=LedColor.blue()),
            10: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=8, accel=False)),
            12: Control(encoder_led=LedColor.blue()),
            13: Control(encoder_led=LedColor.blue()),
            14: Control(encoder_led=LedColor.blue()),
            15: Control(encoder_led=LedColor.blue()),
        },

        "AMEK EQ 200": {
            # Power
            0: Control(button_led=LedColor.blue()),
            # Filters
            4: Control(encoder_led=LedColor.white(), button_led=LedColor.red(), encoder=CtrlEncoder(invert_intensity=True), beautify_button=False),
            8: Control(encoder_led=LedColor.white(), button_led=LedColor.red(), beautify_button=False),
            # Low
            1: Control(button_led=LedColor.red()),
            5: Control(encoder_led=LedColor.red(), button_led=LedColor.grey()),
            9: Control(encoder_led=LedColor.red()),
            13: Control(encoder_led=LedColor.red()),
            # Low M
            2: Control(button_led=LedColor.red()),
            6: Control(encoder_led=LedColor.yellow(), button_led=LedColor.grey()),
            10: Control(encoder_led=LedColor.yellow()),
            14: Control(encoder_led=LedColor.yellow()),
            # Mid
            3: Control(button_led=LedColor.red()),
            7: Control(encoder_led=LedColor.green(), button_led=LedColor.grey()),
            11: Control(encoder_led=LedColor.green()),
            15: Control(encoder_led=LedColor.green()),
            # High M
            16: Control(button_led=LedColor.red()),
            20: Control(encoder_led=LedColor.brown(), button_led=LedColor.grey()),
            24: Control(encoder_led=LedColor.brown()),
            28: Control(encoder_led=LedColor.brown()),
            # High
            17: Control(button_led=LedColor.red()),
            21: Control(encoder_led=LedColor.blue(), button_led=LedColor.grey()),
            25: Control(encoder_led=LedColor.blue()),
            29: Control(encoder_led=LedColor.blue()),
            # Mid panel
            22: Control(encoder_led=LedColor.white(), button_led=LedColor.red()),
            26: Control(button_led=LedColor.red()),
            27: Control(button_led=LedColor.red()),
            30: Control(button_led=LedColor.red()),
            # Levels
            48: Control(encoder_led=LedColor.white()),
            51: Control(encoder_led=LedColor.white()),
            # Mono maker
            49: Control(encoder_led=LedColor.white(), button_led=LedColor.red()), 
            50: Control(encoder_led=LedColor.white(), button_led=LedColor.red()), 
            # THD
            54: Control(encoder_led=LedColor.white(), button_led=LedColor.red()), 
            # TMT
            52: Control(button_led=LedColor.orange()),
            53: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=20, accel=False)),
            # MS/PL
            57: Control(button_led=LedColor.red()),
            58: Control(button_led=LedColor.red()),
        },

        "Black Box Analog Design HG-2MS": {
            # L / Mid
            0: Control(encoder_led=LedColor.white()),
            1: Control(encoder_led=LedColor.white()),
            2: Control(encoder_led=LedColor.white()),
            3: Control(encoder_led=LedColor.white()),
            16: Control(encoder_led=LedColor.white()),
            17: Control(encoder_led=LedColor.white()),
            18: Control(encoder_led=LedColor.white()),
            4: Control(button_led=LedColor.blue()),
            5: Control(button_led=LedColor.blue()),
            6: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)),
            7: Control(button_led=LedColor.blue(), encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=5, accel=False)),
            21: Control(button_led=LedColor.blue()),
            22: Control(button_led=LedColor.blue()),
            # R / Side
            8: Control(encoder_led=LedColor.white()),
            9: Control(encoder_led=LedColor.white()),
            10: Control(encoder_led=LedColor.white()),
            11: Control(encoder_led=LedColor.white()),
            24: Control(encoder_led=LedColor.white()),
            25: Control(encoder_led=LedColor.white()),
            26: Control(encoder_led=LedColor.white()),
            12: Control(button_led=LedColor.blue()),
            13: Control(button_led=LedColor.blue()),
            14: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)),
            15: Control(button_led=LedColor.blue(), encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=5, accel=False)),
            29: Control(button_led=LedColor.blue()),
            30: Control(button_led=LedColor.blue()),
            # BX strip
            48: Control(button_led=LedColor.red()),
            49: Control(encoder_led=LedColor.orange(), encoder=CtrlEncoder(steps=20, accel=False)),
            50: Control(button_led=LedColor.blue()),
            51: Control(button_led=LedColor.blue()),
            53: Control(encoder_led=LedColor.white()),
            54: Control(button_led=LedColor.blue(), button=CtrlButton(steps=3)),
            56: Control(encoder_led=LedColor.white()),
            57: Control(encoder_led=LedColor.white()),
            58: Control(encoder_led=LedColor.white()),
            59: Control(encoder_led=LedColor.white()),
            # More
            61: Control(button_led=LedColor.red()),
            62: Control(button_led=LedColor.blue()),
        },

        "SSL LMC+": {
            # Filters
            5: Control(encoder_led=LedColor.white()),
            6: Control(button_led=LedColor.yellow()),
            7: Control(encoder_led=LedColor.white()),
            # Amount
            9: Control(button_led=LedColor.yellow()),
            10: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=101)),
            11: Control(button_led=LedColor.yellow()),
            # Routing
            13: Control(button_led=LedColor.yellow()),
            14: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=101)),
            15: Control(button_led=LedColor.yellow()),

            # IO
            48: Control(button_led=LedColor.yellow(), button=CtrlButton(invert_intensity=True)),
            49: Control(encoder_led=LedColor.white()),
            50: Control(encoder_led=LedColor.white()),
            51: Control(button_led=LedColor.yellow()),
        },

        "SSL Blitzer": {
            0: Control(encoder_led=LedColor.white()),
            1: Control(button_led=LedColor.purple()),
            2: Control(button_led=LedColor.red()),
            3: Control(encoder_led=LedColor.purple()),
            16: Control(encoder_led=LedColor.white()),
            5: Control(encoder_led=LedColor.purple()),
            6: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=9, accel=False)),
            7: Control(encoder_led=LedColor.purple()),
            9: Control(encoder_led=LedColor.purple()),
            10: Control(button_led=LedColor.cyan()),
            11: Control(encoder_led=LedColor.purple()),
            12: Control(encoder_led=LedColor.blue()),
            13: Control(encoder_led=LedColor.blue()),
            14: Control(encoder_led=LedColor.blue()),
            15: Control(encoder_led=LedColor.blue()),
            28: Control(button_led=LedColor.purple()),
        },

        "TR5 EQ-73": {
            8: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=5, accel=False)),
            9: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=65)),
            10: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=7, accel=False)),
            11: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=65)),
            24: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=45)),
            12: Control(button_led=LedColor.yellow()),
            13: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            14: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=22, accel=False)),
            15: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=5, accel=False)),
            25: Control(button_led=LedColor.yellow()),
            29: Control(button_led=LedColor.yellow()),
        },

        "RoyalCompressor": {
            8: Control(encoder_led=LedColor.red()),
            12: Control(button_led=LedColor.orange(), button=CtrlButton(invert_intensity=True)),
            13: Control(encoder_led=LedColor.lightgreen()),
            10: Control(encoder_led=LedColor.lightgreen(), encoder=CtrlEncoder(steps=3, accel=False)),
            14: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=12, accel=False)),
            11: Control(encoder_led=LedColor.lightgreen(), encoder=CtrlEncoder(steps=2, accel=False)),
            15: Control(encoder_led=LedColor.lightgreen()),
            28: Control(encoder_led=LedColor.lightgreen()),
            25: Control(encoder_led=LedColor.lightgreen()),
        },

        "Chandler Limited Zener Limiter": {
            # L
            0: Control(button_led=LedColor.white()),
            4: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            8: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            9: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)),
            10: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            11: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            7: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=11, accel=False)),
            3: Control(button_led=LedColor.white()),
            # R
            16: Control(button_led=LedColor.white()),
            20: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            24: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            25: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)),
            26: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            27: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            23: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=11, accel=False)),
            19: Control(button_led=LedColor.white()),
            # M
            49: Control(button_led=LedColor.cyan()),
            50: Control(button_led=LedColor.cyan()),
            53: Control(button_led=LedColor.cyan()),
            54: Control(button_led=LedColor.cyan()),
            57: Control(button_led=LedColor.white()),
            58: Control(encoder_led=LedColor.white()),
        },

        "Chandler Limited Curve Bender": {
            # L
            0: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=8, accel=False)),
            1: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            2: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            3: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=9, accel=False)),
            4: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            5: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            6: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            7: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            8: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            9: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            10: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            11: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            # R
            16: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=8, accel=False)),
            17: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            18: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            19: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=9, accel=False)),
            20: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            21: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            22: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            23: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            24: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            25: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            26: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            27: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            # Filter
            48: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            52: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            51: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            55: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            # Mid
            49: Control(button_led=LedColor.cyan()),
            50: Control(button_led=LedColor.cyan()),
            53: Control(button_led=LedColor.cyan()),
            54: Control(button_led=LedColor.cyan()),
            57: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            58: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
        },

        "Complexx": {
            # L
            48: Control(encoder_led=LedColor.purple()),
            52: Control(encoder_led=LedColor.white()),
            0: Control(encoder_led=LedColor.white()),
            1: Control(encoder_led=LedColor.teal()),
            2: Control(encoder_led=LedColor.yellow()),
            3: Control(encoder_led=LedColor.red()),
            4: Control(button_led=LedColor.orange(), button=CtrlButton(steps=3)),
            5: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            6: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            7: Control(button_led=LedColor.teal(), button=CtrlButton(steps=3)),
            8: Control(encoder_led=LedColor.white()),
            9: Control(encoder_led=LedColor.teal()),
            10: Control(encoder_led=LedColor.yellow()),
            11: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            # R
            51: Control(encoder_led=LedColor.purple()),
            55: Control(encoder_led=LedColor.white()),
            19: Control(encoder_led=LedColor.white()),
            18: Control(encoder_led=LedColor.teal()),
            17: Control(encoder_led=LedColor.yellow()),
            16: Control(encoder_led=LedColor.red()),
            23: Control(button_led=LedColor.orange(), button=CtrlButton(steps=3)),
            22: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            21: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            20: Control(button_led=LedColor.teal(), button=CtrlButton(steps=3)),
            27: Control(encoder_led=LedColor.white()),
            26: Control(encoder_led=LedColor.teal()),
            25: Control(encoder_led=LedColor.yellow()),
            24: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            # M
            53: Control(encoder_led=LedColor.white()),
            54: Control(encoder_led=LedColor.white()),
        },

        "ADC1 Compressor": {
            # L
            0: Control(encoder_led=LedColor.red()),
            1: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=4, accel=False)),
            2: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            3: Control(encoder_led=LedColor.white()),
            16: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            17: Control(encoder_led=LedColor.teal()),
            # R
            4: Control(encoder_led=LedColor.red()),
            5: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=4, accel=False)),
            6: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            7: Control(encoder_led=LedColor.white()),
            20: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            21: Control(encoder_led=LedColor.teal()),
        },

        ### Synths

        "Acid V": {
            # Top row
            0: Control(button_led=LedColor.white()),
            1: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=25, accel=False)),
            2: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            3: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            16: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            17: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            18: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            # Mid row
            4: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=3, accel=False, invert=True)),
            5: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=3, accel=False, invert=True)),
            6: Control(encoder_led=LedColor.lime()),
            7: Control(encoder_led=LedColor.lime()),
            20: Control(encoder_led=LedColor.lime()),
            21: Control(encoder_led=LedColor.lime()),
            22: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=14, accel=False)),
            23: Control(encoder_led=LedColor.lime()),
            # Advanced
            13: Control(encoder_led=LedColor.green()),
            14: Control(encoder_led=LedColor.green()),
            15: Control(encoder_led=LedColor.green()),
            28: Control(encoder_led=LedColor.green()),
            29: Control(encoder_led=LedColor.green()),
            30: Control(encoder_led=LedColor.green()),
            31: Control(encoder_led=LedColor.green()),
        },
    }
}