"""CLI validation tests; these do not claim to validate unimplemented geometry."""

import json
from importlib import metadata

import pytest

from scan2flow import __version__, cli


def reconstruction(modality: str = "photo") -> list[str]:
    arguments = [
        "reconstruct",
        "--input",
        "missing-input",
        "--input-type",
        modality,
        "--output",
        "missing-output",
    ]
    if modality == "lidar":
        arguments += ["--scan-units", "mm"]
    else:
        arguments += ["--known-length", "0.25"]
    return arguments


@pytest.mark.parametrize("modality", ["photo", "video", "lidar"])
def test_reconstruction_plan_defaults(modality, capsys):
    assert cli.main(reconstruction(modality) + ["--dry-run"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "planned"
    assert result["backend"] == "unimplemented"
    assert "no files" in result["validation"]
    options = result["options"]
    assert options["units"] == "m"
    assert options["device"] == "auto"
    assert options["model"] is None
    assert options["format"] == "both"
    assert options["voxel_size"] == 0.002
    assert options["tolerance"] == 0.0001
    assert options["frame_step"] == (30 if modality == "video" else None)
    assert options["max_frames"] == (300 if modality == "video" else None)


@pytest.mark.parametrize("flag", ["--known-length", "--voxel-size", "--tolerance"])
@pytest.mark.parametrize("value", ["0", "-1", "nan", "inf", "-inf", "1e999", "bad"])
def test_nonpositive_or_nonfinite_geometry_values_rejected(flag, value, capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(reconstruction() + [f"{flag}={value}", "--dry-run"])
    assert error.value.code == 2
    assert "finite positive number" in capsys.readouterr().err


@pytest.mark.parametrize("flag", ["--frame-step", "--max-frames"])
@pytest.mark.parametrize("value", ["0", "-1", "1.5", "nan", "inf"])
def test_invalid_video_counts_rejected(flag, value):
    with pytest.raises(SystemExit) as error:
        cli.main(reconstruction("video") + [f"{flag}={value}", "--dry-run"])
    assert error.value.code == 2


def test_explicit_video_settings_accepted(capsys):
    arguments = reconstruction("video") + [
        "--frame-step",
        "1",
        "--max-frames",
        "7",
        "--dry-run",
    ]
    assert cli.main(arguments) == 0
    options = json.loads(capsys.readouterr().out)["options"]
    assert (options["frame_step"], options["max_frames"]) == (1, 7)


def test_pretrained_model_override_is_optional_and_recorded(capsys):
    assert cli.main(reconstruction() + ["--model", "release-model", "--dry-run"]) == 0
    assert json.loads(capsys.readouterr().out)["options"]["model"] == "release-model"


@pytest.mark.parametrize("command", ["train", "evaluate"])
def test_developer_commands_are_not_public(command, capsys):
    with pytest.raises(SystemExit) as error:
        cli.main([command, "--help"])
    assert error.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


@pytest.mark.parametrize("flag", ["--checkpoint", "--seed", "--resume", "--config"])
def test_training_and_legacy_options_are_rejected(flag):
    with pytest.raises(SystemExit) as error:
        cli.main(reconstruction() + [flag, "1", "--dry-run"])
    assert error.value.code == 2


def test_public_help_only_lists_user_commands(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(["--help"])
    assert error.value.code == 0
    help_text = capsys.readouterr().out
    assert "{reconstruct,prepare-cfd,doctor}" in help_text
    assert "train" not in help_text
    assert "evaluate" not in help_text


@pytest.mark.parametrize("modality", ["photo", "lidar"])
@pytest.mark.parametrize("flag", ["--frame-step", "--max-frames"])
def test_explicit_video_flags_rejected_for_other_modalities(modality, flag):
    with pytest.raises(SystemExit) as error:
        cli.main(reconstruction(modality) + [flag, "30", "--dry-run"])
    assert error.value.code == 2


@pytest.mark.parametrize("modality", ["photo", "video"])
def test_photo_video_require_metric_anchor(modality):
    arguments = reconstruction(modality)
    index = arguments.index("--known-length")
    del arguments[index : index + 2]
    with pytest.raises(SystemExit) as error:
        cli.main(arguments + ["--dry-run"])
    assert error.value.code == 2


def test_lidar_requires_source_units():
    arguments = reconstruction("lidar")
    index = arguments.index("--scan-units")
    del arguments[index : index + 2]
    with pytest.raises(SystemExit) as error:
        cli.main(arguments + ["--dry-run"])
    assert error.value.code == 2


@pytest.mark.parametrize(
    ("modality", "extra"),
    [("photo", ["--scan-units", "m"]), ("lidar", ["--known-length", "1"])],
)
def test_scale_options_reject_wrong_modality(modality, extra):
    with pytest.raises(SystemExit) as error:
        cli.main(reconstruction(modality) + extra + ["--dry-run"])
    assert error.value.code == 2


@pytest.mark.parametrize("extra", [["--unknown"], ["--dev", "cpu"], ["--version"]])
def test_unknown_abbreviated_or_misplaced_global_options_rejected(extra):
    with pytest.raises(SystemExit) as error:
        cli.main(reconstruction() + extra)
    assert error.value.code == 2


@pytest.mark.parametrize("command", [[], ["prepare-cfd"], ["reconstruct"]])
def test_required_arguments_enforced(command):
    with pytest.raises(SystemExit) as error:
        cli.main(command)
    assert error.value.code == 2


@pytest.mark.parametrize("command", [[], ["reconstruct"], ["prepare-cfd"], ["doctor"]])
def test_help_is_available(command, capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(command + ["--help"])
    assert error.value.code == 0
    assert "usage:" in capsys.readouterr().out


def test_version(capsys):
    with pytest.raises(SystemExit) as error:
        cli.main(["--version"])
    assert error.value.code == 0
    assert capsys.readouterr().out.strip() == f"scan2flow {__version__}"


def test_doctor_reports_discovery_without_certifying_backends(monkeypatch, capsys):
    def version(name):
        if name == "torch":
            return "example-version"
        raise metadata.PackageNotFoundError(name)

    monkeypatch.setattr(cli.metadata, "version", version)
    monkeypatch.setattr(cli.shutil, "which", lambda name: None)
    assert cli.main(["doctor", "--json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "scaffold_available"
    assert report["backend"] == "unimplemented"
    assert report["optional_packages"] == {
        "torch": "example-version",
        "open3d": None,
        "cadquery": None,
    }
    assert report["executables"] == {"ffmpeg": None, "colmap": None}
    assert "no imports" in report["note"]


def test_keyboard_interrupt_has_conventional_exit_code(monkeypatch, capsys):
    def interrupted(_argv):
        raise KeyboardInterrupt

    monkeypatch.setattr(cli, "run", interrupted)
    assert cli.main(["doctor"]) == 130
    assert "interrupted" in capsys.readouterr().err
