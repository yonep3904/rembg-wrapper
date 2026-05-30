from rembg import remove
from PIL import Image
from pathlib import Path
from argparse import ArgumentParser
from collections import Counter


def main():
    io_pairs = argument_parser()

    for input_file, output_file in io_pairs:
        remove_background(input_file, output_file)


def argument_parser() -> list[tuple[Path, Path]]:
    arg_parser = ArgumentParser(description="Remove background from images")
    arg_parser.add_argument(
        "input",
        type=str,
        help="Path to the input image file or directory containing image files",
    )
    arg_parser.add_argument(
        "output",
        type=str,
        help="Path to save directory to save images with removed background",
    )

    args = arg_parser.parse_args()

    # input
    input_path = Path(args.input)
    if not input_path.exists():
        raise ValueError("Input path does not exist.")
    if input_path.is_file() and input_path.suffix not in [".jpg", ".jpeg", ".png"]:
        raise ValueError(
            "Input file must be an image file with .jpg, .jpeg, or .png extension."
        )
    if input_path.is_dir() and not any(
        file.suffix in [".jpg", ".jpeg", ".png"] for file in input_path.glob("*")
    ):
        raise ValueError(
            "Input directory must contain at least one image file with .jpg, .jpeg, or .png extension."
        )

    input_files: list[Path]

    if input_path.is_file():
        input_files = [input_path]
    else:
        input_files = [
            file
            for file in input_path.glob("*")
            if file.suffix in [".jpg", ".jpeg", ".png"]
        ]

    # output
    output_path = Path(args.output)
    output_dir = (
        output_path if output_path and output_path.is_dir() else input_path.parent
    )

    counter = Counter(file.stem for file in input_files)
    output_files = [
        output_dir / f"{file.stem}{file.suffix if counter[file.stem] > 1 else ''}.txt"
        for file in input_files
    ]

    return list(zip(input_files, output_files))


def remove_background(input_path: Path, output_path: Path) -> None:
    # Load the image
    input_image = Image.open(input_path)

    # Remove the background
    output_image = remove(input_image)

    # Save the output image
    output_image.save(output_path)  # type: ignore


if __name__ == "__main__":
    main()
