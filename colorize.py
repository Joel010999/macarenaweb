from PIL import Image
import os

input_path = "Logo/PNG transparente/Recurso 24@2x.png"

def colorize_image(input_path, output_path, r_target, g_target, b_target):
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        # Keep the original alpha
        alpha = item[3]
        # Only change RGB if the pixel is not fully transparent
        if alpha > 0:
            new_data.append((r_target, g_target, b_target, alpha))
        else:
            new_data.append((255, 255, 255, 0)) # Fully transparent

    img.putdata(new_data)
    img.save(output_path, "PNG")

# Generate pink logo
colorize_image(input_path, "Logo/logo-pink.png", 222, 62, 119)
print("logo-pink.png created")

# Generate white logo
colorize_image(input_path, "Logo/logo-white.png", 255, 255, 255)
print("logo-white.png created")
