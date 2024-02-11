import colorsys

def get_color(i):
    # Ensure the input integer maps to a unique hue.
    hue = (i * 137.5) % 360  # Using the golden angle approximation for spread
    saturation = 1.0  # Full saturation
    value = 1.0  # Full brightness/value
    
    # Convert hue from 0-360 to 0-1 scale for colorsys usage
    hue /= 360.0
    
    # Convert HSV to RGB
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    
    # Convert RGB from 0-1 scale to 0-255 scale
    r, g, b = [int(c * 255) for c in (r, g, b)]
    
    return (r, g, b)
