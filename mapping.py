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
    r: int = 0
    g: int = 0
    b: int = 0

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
            32: Control(button_led=LedColor.white()),
            36: Control(encoder_led=LedColor.blue()),
            40: Control(encoder_led=LedColor.blue()),
            # Row 1
            33: Control(encoder_led=LedColor.blue()),
            34: Control(encoder_led=LedColor.blue()),
            35: Control(encoder_led=LedColor.blue()),
            48: Control(encoder_led=LedColor.blue()),
            49: Control(encoder_led=LedColor.blue()),
            # Row 2
            37: Control(encoder_led=LedColor.blue()),
            38: Control(encoder_led=LedColor.blue()),
            39: Control(encoder_led=LedColor.blue()),
            52: Control(encoder_led=LedColor.blue()),
            53: Control(encoder_led=LedColor.blue()),
            # Row 3
            41: Control(encoder_led=LedColor.blue()),
            42: Control(encoder_led=LedColor.blue()),
            43: Control(encoder_led=LedColor.blue()),
            56: Control(encoder_led=LedColor.blue()),
            57: Control(encoder_led=LedColor.blue()),
            # Side chain / Control channel
            44: Control(button_led=LedColor.white()),
            45: Control(button_led=LedColor.red()),
            46: Control(button_led=LedColor.red()),
            47: Control(button_led=LedColor.red()),
            # Mute
            60: Control(button_led=LedColor.white()),
            61: Control(button_led=LedColor.white()),
            62: Control(button_led=LedColor.white()),
            # Balance, Output, in/ext, dry/wet
            51: Control(encoder_led=LedColor.blue()),
            55: Control(encoder_led=LedColor.blue()),
            59: Control(button_led=LedColor.red(), button=CtrlButton(invert_intensity=True)),
            63: Control(encoder_led=LedColor.blue()),
        },

        "Tube-Tech CL 1B mk II": {
            # Controls
            40: Control(encoder_led=LedColor.blue()),
            41: Control(encoder_led=LedColor.blue()),
            42: Control(encoder_led=LedColor.blue()),
            43: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3)),
            44: Control(encoder_led=LedColor.blue()),
            45: Control(encoder_led=LedColor.blue()),
            46: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3)),
            47: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=2)),
            # On off
            60: Control(button_led=LedColor.red()),
            # Sidechain 
            80: Control(button_led=LedColor.white(), button=CtrlButton(steps=2)),
            81: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            83: Control(encoder_led=LedColor.blue()),
        },

        "Tube-Tech Equalizers mk II": {
            # Lows
            32: Control(encoder_led=LedColor.blue()),
            33: Control(encoder_led=LedColor.blue()),
            36: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=4, accel=False)),
            # Mid
            37: Control(encoder_led=LedColor.cyan()),
            38: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=10, accel=False)),
            34: Control(encoder_led=LedColor.cyan()),
            # Atten
            35: Control(encoder_led=LedColor.blue()),
            48: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)), 
            # Output Gain
            52: Control(encoder_led=LedColor.blue(), button_led=LedColor.red(), beautify_button=False),
            # MEQ Peak L
            40: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)), 
            41: Control(encoder_led=LedColor.blue()), 
            # MEQ DIP
            42: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=11, accel=False)), 
            43: Control(encoder_led=LedColor.cyan()), 
            # MEQ Peak H
            56: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)), 
            57: Control(encoder_led=LedColor.blue()), 
            # MEQ Output Gain
            58: Control(encoder_led=LedColor.blue(), button_led=LedColor.red(), beautify_button=False),
        },

        "UADx SSL E Channel Strip": {
            # Line & Mic
            32: Control(button_led=LedColor.white(), encoder_led=LedColor.white(), beautify_button=False),
            33: Control(button_led=LedColor.white()),
            36: Control(button_led=LedColor.grey(), encoder_led=LedColor.red(), beautify_button=False),
            37: Control(button_led=LedColor.red()),
            # Dynamics (comp)
            40: Control(encoder_led=LedColor.white()),
            41: Control(encoder_led=LedColor.white(), button_led=LedColor.yellow(), beautify_button=False),
            44: Control(encoder_led=LedColor.white(), button_led=LedColor.red(), beautify_button=False),
            # Dynamics (exp/gate)
            45: Control(encoder_led=LedColor.green()),
            80: Control(encoder_led=LedColor.green()),
            81: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            84: Control(encoder_led=LedColor.green(), button_led=LedColor.red(), beautify_button=False),
            # Dynamics buttons
            85: Control(button_led=LedColor.green()),
            88: Control(button_led=LedColor.red()),
            89: Control(button_led=LedColor.yellow()),
            # Filters
            92: Control(encoder_led=LedColor.grey(), button_led=LedColor.red(), beautify_button=False, beautify_encoder=False),
            93: Control(encoder_led=LedColor.grey(), button_led=LedColor.yellow(), beautify_button=False, beautify_encoder=False),
            # EQ
            34: Control(encoder_led=LedColor.red()),
            35: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False),
            38: Control(encoder_led=LedColor.green()),
            39: Control(encoder_led=LedColor.green()),
            42: Control(encoder_led=LedColor.green()),
            43: Control(button_led=LedColor.yellow()),
            46: Control(encoder_led=LedColor.blue()),
            47: Control(encoder_led=LedColor.blue()),
            82: Control(encoder_led=LedColor.blue()),
            83: Control(encoder_led=LedColor.brown(), button_led=LedColor.grey(), beautify_button=False),
            86: Control(encoder_led=LedColor.brown()),
            # EQ buttons
            87: Control(button_led=LedColor.green()),
            90: Control(button_led=LedColor.red()),
            91: Control(button_led=LedColor.yellow()),
            # Power
            94: Control(button_led=LedColor(1, 1, 0.5)),
            # Fader & Output
            52: Control(button_led=LedColor.green()),
            56: Control(encoder_led=LedColor.white()),
            60: Control(encoder_led=LedColor.white()),
        },

        "UADx API Vision Channel Strip": {
            # 212L
            32: Control(encoder_led=LedColor.red(), button_led=LedColor.red(), beautify_button=False),
            36: Control(encoder_led=LedColor.green(), button_led=LedColor.green(), beautify_button=False),
            40: Control(button_led=LedColor.red()),
            44: Control(button_led=LedColor.green()),
            # 215L
            80: Control(encoder_led=LedColor.orange()),
            84: Control(button_led=LedColor.green()),
            88: Control(encoder_led=LedColor.orange()),
            92: Control(button_led=LedColor.green()),
            # 235L
            33: Control(encoder_led=LedColor.yellow(), button_led=LedColor.white(), button=CtrlButton(steps=3)),
            37: Control(encoder_led=LedColor.white(), button_led=LedColor.white()),
            41: Control(encoder_led=LedColor.white(), button_led=LedColor.white()),
            45: Control(button_led=LedColor.green()),
            # 225L
            81: Control(encoder_led=LedColor.red(), button_led=LedColor.white(), button=CtrlButton(steps=3)),
            85: Control(encoder_led=LedColor.teal(), button_led=LedColor.white()),
            89: Control(encoder_led=LedColor.white(), button_led=LedColor.white()),
            93: Control(button_led=LedColor.green()),
            # 550L
            34: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11)),
            38: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7), button_led=LedColor.cyan()),
            42: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11)),
            46: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7)),
            82: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11)),
            86: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7), button_led=LedColor.cyan()),
            90: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=11), button_led=LedColor.green()),
            94: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7), button_led=LedColor.green()),
            91: Control(button_led=LedColor.green()),
            95: Control(button_led=LedColor.green()),
            # 560L
            35: Control(encoder_led=LedColor.white()),
            39: Control(encoder_led=LedColor.white()),
            43: Control(encoder_led=LedColor.white()),
            47: Control(encoder_led=LedColor.white()),
            83: Control(encoder_led=LedColor.red()),
            87: Control(encoder_led=LedColor.white()),
            48: Control(encoder_led=LedColor.white()),
            52: Control(encoder_led=LedColor.white()),
            56: Control(encoder_led=LedColor.white()),
            60: Control(encoder_led=LedColor.white()),
            # Fader
            53: Control(encoder_led=LedColor.white()),
            57: Control(button_led=LedColor.orange()),
            61: Control(button_led=LedColor.red()),
        },

        "Chandler Limited Germanium Comp": {
            # Left / Mid
            32: Control(button_led=LedColor(1, 1, 0.5)),
            33: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            34: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            35: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            48: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            49: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            50: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            51: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            54: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            55: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            # Right / Side
            40: Control(button_led=LedColor(1, 1, 0.5)),
            41: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            42: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            43: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            56: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            57: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
            58: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            59: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            62: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            63: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)), 
            # Side panel
            44: Control(button_led=LedColor.white()),
            45: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=101)),
            46: Control(button_led=LedColor.cyan()),
            47: Control(button_led=LedColor.cyan()),
            60: Control(button_led=LedColor.cyan()),
            61: Control(button_led=LedColor.cyan()),
            83: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=101)),
        },

        "UADx SSL G Bus Compressor": {
            32: Control(encoder_led=LedColor.white()),
            33: Control(encoder_led=LedColor.white()),
            36: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=6, accel=False)),
            37: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=5, accel=False)),
            40: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            41: Control(button_led=LedColor.yellow()),
            44: Control(encoder_led=LedColor.white()),
            45: Control(encoder_led=LedColor.white()),
            80: Control(encoder_led=LedColor.white()),
            81: Control(button_led=LedColor.yellow()),
        },
        
        "UADx 1176AE Compressor": {
            40: Control(encoder_led=LedColor.white()),
            41: Control(encoder_led=LedColor.white()),
            42: Control(encoder_led=LedColor.purple()),
            46: Control(encoder_led=LedColor.purple(), button_led=LedColor.yellow(), beautify_button=False),
            43: Control(button_led=LedColor.white(), button=CtrlButton(steps=11)),
            56: Control(button_led=LedColor.white(), button=CtrlButton(steps=4)),
            60: Control(button_led=LedColor.yellow()),
            # HR / Mix
            37: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            45: Control(encoder_led=LedColor.yellow()),
        },

        "UADx 1176 Rev A Compressor": {
            40: Control(encoder_led=LedColor.white()),
            41: Control(encoder_led=LedColor.white()),
            42: Control(encoder_led=LedColor.purple()),
            46: Control(encoder_led=LedColor.purple(), button_led=LedColor.yellow(), beautify_button=False),
            43: Control(button_led=LedColor.white(), button=CtrlButton(steps=11)),
            56: Control(button_led=LedColor.white(), button=CtrlButton(steps=4)),
            60: Control(button_led=LedColor.yellow()),
            # HR / Mix
            37: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            45: Control(encoder_led=LedColor.yellow()),
        },

        "UADx 1176LN Rev E Compressor": {
            40: Control(encoder_led=LedColor.white()),
            41: Control(encoder_led=LedColor.white()),
            42: Control(encoder_led=LedColor.purple()),
            46: Control(encoder_led=LedColor.purple(), button_led=LedColor.yellow(), beautify_button=False),
            43: Control(button_led=LedColor.white(), button=CtrlButton(steps=11)),
            56: Control(button_led=LedColor.white(), button=CtrlButton(steps=4)),
            60: Control(button_led=LedColor.yellow()),
            # HR / Mix
            37: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            45: Control(encoder_led=LedColor.yellow()),
        },

        "UADx LA-2 Compressor": {
            40: Control(encoder_led=LedColor.yellow()),
            41: Control(encoder_led=LedColor.yellow()),
            42: Control(encoder_led=LedColor.white()),
            43: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=3, accel=False)),
            56: Control(encoder_led=LedColor.white()),
            57: Control(button_led=LedColor.red()),
        },

        "UADx LA-2A Gray Compressor": {
            40: Control(button_led=LedColor.red()),
            41: Control(encoder_led=LedColor.red()),
            42: Control(encoder_led=LedColor.white()),
            43: Control(encoder_led=LedColor.yellow()),
            56: Control(encoder_led=LedColor.white()),
            53: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=3, accel=False)),
            57: Control(button_led=LedColor.red()),
        },

        "UADx LA-2A Silver Compressor": {
            40: Control(button_led=LedColor.blue()),
            41: Control(encoder_led=LedColor.blue()),
            42: Control(encoder_led=LedColor.white()),
            43: Control(encoder_led=LedColor.blue()),
            56: Control(encoder_led=LedColor.white()),
            53: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=3, accel=False)),
            57: Control(button_led=LedColor.red()),
        },

        "UADx API 2500 Bus Compressor": {
            # Power / Mix
            37: Control(button_led=LedColor.yellow()),
            38: Control(encoder_led=LedColor.white()),
            # Compressor
            40: Control(encoder_led=LedColor.white()),
            41: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            42: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            43: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            56: Control(encoder_led=LedColor.white()),
            # Source / Headroom
            54: Control(button_led=LedColor.white()),
            55: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=7, accel=False)),
            # Tone
            57: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            58: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            59: Control(button_led=LedColor.white()),
            # Link
            46: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=7, accel=False)),
            47: Control(button_led=LedColor.green(), button=CtrlButton(steps=4)),
            # Output
            60: Control(button_led=LedColor.white()),
            61: Control(button_led=LedColor.white()),
            62: Control(button_led=LedColor.red()),
            63: Control(encoder_led=LedColor.red()), 
        },

        "UADx dbx 160 Compressor": {
            40: Control(encoder_led=LedColor.yellow()), 
            41: Control(encoder_led=LedColor.yellow()), 
            42: Control(encoder_led=LedColor.yellow()), 
            44: Control(button_led=LedColor.white()),
            45: Control(button_led=LedColor.white()),
            47: Control(encoder_led=LedColor.white()), 
        },

        "UADx Verve Analog Machines": {
            44: Control(encoder_led=LedColor.white()),
            45: Control(encoder_led=LedColor.white()),
            46: Control(encoder_led=LedColor.white()),
        },

        "NFuse": {
            # IO
            88: Control(button_led=LedColor.yellow()),
            92: Control(button_led=LedColor.yellow()),
            93: Control(button_led=LedColor.yellow()),
            94: Control(button_led=LedColor.yellow()),
            95: Control(button_led=LedColor.yellow()),
            # F Levels
            80: Control(encoder_led=LedColor.white()),
            81: Control(encoder_led=LedColor.white()),
            84: Control(encoder_led=LedColor.white()),
            # F Sat
            32: Control(encoder_led=LedColor.green()),
            33: Control(encoder_led=LedColor.green()),
            # F EQ
            36: Control(encoder_led=LedColor.purple()),
            37: Control(encoder_led=LedColor.pink()),
            40: Control(encoder_led=LedColor.purple()),
            41: Control(encoder_led=LedColor.pink()),
            # F Comp 1
            34: Control(encoder_led=LedColor.orange()),
            35: Control(encoder_led=LedColor.orange()),
            38: Control(encoder_led=LedColor.orange()),
            39: Control(encoder_led=LedColor.orange()),
            43: Control(encoder_led=LedColor.orange()),
            # F Comp 2
            42: Control(encoder_led=LedColor.brown()),
            46: Control(encoder_led=LedColor.brown()),
            47: Control(encoder_led=LedColor.brown()),
            # F Stereo
            44: Control(encoder_led=LedColor.cyan()),
            45: Control(encoder_led=LedColor.cyan()),
            # N Levels
            82: Control(encoder_led=LedColor.teal()),
            83: Control(encoder_led=LedColor.teal()),
            86: Control(encoder_led=LedColor.teal()),
            # N Sat
            48: Control(encoder_led=LedColor.teal()),
            49: Control(encoder_led=LedColor.yellow(), button_led=LedColor.pink(), beautify_button=False),
            87: Control(encoder_led=LedColor.grey()),
            # N EQ
            52: Control(encoder_led=LedColor.teal()),
            53: Control(encoder_led=LedColor.yellow()),
            56: Control(encoder_led=LedColor.teal()),
            57: Control(encoder_led=LedColor.yellow()),
            # N Comp 1
            50: Control(encoder_led=LedColor.teal()),
            51: Control(encoder_led=LedColor.yellow()),
            54: Control(encoder_led=LedColor.teal()),
            55: Control(encoder_led=LedColor.yellow()),
            59: Control(encoder_led=LedColor.grey()),
            58: Control(button_led=LedColor.pink()),
            85: Control(encoder_led=LedColor.grey()),
            # N Stereo
            60: Control(encoder_led=LedColor.teal()),
            61: Control(encoder_led=LedColor.yellow()),
        },

        "UADx Empirical Labs Distressor": {
            # Controls
            44: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            45: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            46: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            47: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=211)),
            60: Control(encoder_led=LedColor.white()),
            # Buttons
            40: Control(button_led=LedColor.red()),
            41: Control(button_led=LedColor.white(), button=CtrlButton(steps=8)),
            42: Control(button_led=LedColor.white(), button=CtrlButton(steps=8)),
            43: Control(button_led=LedColor.white(), button=CtrlButton(steps=6)),
        },

        "UADx Manley Variable Mu Compressor": {
            # L side
            44: Control(button_led=LedColor.white()),
            45: Control(button_led=LedColor.white()),
            46: Control(button_led=LedColor.white()),
            42: Control(button_led=LedColor.white()),
            # Mid
            43: Control(button_led=LedColor.yellow()),
            36: Control(button_led=LedColor.pink()),
            54: Control(button_led=LedColor.pink()),
            # R side
            56: Control(button_led=LedColor.white()),
            60: Control(button_led=LedColor.white()),
            61: Control(button_led=LedColor.white()),
            62: Control(button_led=LedColor.white()),
            # Main L + R
            33: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=5, accel=False)),
            34: Control(encoder_led=LedColor.purple()),
            35: Control(encoder_led=LedColor.purple()),
            48: Control(encoder_led=LedColor.purple()),
            49: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=5, accel=False)),
            37: Control(encoder_led=LedColor.purple()),
            38: Control(encoder_led=LedColor.purple()),
            39: Control(encoder_led=LedColor.purple()),
            52: Control(encoder_led=LedColor.purple()),
            53: Control(encoder_led=LedColor.purple()),
            # Headroom
            83: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=9, accel=False)),
        },

        "UADx Manley Massive Passive EQ": {
            # Top
            32: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            33: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            34: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            35: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            48: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            49: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            50: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            51: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            # dB & Shelf bell
            36: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            37: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            38: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            39: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            52: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            53: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            54: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            55: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple()),
            # Bandwidth
            40: Control(encoder_led=LedColor.purple()),
            41: Control(encoder_led=LedColor.purple()),
            42: Control(encoder_led=LedColor.purple()),
            43: Control(encoder_led=LedColor.purple()),
            56: Control(encoder_led=LedColor.purple()),
            57: Control(encoder_led=LedColor.purple()),
            58: Control(encoder_led=LedColor.purple()),
            59: Control(encoder_led=LedColor.purple()),
            # Freq
            44: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            45: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            46: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            47: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            60: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            61: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            62: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            63: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            # Mid panel
            80: Control(button_led=LedColor.blue()),
            81: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=2, accel=False)),
            82: Control(button_led=LedColor.blue()),
            85: Control(button_led=LedColor.white()),
            84: Control(encoder_led=LedColor.purple()),
            86: Control(encoder_led=LedColor.purple()),
            88: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            90: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            92: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            94: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
        },

        "UADx Manley Massive Passive MST": {
            # Top
            32: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            33: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            34: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            35: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            48: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            49: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            50: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            51: Control(button_led=LedColor.pink(), button=CtrlButton(steps=3)),
            # dB & Shelf bell
            36: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            37: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            38: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            39: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            52: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            53: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            54: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            55: Control(button_led=LedColor(r=0.5, g=0.2, b=0.0), encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            # Bandwidth
            40: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            41: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            42: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            43: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            56: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            57: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            58: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            59: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=16)),
            # Freq
            44: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            45: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            46: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            47: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            60: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            61: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            62: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            63: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            # Mid panel
            80: Control(button_led=LedColor.blue()),
            81: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=2, accel=False)),
            82: Control(button_led=LedColor.blue()),
            85: Control(button_led=LedColor.white()),
            84: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            86: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=11, accel=False)),
            88: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            90: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            92: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
            94: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=6, accel=False)),
        },

        "UADx Manley Tube Preamp": {
            36: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=2)),
            40: Control(encoder_led=LedColor.purple()),
            38: Control(encoder_led=LedColor.purple(), encoder=CtrlEncoder(steps=5)),
            42: Control(encoder_led=LedColor.purple()),
            33: Control(button_led=LedColor.blue()),
            37: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            41: Control(button_led=LedColor.white()),
            45: Control(button_led=LedColor.white()),
            81: Control(button_led=LedColor.white()),
        },

        "UADx LA-3A Compressor": {
            36: Control(encoder_led=LedColor.red()),
            39: Control(encoder_led=LedColor.red()),
            41: Control(encoder_led=LedColor.red()),
            42: Control(encoder_led=LedColor.red()),
            44: Control(button_led=LedColor.red(), button=CtrlButton(steps=3)),
            47: Control(button_led=LedColor.red()),
        },

        "UADx Fairchild 670 Compressor": {
            32: Control(button_led=LedColor.orange()),
            33: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            34: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            35: Control(encoder_led=LedColor.red()),
            48: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=6, accel=False)),
            37: Control(encoder_led=LedColor.yellow()),
            52: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=2, accel=False)),
            41: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            42: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            43: Control(encoder_led=LedColor.red()),
            56: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=6, accel=False)),
            45: Control(encoder_led=LedColor.yellow()),
            # Lower panel
            80: Control(encoder_led=LedColor.red()),
            81: Control(encoder_led=LedColor.red()),
            82: Control(button_led=LedColor.white()),
            83: Control(button_led=LedColor.white()),
            84: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            85: Control(encoder_led=LedColor.white()),
            86: Control(encoder_led=LedColor.white()),
            87: Control(encoder_led=LedColor.blue()),
        },

        "UADx Fairchild 660 Compressor": { 
            32: Control(button_led=LedColor.orange()),
            33: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            34: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            35: Control(encoder_led=LedColor.red()),
            48: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=6, accel=False)),
            36: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=7, accel=False)),
            37: Control(encoder_led=LedColor.yellow()),
            40: Control(encoder_led=LedColor.red()),
            41: Control(encoder_led=LedColor.white()),
            42: Control(encoder_led=LedColor.red()),
            56: Control(encoder_led=LedColor.blue()),
        },

        "SSL Native Bus Compressor 2": {
            32: Control(encoder_led=LedColor.blue()),
            33: Control(encoder_led=LedColor.blue()),
            36: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            37: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            40: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=7, accel=False)),
            41: Control(button_led=LedColor.yellow(), button=CtrlButton(invert_intensity=True)),
            44: Control(encoder_led=LedColor.blue()),
            45: Control(encoder_led=LedColor.blue()),
            # Side panel
            42: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)),
            46: Control(button_led=LedColor.yellow()),
            47: Control(button_led=LedColor.yellow()),
        },

        "Maag EQ4": {
            44: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=21, accel=False)),
            45: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            46: Control(encoder_led=LedColor.green(), encoder=CtrlEncoder(steps=21, accel=False)),
            47: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            60: Control(encoder_led=LedColor.orange(), encoder=CtrlEncoder(steps=21, accel=False)),
            61: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=21, accel=False)),
            62: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            63: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=21, accel=False)),
            80: Control(button_led=LedColor.green()),
        },

        "SPL PQ": {
            # L LF
            32: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False, encoder=CtrlEncoder(steps=41)),
            36: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False, encoder=CtrlEncoder(steps=41)),
            40: Control(encoder_led=LedColor.red(), button_led=LedColor.grey(), beautify_button=False, encoder=CtrlEncoder(steps=41)),
        },

        "Pre 1973": {
            # L
            32: Control(encoder_led=LedColor.cyan()),
            36: Control(encoder_led=LedColor.cyan()),
            37: Control(encoder_led=LedColor.cyan()),
            40: Control(encoder_led=LedColor.cyan()),
            41: Control(encoder_led=LedColor.cyan()),
            44: Control(encoder_led=LedColor.blue()),
            80: Control(button_led=LedColor.yellow()),
            81: Control(button_led=LedColor.yellow()),
            # R
            34: Control(encoder_led=LedColor.cyan()),
            38: Control(encoder_led=LedColor.cyan()),
            39: Control(encoder_led=LedColor.cyan()),
            42: Control(encoder_led=LedColor.cyan()),
            43: Control(encoder_led=LedColor.cyan()),
            46: Control(encoder_led=LedColor.blue()),
            82: Control(button_led=LedColor.yellow()),
            83: Control(button_led=LedColor.yellow()),
            # AMP L
            49: Control(encoder_led=LedColor.red()),
            53: Control(encoder_led=LedColor.blue()),
            57: Control(button_led=LedColor.cyan()),
            # AMP R
            50: Control(encoder_led=LedColor.red()),
            54: Control(encoder_led=LedColor.blue()),
            58: Control(button_led=LedColor.cyan()),
            # Link / LR / MS
            61: Control(button_led=LedColor.yellow()),
            62: Control(button_led=LedColor.white()),
            # Bypass
            63: Control(button_led=LedColor.cyan(), button=CtrlButton(invert_intensity=True)),
        },

        "Comp TUBE-STA": {
            40: Control(encoder_led=LedColor.orange()),
            43: Control(encoder_led=LedColor.orange()),
            41: Control(encoder_led=LedColor.white()),
            37: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=3, accel=False)),
            42: Control(button_led=LedColor.red()),
            47: Control(encoder_led=LedColor.white()),
            # Advanced
            80: Control(button_led=LedColor.red()),
            84: Control(encoder_led=LedColor.white()),
            85: Control(encoder_led=LedColor.orange(), encoder=CtrlEncoder(steps=5, accel=False)),
            86: Control(button_led=LedColor.red()),
            87: Control(button_led=LedColor.green()), 
            88: Control(encoder_led=LedColor.white()),
            89: Control(encoder_led=LedColor.white()),
            90: Control(encoder_led=LedColor.white()),
            91: Control(encoder_led=LedColor.white()),
        },

        "Pre TridA": {
            # L Top
            33: Control(button_led=LedColor.yellow()),
            34: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            35: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            38: Control(encoder_led=LedColor.pink()),
            39: Control(encoder_led=LedColor.pink()),
            # L Bottom
            42: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            43: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            45: Control(button_led=LedColor.yellow()),
            46: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            47: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            # R Top
            48: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            49: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            50: Control(button_led=LedColor.yellow()),
            52: Control(encoder_led=LedColor.pink()),
            53: Control(encoder_led=LedColor.pink()),
            # R Bottom
            56: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False)),
            57: Control(encoder_led=LedColor.pink(), encoder=CtrlEncoder(steps=4, accel=False, invert=True)),
            60: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            61: Control(button_led=LedColor(r=0.5, g=0.5, b=0.0), encoder_led=LedColor.pink()),
            62: Control(button_led=LedColor.yellow()),
            # Drive
            81: Control(encoder_led=LedColor.pink()),
            82: Control(encoder_led=LedColor.pink()),
            85: Control(button_led=LedColor.red()),
            86: Control(button_led=LedColor.red()),
            89: Control(button_led=LedColor.green()),
            90: Control(button_led=LedColor.green()),
            93: Control(encoder_led=LedColor.purple()),
            94: Control(encoder_led=LedColor.purple()),
            91: Control(button_led=LedColor.yellow()),
            95: Control(button_led=LedColor.yellow()),
        },

        "Tube-Tech Blue Tone": {
            41: Control(encoder_led=LedColor.blue()),
            42: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=8, accel=False)),
            44: Control(encoder_led=LedColor.blue()),
            45: Control(encoder_led=LedColor.blue()),
            46: Control(encoder_led=LedColor.blue()),
            47: Control(encoder_led=LedColor.blue()),
        },

        "AMEK EQ 200": {
            # Power
            32: Control(button_led=LedColor.blue()),
            # Filters
            36: Control(encoder_led=LedColor.white(), button_led=LedColor.red(), encoder=CtrlEncoder(invert_intensity=True), beautify_button=False),
            40: Control(encoder_led=LedColor.white(), button_led=LedColor.red(), beautify_button=False),
            # Low
            33: Control(button_led=LedColor.red()),
            37: Control(encoder_led=LedColor.red(), button_led=LedColor.grey()),
            41: Control(encoder_led=LedColor.red()),
            45: Control(encoder_led=LedColor.red()),
            # Low M
            34: Control(button_led=LedColor.red()),
            38: Control(encoder_led=LedColor.yellow(), button_led=LedColor.grey()),
            42: Control(encoder_led=LedColor.yellow()),
            46: Control(encoder_led=LedColor.yellow()),
            # Mid
            35: Control(button_led=LedColor.red()),
            39: Control(encoder_led=LedColor.green(), button_led=LedColor.grey()),
            43: Control(encoder_led=LedColor.green()),
            47: Control(encoder_led=LedColor.green()),
            # High M
            48: Control(button_led=LedColor.red()),
            52: Control(encoder_led=LedColor.brown(), button_led=LedColor.grey()),
            56: Control(encoder_led=LedColor.brown()),
            60: Control(encoder_led=LedColor.brown()),
            # High
            49: Control(button_led=LedColor.red()),
            53: Control(encoder_led=LedColor.blue(), button_led=LedColor.grey()),
            57: Control(encoder_led=LedColor.blue()),
            61: Control(encoder_led=LedColor.blue()),
            # Mid panel
            54: Control(encoder_led=LedColor.white(), button_led=LedColor.red()),
            58: Control(button_led=LedColor.red()),
            59: Control(button_led=LedColor.red()),
            62: Control(button_led=LedColor.red()),
            # Levels
            80: Control(encoder_led=LedColor.white()),
            83: Control(encoder_led=LedColor.white()),
            # Mono maker
            81: Control(encoder_led=LedColor.white(), button_led=LedColor.red()), 
            82: Control(encoder_led=LedColor.white(), button_led=LedColor.red()), 
            # THD
            86: Control(encoder_led=LedColor.white(), button_led=LedColor.red()), 
            # TMT
            84: Control(button_led=LedColor.orange()),
            85: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=20, accel=False)),
            # MS/PL
            89: Control(button_led=LedColor.red()),
            90: Control(button_led=LedColor.red()),
        },

        "Black Box Analog Design HG-2MS": {
            # L / Mid
            32: Control(encoder_led=LedColor.white()),
            33: Control(encoder_led=LedColor.white()),
            34: Control(encoder_led=LedColor.white()),
            35: Control(encoder_led=LedColor.white()),
            48: Control(encoder_led=LedColor.white()),
            49: Control(encoder_led=LedColor.white()),
            50: Control(encoder_led=LedColor.white()),
            36: Control(button_led=LedColor.blue()),
            37: Control(button_led=LedColor.blue()),
            38: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)),
            39: Control(button_led=LedColor.blue(), encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=5, accel=False)),
            53: Control(button_led=LedColor.blue()),
            54: Control(button_led=LedColor.blue()),
            # R / Side
            40: Control(encoder_led=LedColor.white()),
            41: Control(encoder_led=LedColor.white()),
            42: Control(encoder_led=LedColor.white()),
            43: Control(encoder_led=LedColor.white()),
            56: Control(encoder_led=LedColor.white()),
            57: Control(encoder_led=LedColor.white()),
            58: Control(encoder_led=LedColor.white()),
            44: Control(button_led=LedColor.blue()),
            45: Control(button_led=LedColor.blue()),
            46: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=5, accel=False)),
            47: Control(button_led=LedColor.blue(), encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=5, accel=False)),
            61: Control(button_led=LedColor.blue()),
            62: Control(button_led=LedColor.blue()),
            # BX strip
            80: Control(button_led=LedColor.red()),
            81: Control(encoder_led=LedColor.orange(), encoder=CtrlEncoder(steps=20, accel=False)),
            82: Control(button_led=LedColor.blue()),
            83: Control(button_led=LedColor.blue()),
            85: Control(encoder_led=LedColor.white()),
            86: Control(button_led=LedColor.blue(), button=CtrlButton(steps=3)),
            88: Control(encoder_led=LedColor.white()),
            89: Control(encoder_led=LedColor.white()),
            90: Control(encoder_led=LedColor.white()),
            91: Control(encoder_led=LedColor.white()),
            # More
            93: Control(button_led=LedColor.red()),
            94: Control(button_led=LedColor.blue()),
        },

        "SSL LMC+": {
            # Filters
            37: Control(encoder_led=LedColor.white()),
            38: Control(button_led=LedColor.yellow()),
            39: Control(encoder_led=LedColor.white()),
            # Amount
            41: Control(button_led=LedColor.yellow()),
            42: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=101)),
            43: Control(button_led=LedColor.yellow()),
            # Routing
            45: Control(button_led=LedColor.yellow()),
            46: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=101)),
            47: Control(button_led=LedColor.yellow()),

            # IO
            80: Control(button_led=LedColor.yellow(), button=CtrlButton(invert_intensity=True)),
            81: Control(encoder_led=LedColor.white()),
            82: Control(encoder_led=LedColor.white()),
            83: Control(button_led=LedColor.yellow()),
        },

        "SSL Blitzer": {
            32: Control(encoder_led=LedColor.white()),
            33: Control(button_led=LedColor.purple()),
            34: Control(button_led=LedColor.red()),
            35: Control(encoder_led=LedColor.purple()),
            48: Control(encoder_led=LedColor.white()),
            37: Control(encoder_led=LedColor.purple()),
            38: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=9, accel=False)),
            39: Control(encoder_led=LedColor.purple()),
            41: Control(encoder_led=LedColor.purple()),
            42: Control(button_led=LedColor.cyan()),
            43: Control(encoder_led=LedColor.purple()),
            44: Control(encoder_led=LedColor.blue()),
            45: Control(encoder_led=LedColor.blue()),
            46: Control(encoder_led=LedColor.blue()),
            47: Control(encoder_led=LedColor.blue()),
            60: Control(button_led=LedColor.purple()),
        },

        "TR5 EQ-73": {
            40: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=5, accel=False)),
            41: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=65)),
            42: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=7, accel=False)),
            43: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=65)),
            56: Control(encoder_led=LedColor.white(), encoder=CtrlEncoder(steps=45)),
            44: Control(button_led=LedColor.yellow()),
            45: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            46: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=22, accel=False)),
            47: Control(encoder_led=LedColor.cyan(), encoder=CtrlEncoder(steps=5, accel=False)),
            57: Control(button_led=LedColor.yellow()),
            61: Control(button_led=LedColor.yellow()),
        },

        "RoyalCompressor": {
            40: Control(encoder_led=LedColor.red()),
            44: Control(button_led=LedColor.orange(), button=CtrlButton(invert_intensity=True)),
            45: Control(encoder_led=LedColor.lightgreen()),
            42: Control(encoder_led=LedColor.lightgreen(), encoder=CtrlEncoder(steps=3, accel=False)),
            46: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=12, accel=False)),
            43: Control(encoder_led=LedColor.lightgreen(), encoder=CtrlEncoder(steps=2, accel=False)),
            47: Control(encoder_led=LedColor.lightgreen()),
            60: Control(encoder_led=LedColor.lightgreen()),
            57: Control(encoder_led=LedColor.lightgreen()),
        },

        "Chandler Limited Zener Limiter": {
            # L
            32: Control(button_led=LedColor.white()),
            36: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            40: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            41: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)),
            42: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            43: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            39: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=11, accel=False)),
            35: Control(button_led=LedColor.white()),
            # R
            48: Control(button_led=LedColor.white()),
            52: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            56: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            57: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=3, accel=False)),
            58: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            59: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            55: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=11, accel=False)),
            51: Control(button_led=LedColor.white()),
            # M
            81: Control(button_led=LedColor.cyan()),
            82: Control(button_led=LedColor.cyan()),
            85: Control(button_led=LedColor.cyan()),
            86: Control(button_led=LedColor.cyan()),
            89: Control(button_led=LedColor.white()),
            90: Control(encoder_led=LedColor.white()),
        },

        "Chandler Limited Curve Bender": {
            # L
            32: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=8, accel=False)),
            33: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            34: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            35: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=9, accel=False)),
            36: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            37: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            38: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            39: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            40: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            41: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            42: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            43: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            # R
            48: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=8, accel=False)),
            49: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            50: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=9, accel=False)),
            51: Control(encoder_led=LedColor.red(), button_led=LedColor.yellow(), encoder=CtrlEncoder(steps=9, accel=False)),
            52: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            53: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            54: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            55: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=21, accel=False)),
            56: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            57: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            58: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            59: Control(button_led=LedColor.yellow(), button=CtrlButton(steps=3)),
            # Filter
            80: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            84: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            83: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            87: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            # Mid
            81: Control(button_led=LedColor.cyan()),
            82: Control(button_led=LedColor.cyan()),
            85: Control(button_led=LedColor.cyan()),
            86: Control(button_led=LedColor.cyan()),
            89: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
            90: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=21, accel=False)),
        },

        "Complexx": {
            # L
            80: Control(encoder_led=LedColor.purple()),
            84: Control(encoder_led=LedColor.white()),
            32: Control(encoder_led=LedColor.white()),
            33: Control(encoder_led=LedColor.teal()),
            34: Control(encoder_led=LedColor.yellow()),
            35: Control(encoder_led=LedColor.red()),
            36: Control(button_led=LedColor.orange(), button=CtrlButton(steps=3)),
            37: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            38: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            39: Control(button_led=LedColor.teal(), button=CtrlButton(steps=3)),
            40: Control(encoder_led=LedColor.white()),
            41: Control(encoder_led=LedColor.teal()),
            42: Control(encoder_led=LedColor.yellow()),
            43: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            # R
            83: Control(encoder_led=LedColor.purple()),
            87: Control(encoder_led=LedColor.white()),
            51: Control(encoder_led=LedColor.white()),
            50: Control(encoder_led=LedColor.teal()),
            49: Control(encoder_led=LedColor.yellow()),
            48: Control(encoder_led=LedColor.red()),
            55: Control(button_led=LedColor.orange(), button=CtrlButton(steps=3)),
            54: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            53: Control(button_led=LedColor.white(), button=CtrlButton(steps=3)),
            52: Control(button_led=LedColor.teal(), button=CtrlButton(steps=3)),
            59: Control(encoder_led=LedColor.white()),
            58: Control(encoder_led=LedColor.teal()),
            57: Control(encoder_led=LedColor.yellow()),
            56: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=6, accel=False)),
            # M
            85: Control(encoder_led=LedColor.white()),
            86: Control(encoder_led=LedColor.white()),
        },

        "ADC1 Compressor": {
            # L
            32: Control(encoder_led=LedColor.red()),
            33: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=4, accel=False)),
            34: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            35: Control(encoder_led=LedColor.white()),
            48: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            49: Control(encoder_led=LedColor.teal()),
            # R
            36: Control(encoder_led=LedColor.red()),
            37: Control(encoder_led=LedColor.teal(), encoder=CtrlEncoder(steps=4, accel=False)),
            38: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=6, accel=False)),
            39: Control(encoder_led=LedColor.white()),
            52: Control(encoder_led=LedColor.yellow(), encoder=CtrlEncoder(steps=11, accel=False)),
            53: Control(encoder_led=LedColor.teal()),
        },

        ### Synths

        "Acid V": {
            # Top row
            32: Control(button_led=LedColor.white()),
            33: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=25, accel=False)),
            34: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            35: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            48: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            49: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            50: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=32, accel=False)),
            # Mid row
            36: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=3, accel=False, invert=True)),
            37: Control(encoder_led=LedColor.lime(), encoder=CtrlEncoder(steps=3, accel=False, invert=True)),
            38: Control(encoder_led=LedColor.lime()),
            39: Control(encoder_led=LedColor.lime()),
            52: Control(encoder_led=LedColor.lime()),
            53: Control(encoder_led=LedColor.lime()),
            54: Control(encoder_led=LedColor.red(), encoder=CtrlEncoder(steps=14, accel=False)),
            55: Control(encoder_led=LedColor.lime()),
            # Advanced
            45: Control(encoder_led=LedColor.green()),
            46: Control(encoder_led=LedColor.green()),
            47: Control(encoder_led=LedColor.green()),
            60: Control(encoder_led=LedColor.green()),
            61: Control(encoder_led=LedColor.green()),
            62: Control(encoder_led=LedColor.green()),
            63: Control(encoder_led=LedColor.green()),
        },
    }
}