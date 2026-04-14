import os
import json
from PIL import Image

base_dir = "Carousel"
output_file = "projects_data.js"

projects = []


# Custom descriptions for specific projects
custom_descriptions = {
    "PC vell Fire": "A premium roller pen design for Pierre Cardin, featuring a sleek metallic finish and ergonomic grip.",
    "PC Legacy White Gold RP": "Luxury redefined. Packaging and product design for the Legacy White Gold collection.",
    "PC Royal Salute white the gold roller pen": "Royal elegance in a pen. A high-end concept focusing on gold accents and minimalist white aesthetics.",
    "Stain Gold Ball Pen": "Classic gold finish ball pen design, targeting the corporate gifting sector.",
    "PC Momento BP": "Modern and stylish ball pen concept for everyday professional use.",
    "Doms Inxtra": "Vibrant and playful packaging design for Doms Inxtra, appealing to young students.",
    "DOMS Poster Colours": "Colorful and engaging box design for Doms Poster Colours, highlighting creativity.",
    "Doms Smart Kit": "Comprehensive stationery kit packaging, designed for visibility and compactness.",
    "Doms Creatist Kit": "Artistic kit box design, inspiring young creators with bold graphics.",
    "Doms Cubo Eraser": "Innovative geometric packaging for the Cubo Eraser series.",
    "DOMS Inxify Softy": "Soft-touch pen promotion visuals, focusing on comfort and smooth writing.",
    "Mi-201N": "Minimalist tech-inspired stationery design for MI.",
    "Mi-847": "Sleek and functional product design, aligning with MI's clean design philosophy.",
    "Flair Raw Pencil": "Eco-friendly natural wood look for Flair Raw Pencils. Simple yet impactful.",
    "Flair Move X": "Dynamic and energetic packaging for the Move X series.",
    "Flair Mark Mechanical 0.7mm": "Technical precision highlighted in the blister pack design for this mechanical pencil.",
    "Flair Arti Graff": "Bold and artistic branding for the Arti Graff sketching collection.",
    "Flair Carbonix Mechanical Pencil": "Futuristic design elements for the Carbonix range, emphasizing durability.",
    "Maped Clip Boards": "Functional yet stylish clipboard designs for Maped, using brand colors efficiently.",
    "Maped Color'Peps Ocean 2": "Underwater themed illustrations for the Color'Peps Ocean series.",
    "Color Pencil 12 Shades": "Standard 12-shade pack design, focusing on color accuracy and brightness.",
    "Hauser One pencil": "Premium wooden pencil packaging for Hauser, exuding quality and tradition.",
    "Hauser Art Venture": "Creative and inspiring visual identity for the Art Venture line.",
    "Hauser Luma": "Modern and bright aesthetic for Hauser Luma pens.",
    "Hauser Zoodle": "Fun and quirky character-based design for the Zoodle kid's range.",
    "Hauser Xo Mate": "Sleek and professional blister card design for Xo Mate.",
    "Hauser Pixel Fine liner": "Precision-focused packaging for fine liners, using grid patterns.",
    "Montex Graphic": "Bold typography and strong contrast for Montex Graphic pens.",
    "Montex Seminar": "Professional and corporate styling for the Seminar series.",
    "Banker BP": "Reliable and classic design for the Banker Ball Pen.",
    "Montex Glow": "Neon-inspired visuals for the Montex Glow range.",
    "Mega Meter Montex": "Highlighting longevity and ink capacity in the Mega Meter packaging.",
    "BigInIT insta gudi post": "Vibrant social media creative celebrating the spirit of Gudi Padwa.",
    "BigInIT insta holika dahan post": "Festive Holika Dahan post designed for BigInIT's social media."
}

# Curated list of Top 10 Projects to display in Carousel
# Curated list of Top 10 Projects to display in Carousel
CURATED_TOP_10 = [
    "PC vell Fire",
    "PC Royal Salute white the gold roller pen",
    "PC Coffee Brew",
    "PC Heritage",
    "Stain Gold Ball Pen",
    "PC Coffee Irish",
    "Doms Art Vault Kit",
    "Doms Smart Kit",
    "Doms Creatist Kit",
    "Maped Color'Peps Ocean 2",
    "Flair Raw Pencil",
    "Hauser Art Venture",
    "Hauser Xo Mate",
    "Hauser Luma",
    "Montex Ploom Chhota Bheem"
]

def scan_directory(directory_name, filter_top_10=False):
    data = []
    if not os.path.exists(directory_name):
        return data

    # Check if folder contains images directly (Flat structure like Festive_Posts)
    # or subdirectories (Nested structure like Carousel)
    items = [i for i in os.listdir(directory_name) if not i.startswith('.')]
    has_subdirs = any(os.path.isdir(os.path.join(directory_name, i)) for i in items)

    if not has_subdirs:
        # Flat structure: Treat each image as a standalone project
        images = [f for f in items if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        images.sort()
        
        for img_file in images:
             product_path = os.path.join(directory_name, img_file)
             title_clean = os.path.splitext(img_file)[0].replace('_', ' ')
             
             aspect_ratio = 4/5
             try:
                 with Image.open(product_path) as img:
                    w, h = img.size
                    aspect_ratio = w / h
             except Exception as e:
                 print(f"Error reading image {img_file}: {e}")
             
             brand_name = "Logo Designs" if directory_name == "Logo" else "Festive"
             desc_text = "Logo Design" if directory_name == "Logo" else "Festive Celebration Post"

             data.append({
                "brand": brand_name,
                "title": title_clean, 
                "folder": directory_name,
                "images": [img_file],
                "description": desc_text,
                "instagram_link": "",
                "aspect_ratio": aspect_ratio,
                "sort_order": 999
             })
        return data

    # Nested structure (Carousel)
    brands = [d for d in items if os.path.isdir(os.path.join(directory_name, d))]
    
    for brand in brands:
        brand_path = os.path.join(directory_name, brand)
        products = [d for d in os.listdir(brand_path) if os.path.isdir(os.path.join(brand_path, d)) and not d.startswith('.')]
        
        for product in products:
            title_clean = product.replace('_', ' ')
            
            # If filtering is enabled (for Carousel), skip if not in Top 10
            sort_order = 999
            if filter_top_10:
                match = False
                for idx, top_item in enumerate(CURATED_TOP_10):
                    # Check for exact match or robust containment
                    # Normalize both to lowercase and strip for comparison
                    if top_item.lower().strip() == title_clean.lower().strip():
                        match = True
                        sort_order = idx
                        break
                    # Fallback partial match
                    elif top_item.lower() in title_clean.lower() or title_clean.lower() in top_item.lower():
                         match = True
                         sort_order = idx
                         break
                
                if not match:
                    # print(f"Skipping {title_clean} (not in Top 10)")
                    continue 

            product_path = os.path.join(brand_path, product)
            # Find images
            images = [f for f in os.listdir(product_path) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
            # Sort images to ensure order 1.jpg, 2.jpg, etc.
            images.sort(key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else x)
            
            if images:
                aspect_ratio = 4/5 # Default fallback
                try:
                    first_image_path = os.path.join(product_path, images[0])
                    with Image.open(first_image_path) as img:
                        w, h = img.size
                        aspect_ratio = w / h
                except Exception as e:
                    print(f"Error reading image {product}: {e}")

                # Get custom description or fall back to default
                desc = custom_descriptions.get(title_clean, "Designed during my internship at Student Yard.")
                
                data.append({
                    "brand": brand.replace('_', ' '),
                    "title": title_clean,
                    "folder": os.path.join(directory_name, brand, product),
                    "images": images,
                    "description": desc,
                    "instagram_link": "",
                    "aspect_ratio": aspect_ratio,
                    "sort_order": sort_order
                })
    
    # Sort projects.
    # Primary sort: Aspect Ratio (group by size)
    # Secondary: Sort Order (maintain Top 10 relative preference within same size)
    # Tertiary: Brand/Title
    data.sort(key=lambda x: (round(x.get('aspect_ratio', 0), 2), x['sort_order'], x['brand'], x['title']))
    return data

# Scan Carousel with filtering
projects = scan_directory("Carousel", filter_top_10=True)

# Scan Festive Posts without filtering
festive_projects = scan_directory("Festive_Posts", filter_top_10=False)

# Scan Logo without filtering
logo_projects = scan_directory("Logo", filter_top_10=False)

js_content = f"const projectsData = {json.dumps(projects, indent=4)};\nconst festiveData = {json.dumps(festive_projects, indent=4)};\nconst logoData = {json.dumps(logo_projects, indent=4)};"

with open(output_file, "w") as f:
    f.write(js_content)

print(f"Generated {output_file} with {len(projects)} curated projects, {len(festive_projects)} festive posts, and {len(logo_projects)} logos.")
