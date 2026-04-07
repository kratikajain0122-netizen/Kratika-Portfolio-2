import os

def sanitize_path(root_dir):
    # Walk bottom-up so we rename children before parents
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Rename files
        for filename in filenames:
            if ' ' in filename:
                new_filename = filename.replace(' ', '_')
                old_file = os.path.join(dirpath, filename)
                new_file = os.path.join(dirpath, new_filename)
                os.rename(old_file, new_file)
                print(f"Renamed file: {filename} -> {new_filename}")

        # Rename directories
        for dirname in dirnames:
            if ' ' in dirname:
                new_dirname = dirname.replace(' ', '_')
                old_dir = os.path.join(dirpath, dirname)
                new_dir = os.path.join(dirpath, new_dirname)
                os.rename(old_dir, new_dir)
                print(f"Renamed dir: {dirname} -> {new_dirname}")

if __name__ == "__main__":
    base_dir = "Carousel"
    if os.path.exists(base_dir):
        sanitize_path(base_dir)
        print("Sanitization complete.")
    else:
        print(f"Directory {base_dir} not found.")
