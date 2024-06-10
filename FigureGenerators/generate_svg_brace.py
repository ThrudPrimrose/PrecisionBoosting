import drawsvg as dw

# Create a Drawing object
d = dw.Drawing(700, 220)

def brace(d, x_pos, y_pos, h, w, dd):
    pnt_1 = (x_pos, y_pos+h)
    pnt_2 = (x_pos+w, y_pos)

    trans = f'translate(0,0)'
    p = dw.Path(stroke='black', fill='none',
                stroke_width=2, transform=trans,
                stroke_linejoin='round')
    ctl_1 = (x_pos+dd, y_pos)
    ctl_2 = (x_pos+w-dd, y_pos+h)
    p.M(*pnt_1)
    p.C(*ctl_1, *ctl_2, *pnt_2)
    d.append(p)

    pnt_1 = (x_pos+w, y_pos)
    pnt_2 = (x_pos+w+w, y_pos+h)

    trans = f'translate(0,0)'
    p = dw.Path(stroke='black', fill='none',
                stroke_width=2, transform=trans,
                stroke_linejoin='round')
    ctl_1 = (x_pos+w+dd, y_pos+h)
    ctl_2 = (x_pos+w+w-dd, y_pos)
    p.M(*pnt_1)
    p.C(*ctl_1, *ctl_2, *pnt_2)
    d.append(p)

brace(d, 50, 30, 20, 50, 10)
brace(d, 50, 60, 20, 50, 10)
brace(d, 50, 90, 20, 100, 10)
brace(d, 50, 120, 20, 110, 10)
brace(d, 50, 150, 20, 60, 10)
brace(d, 50, 180, 20, 10, 5)
# Save the drawing
d.save_svg('curly_brace.svg')
