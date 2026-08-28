# rembg-wrapper

A simple CLI wrapper for rembg

rembg-wrapper provides the `rembgwrap` command for removing backgrounds from image files using rembg.

## Features

- Remove backgrounds from common image formats
- Batch-process all supported images in a directory
- Choose a rembg model with `--model`
- Reuse the loaded model when processing multiple images
- Confirm before overwriting existing files
- Automatically write transparent output as `.nobg.png` when the output is omitted

## Requirements

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)

## Installation

The recommended way to install rembg-wrapper is with `uv tool`.

```bash id="rgbr1a"
uv tool install git+https://github.com/yonep3904/rembg-wrapper.git
```


If the installed command is not available in your shell, run:

```bash id="rgbr2b"
uv tool update-shell
```

and restart your shell.

To upgrade rembg-wrapper:

```bash id="rgbr3c"
uv tool upgrade rembg-wrapper
```

To uninstall it:

```bash id="rgbr4d"
uv tool uninstall rembg-wrapper
```

## Usage

Remove the background from an image:

```bash id="rgbr5e"
rembgwrap photo.jpg
```

This creates:

```text id="rgbr6f"
photo.nobg.png
```

The default output name always ends in `.nobg.png`, regardless of the input format:

```text id="rgbr7g"
photo.jpg   → photo.nobg.png
photo.png   → photo.nobg.png
photo.webp  → photo.nobg.png
```

Specify the output file explicitly:

```bash id="rgbr8h"
rembgwrap photo.jpg result.png
```

When an output file is specified explicitly, its name is preserved.

Choose a model:

```bash id="rgbr9i"
rembgwrap photo.jpg --model birefnet-general
```

or:

```bash id="rgb10j"
rembgwrap photo.jpg -m u2net
```

Process all supported images in a directory:

```bash id="rgb11k"
rembgwrap images/
```

The resulting `.nobg.png` files are written into the same directory.

Files already ending in `.nobg.png` are excluded when processing a directory, preventing generated files from being processed again.

Specify a separate output directory:

```bash id="rgb12l"
rembgwrap images/ output/
```

Existing output files require confirmation before they are overwritten. To overwrite them without confirmation:

```bash id="rgb13m"
rembgwrap images/ output/ --overwrite
```

Show all available options:

```bash id="rgb14n"
rembgwrap -h
```

## Input and output behavior

| Input     | Output    | Behavior                                          |
| --------- | --------- | ------------------------------------------------- |
| File      | Omitted   | Write `<stem>.nobg.png` next to the input file    |
| File      | File      | Write to the specified output file                |
| Directory | Omitted   | Write `.nobg.png` files into the input directory  |
| Directory | Directory | Write `.nobg.png` files into the output directory |

Supported input formats are:

```text id="rgb15o"
.jpg  .jpeg  .png  .webp  .bmp  .tiff  .tif
```

## Models

rembg-wrapper supports the local models provided by rembg, including:

```text id="rgb16p"
u2net
u2netp
u2net_human_seg
u2net_cloth_seg
silueta
isnet-general-use
isnet-anime
sam
birefnet-general
birefnet-general-lite
birefnet-portrait
birefnet-dis
birefnet-hrsod
birefnet-cod
birefnet-massive
bria-rmbg
```

Model files are downloaded automatically by rembg on first use. Depending on the selected model, the initial download may be large and take some time.

Different models are optimized for different subjects and workloads. See the rembg documentation for details about each model.

## Development

Clone the repository and synchronize the development environment:

```bash id="rgb17q"
git clone https://github.com/yonep3904/rembg-wrapper.git
cd rembg-wrapper
uv sync
```

Run the CLI without installing it globally:

```bash id="rgb18r"
uv run rembgwrap -h
```

Run Ruff:

```bash id="rgb19s"
uv run ruff check .
```

Format the source code:

```bash id="rgb20t"
uv run ruff format .
```

## License

rembg-wrapper is released under the MIT License.

This project uses [rembg](https://github.com/danielgatis/rembg), which is also distributed under the MIT License.

The machine-learning models used by rembg are separate works and may be distributed under different licenses. Model weights are downloaded by rembg on first use and are not included in rembg-wrapper.

In particular, the `bria-rmbg` model (BRIA RMBG-2.0) is licensed under CC BY-NC 4.0 for non-commercial use. Commercial use requires a separate agreement with BRIA.

Before using a model, especially for commercial purposes, check the license and terms of the corresponding model.
