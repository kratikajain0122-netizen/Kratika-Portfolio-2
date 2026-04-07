
from PIL import Image
import os
import glob

assets_dir = 'Assets'
output_dir = 'Assets'

# List of files to process
files = [
    "Difference Between Procreate and Illustrator.jpg",
    " .jpg",
    "🎨 Canva Creations_ Design Magic Unleashed.jpg",
    "Corel Logo.jpg",
    "Figma_ The Collaborative Interface Design Tool.jpg"
]

def remove_white_bg(input_path, output_path):
    try:
        img = Image.open(input_path)
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            # Change all white (also shades of whites) to transparent
            if item[0] > 200 and item[1] > 200 and item[2] > 200:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save(output_path, "PNG")
        print(f"Successfully converted {input_path} to {output_path}")
    except Exception as e:
        print(f"Failed to process {input_path}: {e}")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in files:
    input_path = os.path.join(assets_dir, filename)
    # Create a cleaner filename for the output
    clean_name = filename.replace('.jpg', '.png').replace('Difference Between Procreate and Illustrator', 'Illustrator_Logo').replace(' .png', 'Photoshop_Logo.png').replace(' .jpg', 'Photoshop_Logo.png').replace('🎨 Canva Creations_ Design Magic Unleashed', 'Canva_Logo').replace('Corel Logo', 'CorelDraw_Logo').replace('Figma_ The Collaborative Interface Design Tool', 'Figma_Logo').strip()
    
    # Handle the specific case for Photoshop which might result in weird names
    if " .jpg" in filename:
        clean_name = "Photoshop_Logo.png"
    elif "Canva" in filename:
        clean_name = "Canva_Logo.png"
    elif "Illustrator" in filename:
        clean_name = "Illustrator_Logo.png"
    elif "Corel" in filename:
        clean_name = "CorelDraw_Logo.png"
    elif "Figma" in filename:
        clean_name = "Figma_Logo.png"

    output_path = os.path.join(output_dir, clean_name)
    
    if os.path.exists(input_path):
        remove_white_bg(input_path, output_path)
    else:
        print(f"File not found: {input_path}")
