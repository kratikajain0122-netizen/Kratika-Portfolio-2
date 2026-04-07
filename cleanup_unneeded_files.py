import os
import shutil

# This should match the updated CURATED_TOP_10 in generate_projects_json.py
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

def cleanup_unused_carousels(base_dir="Carousel"):
    deleted_count = 0
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} not found.")
        return

    # Normalize curated list for comparison
    curated_normalized = [item.replace('_', ' ').lower().strip() for item in CURATED_TOP_10]

    for brand in os.listdir(base_dir):
        if brand.startswith('.'):
            continue
            
        brand_path = os.path.join(base_dir, brand)
        if not os.path.isdir(brand_path):
            continue

        for product in os.listdir(brand_path):
            if product.startswith('.'):
                continue
                
            product_path = os.path.join(brand_path, product)
            if not os.path.isdir(product_path):
                continue
                
            title_clean = product.replace('_', ' ').lower().strip()
            
            # Check if this product is in our curated list
            is_curated = False
            for top_item in curated_normalized:
                if top_item == title_clean or top_item in title_clean or title_clean in top_item:
                    is_curated = True
                    break
            
            if not is_curated:
                print(f"Removing unused carousel: {product_path}")
                try:
                    shutil.rmtree(product_path)
                    deleted_count += 1
                except Exception as e:
                    print(f"Error removing {product_path}: {e}")
                    
    print(f"Total carousels removed: {deleted_count}")

if __name__ == "__main__":
    cleanup_unused_carousels()
