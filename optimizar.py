import os
import sys
import subprocess
import glob

# Asegurar que Pillow esté instalado
try:
    from PIL import Image
except ImportError:
    print("Instalando Pillow...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image

def optimize_images():
    base_dir = "c:/Renderbyte/Maca"
    out_dir = os.path.join(base_dir, "web-assets")
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Encontrar carpetas de productos
    folders = [f for f in os.listdir(base_dir) if f.startswith("Produ ") and os.path.isdir(os.path.join(base_dir, f))]
    
    total_optimized = 0
    
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        out_folder_path = os.path.join(out_dir, folder)
        
        if not os.path.exists(out_folder_path):
            os.makedirs(out_folder_path)
            
        images = [i for i in os.listdir(folder_path) if i.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for img_name in images:
            img_path = os.path.join(folder_path, img_name)
            
            # Guardar como webp
            name_without_ext = os.path.splitext(img_name)[0]
            out_img_path = os.path.join(out_folder_path, f"{name_without_ext}.webp")
            
            # Solo procesar si no existe ya
            if not os.path.exists(out_img_path):
                try:
                    with Image.open(img_path) as img:
                        # Convertir a RGB por si es RGBA o P
                        if img.mode in ("RGBA", "P"):
                            img = img.convert("RGB")
                            
                        # Redimensionar max 800 width
                        max_width = 800
                        if img.width > max_width:
                            wpercent = (max_width / float(img.width))
                            hsize = int((float(img.height) * float(wpercent)))
                            img = img.resize((max_width, hsize), Image.Resampling.LANCZOS)
                            
                        # Guardar con compresión
                        img.save(out_img_path, 'webp', quality=80)
                        total_optimized += 1
                        print(f"Optimizada: {out_img_path}")
                except Exception as e:
                    print(f"Error procesando {img_path}: {e}")

    print(f"Proceso completado. Se optimizaron {total_optimized} imágenes.")

if __name__ == "__main__":
    optimize_images()
