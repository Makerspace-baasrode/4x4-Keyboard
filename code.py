import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.rgb import RGB
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.handlers.sequences import send_string, simple_key_sequence  # https://kmkfw.io/sequences/
from kmk.extensions.international import International

# Rotary
# Macropad van 4x4 Gray

keyboard = KMKKeyboard()

keyboard.col_pins = (board.D0, board.D1, board.D2, board.D3)
keyboard.row_pins = (board.D10, board.D9, board.D8, board.D7)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.extensions.append(International())

# LEDs + colour on layer change
# Based on https://kmkfw.io/layers/#active-layer-indication-with-rgb

class LayerRGB(RGB):
    def on_layer_change(self, layer):
        print(f"Changing to layer {layer}")
        if layer == 0:
            self.set_hsv_fill(0, self.sat_default, self.val_default)   # red
        elif layer == 1:
            self.set_hsv_fill(170, self.sat_default, self.val_default) # blue
        elif layer == 2:
            self.set_hsv_fill(43, self.sat_default, self.val_default)  # yellow
        RGB.show()

RGB = LayerRGB(pixel_pin=board.D6, # GPIO pin of the status LED, or background RGB light
        num_pixels=9,                # one if status LED, more if background RGB light
        rgb_order=(1, 0, 2),         # RGB order may differ depending on the hardware
        hue_default=100,               # in range 0-255: 0/255-red, 85-green, 170-blue
        sat_default=255,
        val_default=10,
        )

keyboard.extensions.append(RGB)

class RGBLayers(Layers):
    def activate_layer(self, keyboard, layer, idx=None):
        super().activate_layer(keyboard, layer, idx)
        RGB.on_layer_change(layer)
        RGB.show()

    def deactivate_layer(self, keyboard, layer):
        super().deactivate_layer(keyboard, layer)
        RGB.on_layer_change(keyboard.active_layers[0])
        RGB.show()

keyboard.modules.append(RGBLayers())

# Rotary Encoder
# https://github.com/KMKfw/kmk_firmware/blob/master/docs/en/encoder.md

keyboard.extensions.append(MediaKeys())

encoder_handler = EncoderHandler()
keyboard.modules.append(encoder_handler)
encoder_handler.pins = (
    (board.D4, board.D5, None,), # encoder #1 
    )

encoder_handler.map = [((KC.VOLU, KC.VOLD, None),), 
                       ((KC.VOLD, KC.VOLU, None),),
                       ((KC.VOLD, KC.VOLU, None),),
                      ]

# Mapping from characters to keycodes
char_to_keycode = {
    'a': KC.Q, 'A': KC.LSFT(KC.Q),
    'b': KC.B, 'B': KC.LSFT(KC.B),
    'c': KC.C, 'C': KC.LSFT(KC.C), 
    'd': KC.D, 'D': KC.LSFT(KC.D),
    'e': KC.E, 'E': KC.LSFT(KC.E),
    'f': KC.F, 'F': KC.LSFT(KC.F),
    'g': KC.G, 'G': KC.LSFT(KC.G),
    'h': KC.H, 'H': KC.LSFT(KC.H),
    'i': KC.I, 'I': KC.LSFT(KC.I),
    'j': KC.J, 'J': KC.LSFT(KC.J),
    'k': KC.K, 'K': KC.LSFT(KC.K),
    'l': KC.L, 'L': KC.LSFT(KC.L), 
    'm': KC.SCLN, 'M': KC.LSFT(KC.SCLN),
    'n': KC.N, 'N': KC.LSFT(KC.N),
    'o': KC.O, 'O': KC.LSFT(KC.O),
    'p': KC.P, 'P': KC.LSFT(KC.P),
    'q': KC.A, 'Q': KC.LSFT(KC.A),
    'r': KC.R, 'R': KC.LSFT(KC.R),
    's': KC.S, 'S': KC.LSFT(KC.S),
    't': KC.T, 'T': KC.LSFT(KC.T),
    'u': KC.U, 'U': KC.LSFT(KC.U),
    'v': KC.V, 'V': KC.LSFT(KC.V),
    'w': KC.Z, 'W': KC.LSFT(KC.Z),
    'x': KC.X, 'X': KC.LSFT(KC.X),
    'y': KC.Y, 'Y': KC.LSFT(KC.Y),
    'z': KC.W, 'Z': KC.LSFT(KC.W),
    '1': KC.LSFT(KC.N1),
    '2': KC.LSFT(KC.N2),
    '3': KC.LSFT(KC.N3),
    '4': KC.LSFT(KC.N4),
    '5': KC.LSFT(KC.N5),
    '6': KC.LSFT(KC.N6),
    '7': KC.LSFT(KC.N7),
    '8': KC.LSFT(KC.N8),
    '9': KC.LSFT(KC.N9),
    '0': KC.LSFT(KC.N0),
    'ç': KC.N9,
    'à': KC.N0,
    'è': KC.N7,
    'ù': KC.QUOT,
    '§': KC.N6,
    '²': KC.GRAVE,
    '³': KC.LSFT(KC.GRAVE),
    '°': KC.LSFT(KC.MINS),
    '¨': KC.LSFT(KC.LBRC),
    'µ': KC.BSLASH,
    ' ': KC.SPC,
    '.': KC.LSFT(KC.COMM),     
    ',': KC.M,
    ';': KC.COMM,
    ':': KC.DOT,
    '!': KC.N8,
    '@': KC.RALT (KC.N2),
    '#': KC.RALT(KC.N3),
    '$': KC.RBRC,
    '€': KC.RALT(KC.E),
    '£': KC.LSFT(KC.BSLS),
    '%': KC.LSFT(KC.QUOTE),
    '^': KC.LBRC,
    '&': KC.N1, 
    '*': KC.LSFT(KC.RBRC),
    '(': KC.N5,
    ')': KC.MINS,
    '-': KC.EQUAL,
    '_': KC.LSFT(KC.EQL),
    '=': KC.SLSH,
    '+': KC.QUESTION,
    '[': KC.RALT(KC.N5),
    ']': KC.RALT(KC.RBRACKET), 
    '{': KC.RALT(KC.N9),
    '}': KC.RALT(KC.N0),
    '|': KC.RALT(KC.N1),
    "'": KC.N4,
    '"': KC.N3,
    '/': KC.LSFT(KC.KP_SLASH),
    '?': KC.LSFT(KC.M),
    '`': KC.RALT(KC.PIPE),
    '´': KC.RALT(KC.DOUBLE_QUOTE),
    '~': KC.RALT(KC.SLSH),
    '<': KC.NONUS_BSLASH,
    '>': KC.LSFT(KC.NONUS_BSLASH),
    '\\': KC.RALT(KC.NONUS_BSLASH),
}

# Function to convert text to keycode sequence
def text_to_keycode_sequence(text):
    return [char_to_keycode[char] for char in text if char in char_to_keycode]

# Function to send converted text
def send_converted_string(text):    
    keycode_sequence = text_to_keycode_sequence(text)
    return simple_key_sequence(keycode_sequence)

# Define a custom key to send the string "Azerty or Qwerty what will it be?"
#WOW = send_converted_string("Azerty or Qwerty what will it be?")
WOW = send_converted_string(" !#$%&'()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ^_abcdefghijklmnopqrstuvwxyzàçèù§²³°¨€£µ{|}[]\"`´~\\<>")
LIJN1 = send_converted_string("&é\"'(§è!çà)-")
LIJN2 = send_converted_string("azertyuiop^$")
LIJN3 = send_converted_string("qsdfghjklmùµ")
LIJN4 = send_converted_string("<wxcvbn,;:=")
LIJN5 = send_converted_string("1234567890°_")
LIJN6 = send_converted_string("AZERTYUIOP¨*")
LIJN7 = send_converted_string("QSDFGHJKLM%£")
LIJN8 = send_converted_string(">WXCVBN?./+")

NORMAL = simple_key_sequence(
        (
            KC.A,
            KC.B,
            KC.C,
            KC.D,
            KC.E,
            KC.F,
            KC.G,
            KC.H,
            KC.I,
            KC.J,
            KC.K,
            KC.L,
            KC.M,
            KC.N,
            KC.O,
            KC.P,
            KC.Q,
            KC.R,
            KC.S,
            KC.T,
            KC.U,
            KC.V,
            KC.W,
            KC.X,
            KC.Y,
            KC.Z,
            KC.N1,
            KC.N2,
            KC.N3,
            KC.N4,
            KC.N5,
            KC.N6,
            KC.N7,
            KC.N8,
            KC.N9,
            KC.N0,
            KC.MINUS,
            KC.EQUAL,
            KC.LBRACKET,
            KC.RBRACKET,
            KC.BSLASH,
            KC.SCOLON,
            KC.QUOTE,
            KC.GRAVE,
            KC.COMMA,
            KC.DOT,
            KC.SLASH,
            KC.TILDE,
            KC.EXCLAIM,
            KC.AT,
            KC.HASH,
            KC.DOLLAR,
            KC.PERCENT,
            KC.CIRCUMFLEX,
            KC.AMPERSAND,
            KC.ASTERISK,
            KC.LEFT_PAREN,
            KC.RIGHT_PAREN,
            KC.UNDERSCORE,
            KC.PLUS,
            KC.LEFT_CURLY_BRACE,
            KC.RIGHT_CURLY_BRACE,
            KC.PIPE,
            KC.COLON,
            KC.DOUBLE_QUOTE,
            KC.LEFT_ANGLE_BRACKET,
            KC.RIGHT_ANGLE_BRACKET,
            KC.QUESTION,
            KC.NONUS_HASH,
            KC.NONUS_BSLASH,
            KC.INT1,
            KC.INT2,
            KC.INT3,
            KC.INT4,
            KC.INT5,
            KC.INT6,
            KC.INT7,
            KC.INT8,
            KC.INT9,
            KC.LANG1,
            KC.LANG2,
            KC.LANG3,
            KC.LANG4,
            KC.LANG5,
            KC.LANG6,
            KC.LANG7,
            KC.LANG8,
            KC.LANG9
        )
        )

LEFTSHIFT = simple_key_sequence(
        (
            KC.LSFT(KC.A),
            KC.LSFT(KC.B),
            KC.LSFT(KC.C),
            KC.LSFT(KC.D),
            KC.LSFT(KC.E),
            KC.LSFT(KC.F),
            KC.LSFT(KC.G),
            KC.LSFT(KC.H),
            KC.LSFT(KC.I),
            KC.LSFT(KC.J),
            KC.LSFT(KC.K),
            KC.LSFT(KC.L),
            KC.LSFT(KC.M),
            KC.LSFT(KC.N),
            KC.LSFT(KC.O),
            KC.LSFT(KC.P),
            KC.LSFT(KC.Q),
            KC.LSFT(KC.R),
            KC.LSFT(KC.S),
            KC.LSFT(KC.T),
            KC.LSFT(KC.U),
            KC.LSFT(KC.V),
            KC.LSFT(KC.W),
            KC.LSFT(KC.X),
            KC.LSFT(KC.Y),
            KC.LSFT(KC.Z),
            KC.LSFT(KC.N1),
            KC.LSFT(KC.N2),
            KC.LSFT(KC.N3),
            KC.LSFT(KC.N4),
            KC.LSFT(KC.N5),
            KC.LSFT(KC.N6),
            KC.LSFT(KC.N7),
            KC.LSFT(KC.N8),
            KC.LSFT(KC.N9),
            KC.LSFT(KC.N0),
            KC.LSFT(KC.MINUS),
            KC.LSFT(KC.EQUAL),
            KC.LSFT(KC.LBRACKET),
            KC.LSFT(KC.RBRACKET),
            KC.LSFT(KC.BSLASH),
            KC.LSFT(KC.SCOLON),
            KC.LSFT(KC.QUOTE),
            KC.LSFT(KC.GRAVE),
            KC.LSFT(KC.COMMA),
            KC.LSFT(KC.DOT),
            KC.LSFT(KC.SLASH),
            KC.LSFT(KC.TILDE),
            KC.LSFT(KC.EXCLAIM),
            KC.LSFT(KC.AT),
            KC.LSFT(KC.HASH),
            KC.LSFT(KC.DOLLAR),
            KC.LSFT(KC.PERCENT),
            KC.LSFT(KC.CIRCUMFLEX),
            KC.LSFT(KC.AMPERSAND),
            KC.LSFT(KC.ASTERISK),
            KC.LSFT(KC.LEFT_PAREN),
            KC.LSFT(KC.RIGHT_PAREN),
            KC.LSFT(KC.UNDERSCORE),
            KC.LSFT(KC.PLUS),
            KC.LSFT(KC.LEFT_CURLY_BRACE),
            KC.LSFT(KC.RIGHT_CURLY_BRACE),
            KC.LSFT(KC.PIPE),
            KC.LSFT(KC.COLON),
            KC.LSFT(KC.DOUBLE_QUOTE),
            KC.LSFT(KC.LEFT_ANGLE_BRACKET),
            KC.LSFT(KC.RIGHT_ANGLE_BRACKET),
            KC.LSFT(KC.QUESTION),
            KC.LSFT(KC.NONUS_HASH),
            KC.LSFT(KC.NONUS_BSLASH),
            KC.LSFT(KC.INT1),
            KC.LSFT(KC.INT2),
            KC.LSFT(KC.INT3),
            KC.LSFT(KC.INT4),
            KC.LSFT(KC.INT5),
            KC.LSFT(KC.INT6),
            KC.LSFT(KC.INT7),
            KC.LSFT(KC.INT8),
            KC.LSFT(KC.INT9),
            KC.LSFT(KC.LANG1),
            KC.LSFT(KC.LANG2),
            KC.LSFT(KC.LANG3),
            KC.LSFT(KC.LANG4),
            KC.LSFT(KC.LANG5),
            KC.LSFT(KC.LANG6),
            KC.LSFT(KC.LANG7),
            KC.LSFT(KC.LANG8),
            KC.LSFT(KC.LANG9)
        )
        )

RIGHTALT = simple_key_sequence(
        (
            KC.RALT(KC.A),
            KC.RALT(KC.B),
            KC.RALT(KC.C),
            KC.RALT(KC.D),
            KC.RALT(KC.E),
            KC.RALT(KC.F),
            KC.RALT(KC.G),
            KC.RALT(KC.H),
            KC.RALT(KC.I),
            KC.RALT(KC.J),
            KC.RALT(KC.K),
            KC.RALT(KC.L),
            KC.RALT(KC.M),
            KC.RALT(KC.N),
            KC.RALT(KC.O),
            KC.RALT(KC.P),
            KC.RALT(KC.Q),
            KC.RALT(KC.R),
            KC.RALT(KC.S),
            KC.RALT(KC.T),
            KC.RALT(KC.U),
            KC.RALT(KC.V),
            KC.RALT(KC.W),
            KC.RALT(KC.X),
            KC.RALT(KC.Y),
            KC.RALT(KC.Z),
            
            KC.RALT(KC.N1),
            KC.RALT(KC.N2),
            KC.RALT(KC.N3),
            KC.RALT(KC.N4),
            KC.RALT(KC.N5),
            KC.RALT(KC.N6),
            KC.RALT(KC.N7),
            KC.RALT(KC.N8),
            KC.RALT(KC.N9),
            KC.RALT(KC.N0),
            KC.RALT(KC.MINUS),
            KC.RALT(KC.EQUAL),
            KC.RALT(KC.LBRACKET),
            KC.RALT(KC.RBRACKET),
            KC.RALT(KC.BSLASH),
            KC.RALT(KC.SCOLON),
            KC.RALT(KC.QUOTE),
            KC.RALT(KC.GRAVE),
            KC.RALT(KC.COMMA),
            KC.RALT(KC.DOT),
            KC.RALT(KC.SLASH),
            KC.RALT(KC.TILDE),
            KC.RALT(KC.EXCLAIM),
            KC.RALT(KC.AT),
            KC.RALT(KC.HASH),
            KC.RALT(KC.DOLLAR),
            KC.RALT(KC.PERCENT),
            KC.RALT(KC.CIRCUMFLEX),
            KC.RALT(KC.AMPERSAND),
            KC.RALT(KC.ASTERISK),
            KC.RALT(KC.LEFT_PAREN),
            KC.RALT(KC.RIGHT_PAREN),
            KC.RALT(KC.UNDERSCORE),
            KC.RALT(KC.PLUS),
            KC.RALT(KC.LEFT_CURLY_BRACE),
            KC.RALT(KC.RIGHT_CURLY_BRACE),
            KC.RALT(KC.PIPE),
            KC.RALT(KC.COLON),
            KC.RALT(KC.DOUBLE_QUOTE),
            KC.RALT(KC.LEFT_ANGLE_BRACKET),
            KC.RALT(KC.RIGHT_ANGLE_BRACKET),
            KC.RALT(KC.QUESTION),
            KC.RALT(KC.NONUS_HASH),
            KC.RALT(KC.NONUS_BSLASH),
            KC.RALT(KC.INT1),
            KC.RALT(KC.INT2),
            KC.RALT(KC.INT3),
            KC.RALT(KC.INT4),
            KC.RALT(KC.INT5),
            KC.RALT(KC.INT6),
            KC.RALT(KC.INT7),
            KC.RALT(KC.INT8),
            KC.RALT(KC.INT9),
            KC.RALT(KC.LANG1),
            KC.RALT(KC.LANG2),
            KC.RALT(KC.LANG3),
            KC.RALT(KC.LANG4),
            KC.RALT(KC.LANG5),
            KC.RALT(KC.LANG6),
            KC.RALT(KC.LANG7),
            KC.RALT(KC.LANG8),
            KC.RALT(KC.LANG9)
        )
        )
        
# https://kmkfw.io/keycodes/

keyboard.keymap = [
    # Base layer
    [
        KC.TO(0), KC.TO(1), KC.TO(2), KC.MUTE,
        WOW, NORMAL, LEFTSHIFT,  RIGHTALT, 
        KC.KP_5,  KC.KP_6,  KC.KP_7,  KC.KP_8,
        KC.KP_9,  KC.KP_0,  KC.KP_MINUS,  KC.KP_PLUS,
    ],

    # Azerty Layer test
    [
        KC.TO(0), KC.TO(1), KC.TO(2), KC.MUTE,
        WOW, LIJN1, LIJN2, LIJN3,
        LIJN4, LIJN5, LIJN6, LIJN7,
        LIJN8, KC.P, KC.Q, KC.S,
    ],

    # Symbol Layer
    [
        KC.TO(0), KC.TO(1), KC.TO(2), KC.MUTE,
        KC.N1, KC.N2, KC.N3, KC.N4,
        KC.N5, KC.N6, KC.N7, KC.N8,
        KC.N9, KC.N0, KC.DOT, KC.GRAVE,
    ]
]

if __name__ == '__main__':
    keyboard.go()
