"""Exercise each workflow with real paths and verify the scaffold preserves files."""

import json

import pytest

from scan2flow.cli import main


@pytest.mark.parametrize("command", ["photo", "video", "lidar", "train", "evaluate", "prepare-cfd"])
@pytest.mark.parametrize("dry_run", [True, False])
def test_workflows_do_not_read_or_modify_assets(command, dry_run, tmp_path, capsys):
    asset = tmp_path / "input with spaces.bin"
    asset.write_bytes(b"Intentionally not valid image, checkpoint, CAD, or TOML content.\x00")
    original = asset.read_bytes()
    output = tmp_path / "new output"
    if command in {"photo", "video", "lidar"}:
        arguments = [
            "reconstruct",
            "--input",
            str(asset),
            "--input-type",
            command,
            "--checkpoint",
            str(asset),
            "--output",
            str(output),
        ]
        if command == "lidar":
            arguments += ["--scan-units", "mm"]
        else:
            arguments += ["--input", str(tmp_path / "nonexistent-view"), "--known-length", "25"]
    elif command == "train":
        arguments = [
            "train",
            "--config",
            str(asset),
            "--resume",
            str(asset),
            "--output",
            str(output),
        ]
    elif command == "evaluate":
        arguments = [
            "evaluate",
            "--config",
            str(asset),
            "--checkpoint",
            str(asset),
            "--output",
            str(output),
        ]
    else:
        arguments = [
            "prepare-cfd",
            "--input",
            str(asset),
            "--output",
            str(output),
            "--domain",
            str(asset),
            "--flow",
            "external",
            "--units",
            "mm",
        ]

    if dry_run:
        arguments += ["--dry-run"]
    assert main(arguments) == (0 if dry_run else 3)
    captured = capsys.readouterr()
    if dry_run:
        plan = json.loads(captured.out)
        assert plan["backend"] == "unimplemented"
        assert captured.err == ""
    else:
        assert captured.out == ""
        assert "backend is not implemented" in captured.err
    assert not output.exists()
    assert asset.read_bytes() == original
    assert list(tmp_path.iterdir()) == [asset]
