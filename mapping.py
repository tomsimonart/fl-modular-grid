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


@dataclass
class CtrlEncoder():
    steps: int = 256

@dataclass
class CtrlButton():
    steps: int = 2

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
            59: Control(button_led=LedColor.white()),
            63: Control(encoder_led=LedColor.blue()),
        },

        "Tube-Tech CL 1B mk II": {
            # Controls
            40: Control(encoder_led=LedColor.blue()),
            41: Control(encoder_led=LedColor.blue()),
            42: Control(encoder_led=LedColor.blue()),
            43: Control(encoder_led=LedColor.blue(), encoder=CtrlEncoder(steps=2)),
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

        "UADx SSL E Channel Strip": {
            # Line & Mic
            32: Control(button_led=LedColor.white(), encoder_led=LedColor.white(), beautify_button=False),
            33: Control(button_led=LedColor.white()),
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
        "Chandler Limited Germanium Comp": {
            # Left / Mid
            32: Control(button_led=LedColor(1, 1, 0.5)),
            33: Control(encoder_led=LedColor.yellow()),
            34: Control(encoder_led=LedColor.yellow()),
            35: Control(encoder_led=LedColor.yellow()),
            48: Control(encoder_led=LedColor.yellow()),
            49: Control(encoder_led=LedColor.yellow()),
            50: Control(encoder_led=LedColor.white()),
            51: Control(encoder_led=LedColor.white()),
            54: Control(encoder_led=LedColor.yellow()),
            55: Control(encoder_led=LedColor.yellow()),
            # Right / Side
            40: Control(button_led=LedColor(1, 1, 0.5)),
            41: Control(encoder_led=LedColor.yellow()),
            42: Control(encoder_led=LedColor.yellow()),
            43: Control(encoder_led=LedColor.yellow()),
            56: Control(encoder_led=LedColor.yellow()),
            57: Control(encoder_led=LedColor.yellow()),
            58: Control(encoder_led=LedColor.white()),
            59: Control(encoder_led=LedColor.white()),
            62: Control(encoder_led=LedColor.yellow()),
            63: Control(encoder_led=LedColor.yellow()), 
            # Side panel
            44: Control(button_led=LedColor.white()),
            45: Control(encoder_led=LedColor.white()),
            46: Control(button_led=LedColor.cyan()),
            47: Control(button_led=LedColor.cyan()),
            60: Control(button_led=LedColor.cyan()),
            61: Control(button_led=LedColor.cyan()),
            83: Control(encoder_led=LedColor.yellow()),
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
            44: Control(encoder_led=LedColor.white()),
            45: Control(encoder_led=LedColor.white()),
            46: Control(encoder_led=LedColor.white()),
            47: Control(encoder_led=LedColor.white()),
            60: Control(encoder_led=LedColor.white()),
            # Buttons
            40: Control(button_led=LedColor.red()),
            41: Control(button_led=LedColor.white(), button=CtrlButton(steps=8)),
            42: Control(button_led=LedColor.white(), button=CtrlButton(steps=8)),
            43: Control(button_led=LedColor.white(), button=CtrlButton(steps=6)),
        }
    }
}