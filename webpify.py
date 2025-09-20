import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

# ------------------------------
# CONFIG
# ------------------------------
TEMPLATES_DIR = "templates"
IMAGES_DIR = "static/images"
DELETE_OLD = True  # Set to False to keep original PNG/JPG

# ------------------------------
# STEP 1: Collect all images from HTML
# ------------------------------
image_usage = {}  # {image_src: {"max_width": w, "max_height": h}}

# Set up headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

for template_file in os.listdir(TEMPLATES_DIR):
    if not template_file.endswith(".html"):
        continue
    path = os.path.join(TEMPLATES_DIR, template_file)
    driver.get("file://" + os.path.abspath(path))
    
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        
        try:
            element = driver.find_element("css selector", f'img[src="{src}"]')
            size = element.size  # {"width": ..., "height": ...}
        except:
            # fallback if selenium cannot find it
            size = {"width": int(img.get("width") or 0),
                    "height": int(img.get("height") or 0)}
        
        if src in image_usage:
            image_usage[src]["width"] = max(image_usage[src]["width"], size["width"])
            image_usage[src]["height"] = max(image_usage[src]["height"], size["height"])
        else:
            image_usage[src] = {"width": size["width"], "height": size["height"]}

driver.quit()

# ------------------------------
# STEP 2: Convert images to WebP
# ------------------------------
for src, size in image_usage.items():
    original_path = os.path.join(IMAGES_DIR, os.path.basename(src))
    if not os.path.exists(original_path):
        print(f"Skipping {original_path}, file not found.")
        continue
    
    webp_path = os.path.splitext(original_path)[0] + ".webp"
    
    # Open, resize, and save as WebP
    im = Image.open(original_path)
    
    # Only resize if larger than max display size
    max_width, max_height = size["width"], size["height"]
    if max_width > 0 and max_height > 0:
        im.thumbnail((max_width, max_height), Image.ANTIALIAS)
    
    im.save(webp_path, "WEBP", quality=80)
    
    # Optionally delete original
    if DELETE_OLD:
        os.remove(original_path)
    
    print(f"Converted {original_path} -> {webp_path}")

# ------------------------------
# STEP 3: Update HTML templates
# ------------------------------
for template_file in os.listdir(TEMPLATES_DIR):
    if not template_file.endswith(".html"):
        continue
    path = os.path.join(TEMPLATES_DIR, template_file)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    for src in image_usage.keys():
        webp_src = os.path.splitext(src)[0] + ".webp"
        html = html.replace(src, webp_src)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Updated {template_file} to use WebP images.")
