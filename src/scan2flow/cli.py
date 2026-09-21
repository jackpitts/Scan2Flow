"""Parse and inspect proposed workflows without claiming backend execution."""

from __future__ import annotations

import argparse
import json
import math
import platform
import shutil
import sys
from collections.abc import Sequence
from importlib import metadata

from scan2flow import __version__

UNITS = ("m", "cm", "mm")
DEVICES = ("auto", "cpu", "cuda")
DRY_RUN_SCOPE = (
    "CLI syntax and cross-option constraints only; "
    "no files, configuration contents, or environment checked."
)


def positive_float(value: str) -> float:
    """Accept a finite number strictly greater than zero."""
    try:
        number = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a finite positive number") from error
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("must be a finite positive number")
    return number


def positive_int(value: str) -> int:
    """Accept a strictly positive integer."""
    number = nonnegative_int(value)
    if number == 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def nonnegative_int(value: str) -> int:
    """Accept an integer greater than or equal to zero."""
    try:
        number = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a nonnegative integer") from error
    if number < 0:
        raise argparse.ArgumentTypeError("must be a nonnegative integer")
    return number


def add_device(parser: argparse.ArgumentParser) -> None:
    """Add the shared compute-device option."""
    parser.add_argument("--device", choices=DEVICES, default="auto", help="compute device")


def add_seed(parser: argparse.ArgumentParser) -> None:
    """Add the shared deterministic-seed request."""
    parser.add_argument("--seed", type=nonnegative_int, default=42, help="nonnegative random seed")


def add_dry_run(parser: argparse.ArgumentParser) -> None:
    """Add a side-effect-free JSON planning option."""
    parser.add_argument(
        "--dry-run", action="store_true", help="print a JSON plan; do not inspect or create files"
    )


def build_parser() -> argparse.ArgumentParser:
    """Build the public CLI contract using only the Python standard library."""
    parser = argparse.ArgumentParser(
        prog="scan2flow",
        description="Scan2Flow: CLI scaffold for scan-to-CAD and CFD preparation.",
        epilog="ML, CAD, and CFD backends are unimplemented. Use --dry-run to inspect a plan.",
        allow_abbrev=False,
    )
    parser.add_argument("--version", action="version", version=f"scan2flow {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    reconstruct = commands.add_parser(
        "reconstruct",
        help="plan object reconstruction from photos, videos, or LiDAR",
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    reconstruct.add_argument(
        "--input",
        action="append",
        required=True,
        metavar="PATH",
        help="input file; repeat for views of the same object",
    )
    reconstruct.add_argument("--input-type", choices=("photo", "video", "lidar"), required=True)
    reconstruct.add_argument("--output", required=True, metavar="PATH", help="output directory")
    reconstruct.add_argument("--checkpoint", required=True, metavar="PATH", help="model checkpoint")
    reconstruct.add_argument("--calibration", metavar="PATH", help="camera/sensor calibration file")
    reconstruct.add_argument(
        "--units", choices=UNITS, default="m", help="output CAD and --known-length units"
    )
    reconstruct.add_argument(
        "--known-length",
        type=positive_float,
        metavar="NUMBER",
        help="approximate longest oriented-bounding-box side; required for photo/video",
    )
    reconstruct.add_argument(
        "--scan-units", choices=UNITS, help="source coordinate units; required for LiDAR only"
    )
    reconstruct.add_argument(
        "--frame-step",
        type=positive_int,
        metavar="N",
        help="video only: sample every Nth frame (video default: 30)",
    )
    reconstruct.add_argument(
        "--max-frames",
        type=positive_int,
        metavar="N",
        help="video only: maximum retained frames across all input videos (video default: 300)",
    )
    reconstruct.add_argument(
        "--voxel-size",
        type=positive_float,
        default=0.002,
        metavar="METRES",
        help="point-cloud downsampling voxel size in metres",
    )
    reconstruct.add_argument(
        "--tolerance",
        type=positive_float,
        default=0.0001,
        metavar="METRES",
        help="requested geometry tolerance in metres; not an accuracy guarantee",
    )
    reconstruct.add_argument("--format", choices=("step", "stl", "both"), default="both")
    add_device(reconstruct)
    add_seed(reconstruct)
    add_dry_run(reconstruct)

    train = commands.add_parser(
        "train",
        help="plan ML model training",
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    train.add_argument(
        "--config", required=True, metavar="PATH", help="training TOML configuration"
    )
    train.add_argument("--output", required=True, metavar="PATH", help="training run directory")
    train.add_argument("--resume", metavar="PATH", help="checkpoint from which to resume")
    add_device(train)
    add_seed(train)
    add_dry_run(train)

    evaluate = commands.add_parser(
        "evaluate",
        help="plan evaluation of a checkpoint",
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    evaluate.add_argument(
        "--config", required=True, metavar="PATH", help="evaluation TOML configuration"
    )
    evaluate.add_argument("--checkpoint", required=True, metavar="PATH", help="model checkpoint")
    evaluate.add_argument("--split", choices=("validation", "test"), default="test")
    evaluate.add_argument(
        "--output", required=True, metavar="PATH", help="evaluation report directory"
    )
    add_device(evaluate)
    add_dry_run(evaluate)

    cfd = commands.add_parser(
        "prepare-cfd",
        help="plan fluid-domain preparation from reconstructed geometry",
        allow_abbrev=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    cfd.add_argument("--input", required=True, metavar="PATH", help="source CAD or surface mesh")
    cfd.add_argument("--output", required=True, metavar="PATH", help="prepared-domain directory")
    cfd.add_argument("--flow", choices=("external", "internal"), required=True)
    cfd.add_argument(
        "--units", choices=UNITS, required=True, help="source geometry coordinate units"
    )
    cfd.add_argument(
        "--tolerance",
        type=positive_float,
        default=0.0001,
        metavar="METRES",
        help="requested geometry tolerance in metres; not an accuracy guarantee",
    )
    cfd.add_argument(
        "--domain",
        required=True,
        metavar="PATH",
        help="TOML domain extent or inlet/outlet cap settings",
    )
    add_dry_run(cfd)

    doctor = commands.add_parser(
        "doctor",
        help="report scaffold environment; does not certify backend readiness",
        allow_abbrev=False,
    )
    doctor.add_argument("--json", action="store_true", help="print the environment report as JSON")
    return parser


def validate_options(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    """Reject incompatible reconstruction flags before planning or execution."""
    if args.command != "reconstruct":
        return
    if args.input_type == "lidar":
        if args.scan_units is None:
            parser.error("reconstruct --input-type lidar requires --scan-units")
        if args.known_length is not None:
            parser.error("--known-length is only supported for photo/video input")
    else:
        if args.known_length is None:
            parser.error("photo/video reconstruction requires --known-length in --units")
        if args.scan_units is not None:
            parser.error("--scan-units is only supported for lidar input")

    if args.input_type != "video":
        if args.frame_step is not None or args.max_frames is not None:
            parser.error("--frame-step and --max-frames are only supported for video input")
    else:
        if args.frame_step is None:
            args.frame_step = 30
        if args.max_frames is None:
            args.max_frames = 300


def environment_report() -> dict[str, object]:
    """Report executable paths and distribution metadata without importing ML packages."""
    optional_packages: dict[str, str | None] = {}
    for package in ("torch", "open3d", "cadquery"):
        try:
            optional_packages[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            optional_packages[package] = None
    return {
        "status": "scaffold_available",
        "backend": "unimplemented",
        "version": __version__,
        "python": {"version": platform.python_version(), "executable": sys.executable},
        "executables": {name: shutil.which(name) for name in ("ffmpeg", "colmap")},
        "optional_packages": optional_packages,
        "note": "Discovery only: no imports, GPU checks, or backend compatibility validation.",
    }


def run(argv: Sequence[str] | None = None) -> int:
    """Execute only implemented scaffold operations."""
    parser = build_parser()
    args = parser.parse_args(argv)
    validate_options(parser, args)

    if args.command == "doctor":
        report = environment_report()
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"Scan2Flow {__version__}: scaffold available; backends unimplemented.")
            print(f"Python: {platform.python_version()} ({sys.executable})")
            for group in ("executables", "optional_packages"):
                for name, value in report[group].items():
                    print(f"{name}: {value if value is not None else 'not found'}")
            print(report["note"])
        return 0

    if args.dry_run:
        options = {
            key: value for key, value in vars(args).items() if key not in {"command", "dry_run"}
        }
        print(
            json.dumps(
                {
                    "status": "planned",
                    "backend": "unimplemented",
                    "command": args.command,
                    "options": options,
                    "validation": DRY_RUN_SCOPE,
                },
                indent=2,
                allow_nan=False,
            )
        )
        return 0

    print(
        f"scan2flow: '{args.command}' backend is not implemented in this scaffold. "
        "No input files were read and no output files were created. "
        "Use --dry-run to inspect a command plan.",
        file=sys.stderr,
    )
    return 3


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point with a conventional interrupted-command exit code."""
    try:
        return run(argv)
    except KeyboardInterrupt:
        print("scan2flow: interrupted", file=sys.stderr)
        return 130
