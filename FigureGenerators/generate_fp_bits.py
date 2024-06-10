import drawsvg as draw
import struct
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import numpy as np
import random

def float_to_bin(num):
    """Convert a float into its 32-bit binary representation."""
    packed = struct.pack('!f', num)
    bits = ''.join(f'{byte:08b}' for byte in packed)
    return bits

def double_to_bin(num):
    packed = struct.pack('!d', num)
    bits = ''.join(f'{byte:08b}' for byte in packed)
    return bits

def brace(d, x_pos, y_pos, h, w, dd, color):
    pnt_1 = (x_pos, y_pos+h)
    pnt_2 = (x_pos+w, y_pos)

    trans = f'translate(0,0)'
    p = draw.Path(stroke=color, fill='none',
                stroke_width=1, transform=trans,
                stroke_linejoin='round')
    ctl_1 = (x_pos+dd, y_pos)
    ctl_2 = (x_pos+w-dd, y_pos+h)
    p.M(*pnt_1)
    p.C(*ctl_1, *ctl_2, *pnt_2)
    d.append(p)

    pnt_1 = (x_pos+w, y_pos)
    pnt_2 = (x_pos+w+w, y_pos+h)

    trans = f'translate(0,0)'
    p = draw.Path(stroke=color, fill='none',
                stroke_width=1, transform=trans,
                stroke_linejoin='round')
    ctl_1 = (x_pos+w+dd, y_pos+h)
    ctl_2 = (x_pos+w+w-dd, y_pos)
    p.M(*pnt_1)
    p.C(*ctl_1, *ctl_2, *pnt_2)
    d.append(p)


def draw_fp_bits(num, filename='float_bits.svg', font_family='monospace',
                     num_bits=64, num_sign_bits = 1,
                     num_exp_bits = 11, num_fraction_bits = 52, bits = None,
                     braces = True):
    if bits == None:
        if num_bits == 16:
            bits = format(np.frombuffer(np.float16(num).tobytes(), dtype=np.uint16)[0], '016b')
        elif num_bits == 32:
            bits = format(np.frombuffer(np.float32(num).tobytes(), dtype=np.uint32)[0], '032b')
        elif num_bits == 64:
            bits = format(np.frombuffer(np.float64(num).tobytes(), dtype=np.uint64)[0], '064b')
        else:
            bits = ''.join(random.choice('01') for _ in range(num_bits))
    #float_to_bin(num) if num_bits == 32 else double_to_bin(num)

    # Define bit sizes and total sizes
    bit_width = 20
    bit_height = 30
    total_width = bit_width * (num_bits+1)
    total_height = 90
    if not braces:
        total_height = 60
    y_pos = -5
    if not braces:
        y_pos = -15

    # Create the SVG canvas
    d = draw.Drawing(total_width, total_height, origin='center')

    # Center alignment calculations
    center_x = -total_width / 2
    x_start = center_x + 10

    light_green =  "#c2f0c2"
    green = "#33cc33"
    light_turquoise = " #b3e6ff"
    turquoise = "#00aaff"
    light_red = "#ffd6cc"
    red = "#ff0000"

    # Labels and curly brackets
    if braces:
        d.append(draw.Text('Sign', 12, x_start + bit_width / 2, -total_height / 2 + 15,
                       fill=turquoise, text_anchor="middle", font_family=font_family))
        d.append(draw.Text('Exponent', 12, x_start + ((2*num_sign_bits+num_exp_bits)*bit_width/2), -total_height / 2 + 15,
                       fill=green, text_anchor="middle", font_family=font_family))
        d.append(draw.Text('Fraction', 12, x_start + ((2*(num_sign_bits+num_exp_bits)+num_fraction_bits)*bit_width/2), -total_height / 2 + 15,
                       fill=red, text_anchor="middle", font_family=font_family))

    # Draw the sign bit
    x_pos = x_start
    d.append(draw.Rectangle(x_pos, y_pos, bit_width, bit_height, fill=light_turquoise, stroke='black'))
    d.append(draw.Text(bits[0], 12, x_pos + (bit_width/2), y_pos + 20, fill='black', text_anchor="middle", font_family=font_family))
    if braces:
        brace(d, x_pos + 1, y_pos - 12, 10, (bit_width/2) - 1 , 2, turquoise)  # lighter shade background

    # Draw the exponent bits
    x_pos += bit_width
    if braces:
        brace(d, x_pos + 1, y_pos - 12, 10, (num_exp_bits*bit_width/2) - 1 , 0.00001, green)  # lighter shade background
    for bit in bits[1:(num_exp_bits+num_sign_bits)]:
        d.append(draw.Rectangle(x_pos, y_pos, bit_width, bit_height, fill=light_green, stroke='black'))  # lighter shade background
        d.append(draw.Text(bit, 12, x_pos + (bit_width/2), y_pos + 20, fill='black', text_anchor="middle", font_family=font_family))
        x_pos += bit_width
    if braces:
        brace(d, x_pos + 1, y_pos - 12, 10, (num_fraction_bits*bit_width/2) - 1 , 0.000001, red)  # lighter shade background

    # Draw the mantissa bits
    for bit in bits[(num_exp_bits+num_sign_bits):]:
        d.append(draw.Rectangle(x_pos, y_pos, bit_width, bit_height, fill=light_red, stroke='black'))  # lighter shade background
        d.append(draw.Text(bit, 12, x_pos + (bit_width/2), y_pos + 20, fill='black', text_anchor="middle", font_family=font_family))
        x_pos += bit_width

    # Save the drawing
    d.save_svg(filename)


bits = format(np.frombuffer(np.float64(3.14).tobytes(), dtype=np.uint64)[0], '064b')
print(bits)
print(bits[0] , "|", bits[1:12], "|", bits[12:])
print(bits[12+23:])
print(len(bits[12+23:]))
print(1024 - 1023 + 127 - 23)
nexp = 1024 - 1023 + 127 - 23 - 1
nexpstr = format(nexp, '08b')
print(nexpstr)
f = "fp_2"
bbits = bits[0] + nexpstr + bits[12+23+1:12+23+23+1]

draw_fp_bits(3.14, f + ".svg", "monospace", 32, 1, 8, 23, bbits, False)
drawing = svg2rlg(f + ".svg")
renderPDF.drawToFile(drawing, f + ".pdf")

f = "brainfloat_bits_f"
bbits = bits[0] + bits[1:9] + bits[9:9+7]
draw_fp_bits(3.14, f + ".svg", "monospace", 16, 1, 8, 7, bbits, False)
drawing = svg2rlg(f + ".svg")
renderPDF.drawToFile(drawing, f + ".pdf")

f = "half_bits"
# Example usage
draw_fp_bits(3.14, f + ".svg", "monospace", 16, 1, 5, 10)
drawing = svg2rlg(f + ".svg")
renderPDF.drawToFile(drawing, f + ".pdf")

f = "float_bits"
# Example usage
draw_fp_bits(3.14, f + ".svg", "monospace", 32, 1, 8, 23)
drawing = svg2rlg(f + ".svg")
renderPDF.drawToFile(drawing, f + ".pdf")

d = "double_bits"
# Example usage
draw_fp_bits(3.14, d + ".svg", "monospace", 64, 1, 11, 52)
drawing = svg2rlg(d + ".svg")
renderPDF.drawToFile(drawing, d + ".pdf")

d = "quadruple_bits"
# Example usage
draw_fp_bits(3.14, d + ".svg", "monospace", 128, 1, 15, 112)
drawing = svg2rlg(d + ".svg")
renderPDF.drawToFile(drawing, d + ".pdf")
