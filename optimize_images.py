import os
import subprocess
import shutil

def get_dimensions(filepath):
    try:
        output = subprocess.check_output(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', filepath], stderr=subprocess.DEVNULL).decode('utf-8')
        width = 0
        height = 0
        for line in output.split('\n'):
            if 'pixelWidth:' in line:
                width = int(line.split(':')[1].strip())
            elif 'pixelHeight:' in line:
                height = int(line.split(':')[1].strip())
        return width, height
    except Exception:
        return 0, 0

def optimize_images(directory):
    total_saved = 0
    count = 0
    for root, dirs, files in os.walk(directory):
        if '.git' in root or '.gemini' in root:
            continue
        for file in files:
            if file.startswith('.'):
                continue
            ext = file.lower().split('.')[-1]
            if ext in ['jpg', 'jpeg', 'png', 'webp']:
                filepath = os.path.join(root, file)
                try:
                    orig_size = os.path.getsize(filepath)
                except Exception:
                    continue
                
                width, height = get_dimensions(filepath)
                max_dim = max(width, height)
                
                cmd = ['sips']
                should_run = False
                
                if max_dim > 1920:
                    cmd.extend(['-Z', '1920'])
                    should_run = True
                
                if ext in ['jpg', 'jpeg']:
                    cmd.extend(['-s', 'formatOptions', '80'])
                    should_run = True
                
                # To reduce extremely large PNGs that are smaller than 1920px (if any exist)
                # sips doesn't support PNG compression directly nicely, so we only resize
                if should_run:
                    temp_filepath = filepath + '.tmp'
                    cmd.extend([filepath, '--out', temp_filepath])
                    try:
                        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        if os.path.exists(temp_filepath):
                            new_size = os.path.getsize(temp_filepath)
                            # Only keep if we actually save space (at least 5%)
                            if new_size < orig_size * 0.95:
                                os.replace(temp_filepath, filepath)
                                saved = orig_size - new_size
                                total_saved += saved
                                count += 1
                                print(f"Optimized: {filepath} (-{saved / (1024*1024):.2f} MB)")
                            else:
                                os.remove(temp_filepath)
                    except Exception as e:
                        print(f"Failed to optimize {filepath}: {e}")
                        if os.path.exists(temp_filepath):
                            os.remove(temp_filepath)
                
    print(f"Total images optimized: {count}")
    print(f"Total space saved: {total_saved / (1024 * 1024):.2f} MB")

if __name__ == '__main__':
    optimize_images('.')
