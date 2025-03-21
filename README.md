# 🦆 DuckImg Scraper

DuckImg Scraper is a command-line tool for scraping images from DuckDuckGo, designed to help in training AI models by collecting categorized images efficiently.

## 🚀 Features
- Supports categorized searches using `category=term1,term2` format.
- Saves images in structured folders.
- Uses Selenium and DuckDuckGo for efficient scraping.
- Command-line interface for easy usage.

## 📥 Installation
```sh
pip install -r requirements.txt
```

## 🛠 Usage

### Basic Usage
Run the following command to download images:
```sh
python main.py "cars=tesla,ferrari" 50
```
This will download 50 images each for "tesla" and "ferrari" inside a "cars" folder.

### Without Categories
If no categories are provided, images are stored directly:
```sh
python main.py "dog,cat" 30
```
This will download 30 images each for "dog" and "cat" in separate folders.

### Disabling Subfolders
To disable subfolders inside categories:
```sh
python main.py "cars=tesla,ferrari" 50 --no-subfolders
```
This will save all images inside the "cars" folder without subdirectories.

### Example in Python
You can also use DuckImg Scraper in a Python script:
```python
from dockimg import download_images

download_images("fruits=apple,banana", 20, use_subfolders=False)
```

# Projects with using duckimg-scraper

Image-classification - https://github.com/Sem-Segredos-Tech/image-classification

## ⚠️ Scraping Limitations
DuckDuckGo may temporarily block repeated scraping requests. To mitigate this:
- Use a delay between requests.
- Utilize proxy services.
- Avoid running large batches in a short time.

Happy Scraping! 🦆
