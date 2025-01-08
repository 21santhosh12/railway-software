from cairosvg import svg2png
from PIL import Image
import io

# Read the SVG file
with open('static/favicon.svg', 'rb') as svg_file:
    svg_data = svg_file.read()

# Convert SVG to PNG in memory
png_data = svg2png(bytestring=svg_data, output_width=32, output_height=32)

# Convert PNG to ICO
img = Image.open(io.BytesIO(png_data))
img.save('static/favicon.ico', format='ICO', sizes=[(32, 32)])

print("Favicon created successfully!") 