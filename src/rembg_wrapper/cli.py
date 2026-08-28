"""Remove backgrounds from images using rembg.

Input       Output        Behavior
-------------------------------------------------------
file        omitted       Write <stem>.nobg.png next to the input file
file        file          Write to the specified output file
directory   omitted       Write .nobg.png files into the input directory
directory   directory     Write .nobg.png files into the output directory
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from .remover import ModelName, Remover

SUPPORTED_EXTENSIONS = frozenset(
    {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}
)
OUTPUT_SUFFIX = ".nobg.png"
console = Console()


@dataclass(frozen=True)
class RemovalJob:
    input_path: Path
    output_path: Path


def default_output_path(
    input_path: Path,
    output_dir: Path | None = None,
) -> Path:
    """Return the default output path for an input image."""
    output_dir = output_dir or input_path.parent
    return output_dir / f"{input_path.stem}{OUTPUT_SUFFIX}"


def resolve_jobs(
    input_path: Path,
    output_path: Path | None,
    supported_extensions: frozenset[str] = SUPPORTED_EXTENSIONS,
    output_suffix: str = OUTPUT_SUFFIX,
) -> list[RemovalJob]:
    """Resolve input/output paths into individual background removal jobs."""
    if input_path.is_file():
        if input_path.suffix.lower() not in supported_extensions:
            raise typer.BadParameter(f"Unsupported input format: {input_path.suffix}")

        if output_path is None:
            resolved_output = default_output_path(input_path)
        else:
            if output_path.exists() and output_path.is_dir():
                raise typer.BadParameter("Output must be a file when input is a file.")

            resolved_output = output_path

        return [RemovalJob(input_path, resolved_output)]

    if input_path.is_dir():
        if output_path is None:
            output_dir = input_path
        else:
            if output_path.exists() and not output_path.is_dir():
                raise typer.BadParameter(
                    "Output must be a directory when input is a directory."
                )

            output_dir = output_path

        input_files = sorted(
            path
            for path in input_path.iterdir()
            if (
                path.is_file()
                and path.suffix.lower() in supported_extensions
                and not path.name.lower().endswith(output_suffix)
            )
        )

        return [
            RemovalJob(
                input_file,
                default_output_path(input_file, output_dir),
            )
            for input_file in input_files
        ]

    raise typer.BadParameter(f"Input is neither a file nor a directory: {input_path}")


def should_overwrite(
    output_file: Path,
    overwrite: bool,
) -> bool:
    """Return whether an output file may be written."""
    if not output_file.exists():
        return True

    if overwrite:
        return True

    return typer.confirm(f"{output_file} already exists. Overwrite?")


def main(
    input_path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            readable=True,
            help="Image file or directory containing image files.",
        ),
    ],
    output_path: Annotated[
        Path | None,
        typer.Argument(
            help="Output image file or directory.",
        ),
    ] = None,
    model: Annotated[
        ModelName,
        typer.Option(
            "--model",
            "-m",
            help="Background removal model to use.",
        ),
    ] = ModelName.BRIA_RMBG,
    overwrite: Annotated[
        bool,
        typer.Option(
            "--overwrite",
            help="Overwrite existing output files without confirmation.",
        ),
    ] = False,
) -> None:
    """Remove backgrounds from images."""

    jobs = resolve_jobs(input_path, output_path)
    if not jobs:
        console.print("[yellow]No supported image files found.[/yellow]")
        raise typer.Exit()

    jobs = [job for job in jobs if should_overwrite(job.output_path, overwrite)]
    if not jobs:
        console.print("[yellow]No files to process.[/yellow]")
        raise typer.Exit()

    console.print(f"Background removal jobs: [bold cyan]{len(jobs)}[/bold cyan]")

    console.print(f"Loading model [bold cyan]{model.value}[/bold cyan] ...")
    remover = Remover(model_name=model)
    console.print(f"[green]✓[/green] Model loaded: [bold cyan]{model.value}[/bold cyan]")

    for job in jobs:
        job.output_path.parent.mkdir(parents=True, exist_ok=True)

        with console.status(
            f"Removing background from [bold cyan]{job.input_path}[/bold cyan] "
            f"→ [cyan]{job.output_path}[/cyan]",
            spinner="dots",
        ):
            remover.remove(job.input_path, job.output_path)

        console.print(
            f"[green]✓[/green] Background removed "
            f"[bold cyan]{job.input_path}[/bold cyan] "
            f"→ [cyan]{job.output_path}[/cyan]"
        )


def cli() -> None:
    app = typer.Typer(
        context_settings={
            "help_option_names": ["-h", "--help"],
        }
    )

    app.command()(main)
    app()


if __name__ == "__main__":
    cli()
