import colorsys

def nearest_color(rgb_value):
    h, s, v = colorsys.rgb_to_hsv(*map(lambda v: v / 256, rgb_value))
    h *= 360

    if v <= .07: return 'black'

    if s <= .15:
        return 'black' if v <= .3 else 'white'

    if h <= 15: return 'red'
    elif h <= 40: return 'orange'
    elif h <= 75: return 'yellow'
    elif h <= 155: return 'green'
    elif h <= 340: return 'blue'
    else: return 'red'
