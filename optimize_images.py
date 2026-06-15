import os
import glob
from PIL import Image

def optimize_images():
    # Find all JPG files in directories matching "Produ *"
    base_dir = r"c:\Renderbyte\Maca"
    
    # Let's search inside Produ folders
    pattern = os.path.join(base_dir, "Produ *", "*.jpg")
    files = glob.glob(pattern)
    
    total_files = len(files)
    print(f"Found {total_files} JPG files to process.")
    
    for i, file_path in enumerate(files):
        try:
            # We want to check the size, if it's already small (< 500kb), we can probably skip it, 
            # but let's process everything just to be safe.
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb < 0.5:
                continue # Skip small files

            with Image.open(file_path) as img:
                # Convert to RGB in case of some weird color spaces
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if the image is too large (e.g. max 1000px width/height)
                max_size = (1000, 1000)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save it over the original file, compressed
                img.save(file_path, "JPEG", quality=80, optimize=True)
            
            if (i+1) % 10 == 0:
                print(f"Processed {i+1}/{total_files}...")
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    print("Optimization complete!")

if __name__ == "__main__":
    optimize_images()
