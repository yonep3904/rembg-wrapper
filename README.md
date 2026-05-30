# Rembg Wrapper

rembg(画像の背景を削除するツール) をラップして、画像ファイルの背景削除を CLI で簡単に行えるスクリプト。

## Installation

パッケージマネージャーとして [uv](https://docs.astral.sh/uv/) を使用しています。

```bash
# Clone the repository
git clone https://github.com/yonep3904/rembg-wrapper.git

# Navigate to the project directory
cd rembg-wrapper

# Install the required dependencies
uv sync

```

## Usage

```bash
# uv run main.py [input file or directory] [output directory]

# Remove background from a single image
uv run main.py ./image.jpg ./output

# Remove background from all images in a directory
uv run main.py ./image_directory ./output
```
