# PhotoRank

A Python application that helps you organize and rank similar photos using machine learning.

## Features

- Automatic clustering of similar photos using ResNet50
- Support for JPG, JPEG, PNG, and HEIC formats
- Progress tracking with visual feedback
- Easy-to-use command-line interface

## Installation

1. Clone this repository:
```bash
git clone https://github.com/joeypohie/photorank.git
cd photorank
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the program with:
```bash
python src/main.py
```

When prompted, enter the path to your directory containing photos.

## How it Works

1. The program loads all images from the specified directory
2. Uses ResNet50 to extract features from each image
3. Groups similar images together using DBSCAN clustering
4. Displays groups of similar images

## Requirements

- Python 3.7+
- See requirements.txt for Python package dependencies 