#Thumbnail, stories, product design updated on 13th june 
import os
import json
import re
from PIL import Image

def generate_slug(brand, title, filename=None):
    # Combine components to generate a descriptive slug
    parts = [brand, title]
    if filename:
        name_without_ext = os.path.splitext(filename)[0]
        # Only add filename component if it's not already in brand or title
        if name_without_ext.lower() not in title.lower() and name_without_ext.lower() not in brand.lower():
            parts.append(name_without_ext)
    
    text = " ".join(parts)
    # Convert to lowercase and split by non-alphanumeric characters
    raw_words = re.split(r'[^a-zA-Z0-9]+', text.lower())
    
    # Remove duplicates while preserving order
    words = []
    for word in raw_words:
        if word and word not in words:
            words.append(word)
    
    return "-".join(words)


base_dir = "Carousel"
output_file = "projects_data.js"

projects = []


# Custom descriptions for specific projects
custom_descriptions = {
    "PC vell Fire": "A premium roller pen design for Pierre Cardin, featuring a sleek metallic finish and ergonomic grip.",
    "PC Legacy White Gold RP": "Luxury redefined. Packaging and product design for the Legacy White Gold collection.",
    "PC Royal Salute white the gold roller pen": "Royal elegance in a pen. A high-end concept focusing on gold accents and minimalist white aesthetics.",
    "PC Coffee Brew": "Rich coffee-inspired luxury roller pen carousel post for Pierre Cardin, combining warm tones with sleek metallic accents.",
    "PC Heritage": "Classic heritage series showcase for Pierre Cardin, highlighting timeless craftsmanship, refined balance, and metallic detailing.",
    "Stain Gold Ball Pen": "Classic gold finish ball pen design, targeting the corporate gifting sector with premium packaging.",
    "PC Coffee Irish": "Sleek and rich Irish coffee themed carousel post highlighting premium pen finishes, metallic clips, and elegant typography.",
    "Flair Raw Pencil": "Eco-friendly natural wood pencil series carousel for Flair, emphasizing sustainable craft, comfortable grip, and smooth writing.",
    "Flair Raw Pencil ": "Eco-friendly natural wood pencil series carousel for Flair, emphasizing sustainable craft, comfortable grip, and smooth writing.",
    "Flair Plug GP": "Vibrant promotional carousel post for Flair Plug GP pens, featuring bold product callouts and ergonomic highlights.",
    "Hauser Art Venture": "Creative and inspiring visual identity for the Art Venture line, showcasing vibrant sketch tools for young artists.",
    "Hauser Luma": "Modern and bright aesthetic for Hauser Luma pens, featuring pastel body hues and smooth fluid ink flow.",
    "Hauser HC-801": "High-precision calculator & desk tool carousel design for Hauser HC-801, built with clean tech visuals and intuitive key layouts.",
    "Hauser Numerix": "Sleek numerical device and desk calculator promotional carousel created for Hauser Numerix series.",
    "Hauser Numerix ": "Sleek numerical device and desk calculator promotional carousel created for Hauser Numerix series.",
    "Hauser P2P Pencil": "Modern mechanical pencil carousel post for Hauser P2P, focusing on grip ergonomics, lead protection, and refill mechanism.",
    "Hauser Icy Super Dark Pencil": "Cool pastel-themed promo carousel for Hauser Icy Super Dark pencils, targeting students and artists with dark lead clarity.",
    "Froyo Pencil": "Playful, pastel-flavored pencil packaging and carousel post design for Hauser Froyo series, inspiring fun daily sketch sessions.",
    "Doms Art Vault Kit": "Premium art kit carousel showcase for Doms Art Vault, highlighting multi-tool art supplies and rich color palettes for young creators.",
    "Doms Smart Kit": "Comprehensive stationery kit packaging, designed for high shelf visibility, compactness, and complete student utility.",
    "Doms Creatist Kit": "Artistic kit box design, inspiring young creators with bold graphics, vibrant colors, and versatile drawing tools.",
    "Doms Inxtra": "Vibrant and playful packaging design for Doms Inxtra, appealing to young students.",
    "DOMS Poster Colours": "Colorful and engaging box design for Doms Poster Colours, highlighting creativity.",
    "Doms Cubo Eraser": "Innovative geometric packaging for the Cubo Eraser series.",
    "DOMS Inxify Softy": "Soft-touch pen promotion visuals, focusing on comfort and smooth writing.",
    "Maped Clip Boards": "Functional yet stylish clipboard designs for Maped, using brand colors efficiently.",
    "Maped Color'Peps Ocean 2": "Underwater themed illustrations and vibrant layout design for the Maped Color'Peps Ocean series.",
    "Color Pencil 12 Shades": "Standard 12-shade pack design, focusing on color accuracy and brightness.",
    "Hauser One pencil": "Premium wooden pencil packaging for Hauser, exuding quality and tradition.",
    "Hauser Zoodle": "Fun and quirky character-based design for the Zoodle kid's range.",
    "Hauser Xo Mate": "Sleek and professional blister card design for Xo Mate.",
    "Hauser Pixel Fine liner": "Precision-focused packaging for fine liners, using grid patterns.",
    "Montex Graphic": "Bold typography and strong contrast for Montex Graphic pens.",
    "Montex Seminar": "Professional and corporate styling for the Seminar series.",
    "Banker BP": "Reliable and classic design for the Banker Ball Pen.",
    "Montex Glow": "Neon-inspired visuals for the Montex Glow range.",
    "Mega Meter Montex": "Highlighting longevity and ink capacity in the Mega Meter packaging.",
    "Montex Ploom Chhota Bheem": "Fun character-branded fountain & gel pen carousel for Montex Ploom featuring Chhota Bheem graphics.",
    "BigInIT insta gudi post": "Vibrant social media creative celebrating the spirit of Gudi Padwa with traditional festive motifs.",
    "BigInIT insta holika dahan post": "Festive Holika Dahan post designed for BigInIT's social media, capturing warm glowing festive vibes.",
    "BigInIT": "Engaging corporate festive greeting creative designed for BigInIT social media branding.",
    "Design Dharma": "Designed brand logo and visual identity assets, capturing the brand's unique modern essence and style.",
    "Lumora Candles": "Logo design capturing the calm, warm, and handcrafted essence of eco-friendly candles.",
    "Sthir": "Logo and brand symbol designed for Sthir, capturing stillness, stability, and premium clean aesthetics.",
    "Cafe Biblio": "A charming cafe logo concept blending library theme and cozy literary vibes with minimalist visual design.",
    "4": "Vibrant and engaging vertical Instagram story layout created for promotional campaigns.",
    "Kidgets Brother's Day Story": "Heartwarming Brother's Day special Instagram story designed with fun illustrations for Kidgets.",
    "Kidgets Happy National Best friend day ": "Engaging National Best Friend Day Instagram story creative for Kidgets featuring playful visual elements.",
    "Kidgets International Day of Yoga 21st June": "Serene International Day of Yoga Instagram story designed for Kidgets with minimalist wellness graphics.",
    "Shape Happy National Best friend day ": "Bold and modern National Best Friend Day story post designed for Shape.",
    "Shape Page Story ": "Brand presentation and promotional vertical Instagram story designed with sleek typography for Shape.",
    "Shape World Environment Day 5th June": "Eco-inspired World Environment Day Instagram story designed with green aesthetic elements for Shape.",
    "Qimati Thank you card": "Elegant thank you insert card designed for luxury jewelry brand Qimati, featuring gold foil aesthetics and minimal typography.",
    "Tulsava Bag Design": "Custom product carry bag packaging designed for Tulsava, showcasing front and back layout designs with elegant branding.",
    "Tulsava Thank You Card": "Charming thank you insert card designed for Tulsava, enhancing unboxing experience with warm personal messaging."
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
    "Flair Plug GP",
    "Hauser Art Venture",
    "Hauser Luma",
    "Hauser HC-801",
    "Hauser Numerix",
    "Hauser P2P Pencil",
    "Hauser Icy Super Dark Pencil",
    "Froyo Pencil",
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
             desc_text = custom_descriptions.get(title_clean, "Logo Design" if directory_name == "Logo" else "Festive Celebration Post")

             data.append({
                "brand": brand_name,
                "title": title_clean, 
                "folder": directory_name,
                "images": [img_file],
                "description": desc_text,
                "instagram_link": "",
                "aspect_ratio": aspect_ratio,
                "sort_order": 999,
                "slug": generate_slug(brand_name, title_clean, img_file)
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
                    "sort_order": sort_order,
                    "slug": generate_slug(brand.replace('_', ' '), title_clean)
                })
    
    # Sort projects.
    # Primary sort: Aspect Ratio (group by size)
    # Secondary: Sort Order (maintain Top 10 relative preference within same size)
    # Tertiary: Brand/Title
    data.sort(key=lambda x: (round(x.get('aspect_ratio', 0), 2), x['sort_order'], x['brand'], x['title']))
    return data

def scan_thumbnails(directory_name):
    data = []
    if not os.path.exists(directory_name):
        return data
    
    folders = [d for d in os.listdir(directory_name) if os.path.isdir(os.path.join(directory_name, d)) and not d.startswith('.')]
    folders.sort()
    
    for folder in folders:
        folder_path = os.path.join(directory_name, folder)
        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
        images.sort(key=lambda x: int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else x)
        
        for img_file in images:
            img_path = os.path.join(folder_path, img_file)
            title_clean = f"{folder} Thumbnail"
            
            aspect_ratio = 16/9
            try:
                with Image.open(img_path) as img:
                    w, h = img.size
                    aspect_ratio = w / h
            except Exception as e:
                print(f"Error reading image {img_path}: {e}")
            
            description = f"Instagram Thumbnail design created for {folder}."
            if folder == "Shape":
                description = "Minimalist and bold Instagram thumbnail design created for Shape."
            elif folder == "Kidgets":
                description = "Vibrant and engaging Instagram thumbnail design created for Kidgets."

            data.append({
                "brand": folder,
                "title": title_clean,
                "folder": os.path.join(directory_name, folder),
                "images": [img_file],
                "description": description,
                "instagram_link": "",
                "aspect_ratio": aspect_ratio,
                "sort_order": 999,
                "slug": generate_slug(folder, title_clean, img_file)
            })
    return data

def scan_stories(directory_name):
    data = []
    if not os.path.exists(directory_name):
        return data
    
    story_metadata = {
        "1.jpg": {
            "brand": "Gujarat Titans",
            "title": "Gujarat Titans IPL Champions Story",
            "description": "IPL Champions celebratory story design created for Gujarat Titans."
        },
        "4.jpg": {
            "brand": "Royal Challengers Bengaluru",
            "title": "RCB IPL Champions Story",
            "description": "IPL Champions celebratory story design created for Royal Challengers Bengaluru."
        },
        "Kidgets Brother's Day Story.jpg": {
            "brand": "Kidgets",
            "title": "Brother's Day Special Story",
            "description": "Heartwarming Brother's Day special Instagram story designed for Kidgets."
        },
        "Kidgets Happy National Best friend day .jpg": {
            "brand": "Kidgets",
            "title": "National Best Friend Day Story",
            "description": "Engaging National Best Friend Day Instagram story creative designed for Kidgets."
        },
        "Kidgets International Day of Yoga 21st June.jpg": {
            "brand": "Kidgets",
            "title": "International Day of Yoga Story",
            "description": "Serene International Day of Yoga Instagram story designed for Kidgets."
        },
        "Shape Happy National Best friend day .jpg": {
            "brand": "Shape",
            "title": "National Best Friend Day Story",
            "description": "Bold and modern National Best Friend Day story post designed for Shape."
        },
        "Shape Page Story .jpg": {
            "brand": "Shape",
            "title": "Brand Highlights Story",
            "description": "Brand presentation and promotional vertical Instagram story designed for Shape."
        },
        "Shape World Environment Day 5th June.jpg": {
            "brand": "Shape",
            "title": "World Environment Day Story",
            "description": "Eco-inspired World Environment Day Instagram story designed for Shape."
        }
    }

    files = [f for f in os.listdir(directory_name) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
    files.sort()
    
    for img_file in files:
        product_path = os.path.join(directory_name, img_file)
        meta = story_metadata.get(img_file, {
            "brand": "Stories",
            "title": os.path.splitext(img_file)[0].replace('_', ' '),
            "description": f"Instagram Story design created for {directory_name}."
        })
        
        aspect_ratio = 9/16
        try:
            with Image.open(product_path) as img:
                w, h = img.size
                aspect_ratio = w / h
        except Exception as e:
            print(f"Error reading image {img_file}: {e}")

        data.append({
            "brand": meta["brand"],
            "title": meta["title"],
            "folder": directory_name,
            "images": [img_file],
            "description": meta["description"],
            "instagram_link": "",
            "aspect_ratio": aspect_ratio,
            "sort_order": 999,
            "slug": generate_slug(meta["brand"], meta["title"], img_file)
        })
    return data

def scan_product_design(directory_name):
    data = []
    if not os.path.exists(directory_name):
        return data
    
    items = [i for i in os.listdir(directory_name) if not i.startswith('.')]
    
    for item in items:
        item_path = os.path.join(directory_name, item)
            
        if os.path.isdir(item_path):
            # Group all images in the subdirectory into a single project carousel
            images = [f for f in os.listdir(item_path) if f.lower().endswith(('.jpg', '.jpeg', '.png')) and not f.startswith('.')]
            images.sort(key=lambda x: (0 if "front" in x.lower() else (1 if "back" in x.lower() else 2), int(os.path.splitext(x)[0]) if os.path.splitext(x)[0].isdigit() else x))
            
            if images:
                aspect_ratio = 1.0 # default
                try:
                    first_image_path = os.path.join(item_path, images[0])
                    with Image.open(first_image_path) as img:
                        w, h = img.size
                        aspect_ratio = w / h
                except Exception as e:
                    print(f"Error reading image {first_image_path}: {e}")
                
                title_clean = item.replace('_', ' ')
                description = f"Product packaging and thank you card design for {title_clean}."
                if "qimati" in title_clean.lower():
                    description = "Elegant thank you insert card designed for luxury jewelry brand Qimati."
                elif "tulsava" in title_clean.lower() and "bag" in title_clean.lower():
                    description = "Custom product carry bag packaging designed for Tulsava."
                elif "tulsava" in title_clean.lower():
                    description = "Charming thank you insert card designed for Tulsava."

                data.append({
                    "brand": "Product Design",
                    "title": title_clean,
                    "folder": item_path,
                    "images": images,
                    "description": description,
                    "instagram_link": "",
                    "aspect_ratio": aspect_ratio,
                    "sort_order": 999,
                    "slug": generate_slug("Product Design", title_clean)
                })
        else:
            # It's a flat image file (Tulsava bag Design.png)
            if item.lower().endswith(('.jpg', '.jpeg', '.png')):
                title_clean = os.path.splitext(item)[0].replace('_', ' ')
                
                aspect_ratio = 1.0
                try:
                    with Image.open(item_path) as img:
                        w, h = img.size
                        aspect_ratio = w / h
                except Exception as e:
                    print(f"Error reading image {item_path}: {e}")
                
                description = f"Custom bag packaging design for Tulsava."
                if "tulsava" in title_clean.lower():
                    description = "Custom product carry bag packaging designed for Tulsava."

                data.append({
                    "brand": "Product Design",
                    "title": title_clean,
                    "folder": directory_name,
                    "images": [item],
                    "description": description,
                    "instagram_link": "",
                    "aspect_ratio": aspect_ratio,
                    "sort_order": 999,
                    "slug": generate_slug("Product Design", title_clean, item)
                })
                
    # Sort by title
    data.sort(key=lambda x: x['title'])
    return data

# Scan Carousel with filtering
projects = scan_directory("Carousel", filter_top_10=True)

# Scan Festive Posts without filtering
festive_projects = scan_directory("Festive_Posts", filter_top_10=False)

# Scan Logo without filtering
logo_projects = scan_directory("Logo", filter_top_10=False)

# Scan Thumbnail without filtering
thumbnail_projects = scan_thumbnails("Thumbnail")

# Scan Stories without filtering
stories_projects = scan_stories("Stories")

# Scan Product Design without filtering
product_design_projects = scan_product_design("Product Design")

# Verify uniqueness of slugs
all_slugs = []
for dataset_name, dataset in [
    ("Carousel", projects),
    ("Festive", festive_projects),
    ("Logo", logo_projects),
    ("Thumbnail", thumbnail_projects),
    ("Stories", stories_projects),
    ("Product Design", product_design_projects)
]:
    for p in dataset:
        all_slugs.append(p['slug'])

# Check for duplicates
duplicates = set([s for s in all_slugs if all_slugs.count(s) > 1])
if duplicates:
    print(f"Warning: Duplicate slugs found: {duplicates}")
    # Resolve duplicates by adding suffix
    seen = {}
    for dataset in [projects, festive_projects, logo_projects, thumbnail_projects, stories_projects, product_design_projects]:
        for p in dataset:
            slug = p['slug']
            if slug in duplicates:
                seen[slug] = seen.get(slug, 0) + 1
                if seen[slug] > 1:
                    p['slug'] = f"{slug}-{seen[slug]}"
                    print(f"Resolved duplicate slug to: {p['slug']}")

js_content = f"const projectsData = {json.dumps(projects, indent=4)};\nconst festiveData = {json.dumps(festive_projects, indent=4)};\nconst logoData = {json.dumps(logo_projects, indent=4)};\nconst thumbnailData = {json.dumps(thumbnail_projects, indent=4)};\nconst storiesData = {json.dumps(stories_projects, indent=4)};\nconst productDesignData = {json.dumps(product_design_projects, indent=4)};"

with open(output_file, "w") as f:
    f.write(js_content)

print(f"Generated {output_file} with {len(projects)} curated projects, {len(festive_projects)} festive posts, {len(logo_projects)} logos, {len(thumbnail_projects)} thumbnails, {len(stories_projects)} stories, and {len(product_design_projects)} product designs.")
