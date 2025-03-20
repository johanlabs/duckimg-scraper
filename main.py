import os
import time
import requests
import sys
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def download_images(terms, quantity, use_subfolders=True):
    """
    Downloads images from DuckDuckGo with support for categories and subfolders.

    Args:
        terms (str): Search terms in "category=term1,term2" format or "term1,term2".
        quantity (int): Number of images per term.
        use_subfolders (bool): If True, creates subfolders inside categories.
    """
    
    # Parse terms (supports categories)
    categories = {}
    simple_terms = []
    
    for part in terms.split(","):
        if "=" in part:
            category, items = part.split("=")
            categories[category.strip()] = [item.strip() for item in items.split(",")]
        else:
            simple_terms.append(part.strip())  # No category, save directly
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Process terms without categories
    for term in simple_terms:
        folder = term.replace(" ", "_")
        
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"📁 Folder '{folder}' created.")
        
        url = f"https://duckduckgo.com/?q={term}&iar=images&iax=images&ia=images"
        driver.get(url)
        time.sleep(2)
        
        images = []
        while len(images) < quantity:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            images = driver.find_elements(By.CSS_SELECTOR, "img.tile--img__img")
            if len(images) >= quantity:
                break
        
        print(f"🔍 Found {len(images)} images for '{term}'. Downloading {quantity} images...")
        
        downloaded = 0
        for img in images:
            if downloaded >= quantity:
                break
            src = img.get_attribute("src")
            if src and src.startswith("http"):
                try:
                    response = requests.get(src, timeout=10)
                    if response.status_code == 200:
                        image_path = os.path.join(folder, f"image_{downloaded + 1}.jpg")
                        with open(image_path, "wb") as f:
                            f.write(response.content)
                        downloaded += 1
                        print(f"✅ Image {downloaded} saved: {image_path}")
                except Exception as e:
                    print(f"❌ Error downloading image: {e}")
    
    # Process categories
    for category, items in categories.items():
        if not os.path.exists(category):
            os.makedirs(category)
            print(f"📁 Folder '{category}' created.")
        
        for term in items:
            folder = os.path.join(category, term.replace(" ", "_")) if use_subfolders else category
            
            if use_subfolders and not os.path.exists(folder):
                os.makedirs(folder)
                print(f"📂 Subfolder '{folder}' created.")
            
            url = f"https://duckduckgo.com/?q={category}+{term}&iar=images&iax=images&ia=images"
            driver.get(url)
            time.sleep(2)
            
            images = []
            while len(images) < quantity:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                images = driver.find_elements(By.CSS_SELECTOR, "img.tile--img__img")
                if len(images) >= quantity:
                    break
            
            print(f"🔍 Found {len(images)} images for '{category} {term}'. Downloading {quantity} images...")
            
            downloaded = 0
            for img in images:
                if downloaded >= quantity:
                    break
                src = img.get_attribute("src")
                if src and src.startswith("http"):
                    try:
                        response = requests.get(src, timeout=10)
                        if response.status_code == 200:
                            image_path = os.path.join(folder, f"image_{downloaded + 1}.jpg")
                            with open(image_path, "wb") as f:
                                f.write(response.content)
                            downloaded += 1
                            print(f"✅ Image {downloaded} saved: {image_path}")
                    except Exception as e:
                        print(f"❌ Error downloading image: {e}")
    
    driver.quit()
    print("🎉 Download completed.")

def main():
    parser = argparse.ArgumentParser(description="DuckDuckGo Image Scraper with Categories and Subfolders")
    parser.add_argument("terms", type=str, help="Search terms (category=term1,term2 or term1,term2)")
    parser.add_argument("quantity", type=int, help="Number of images per term")
    parser.add_argument("--no-subfolders", action="store_true", help="Disable subfolders inside categories")
    
    args = parser.parse_args()
    
    download_images(args.terms, args.quantity, not args.no_subfolders)

if __name__ == "__main__":
    main()
