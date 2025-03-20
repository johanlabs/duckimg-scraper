from setuptools import setup, find_packages

setup(
    name="duckimg-scraper",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "requests",
        "webdriver-manager",
    ],
    entry_points={
        "console_scripts": [
            "duckimg = duckimg_scraper:main",
        ],
    },
)
