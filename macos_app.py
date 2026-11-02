#!/usr/bin/env python3
"""macOS app entry point; load the bundled printer configuration safely."""

import pickle
import sys
from pathlib import Path

from ui import EpsonPrinterUI


def bundled_resource(name: str) -> Path:
    """Return a resource path both in development and in a PyInstaller app."""
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent
    return base / name


def main() -> None:
    config_path = bundled_resource("epson_print_conf.pickle")
    with config_path.open("rb") as config_file:
        config = pickle.load(config_file)

    if not isinstance(config, dict):
        raise ValueError("Bundled printer configuration is not a dictionary")

    # The repository's sample config is for a different printer/IP. Keep the
    # validated XP-520 model data, but don't prefill another device's address.
    internal_data = config.setdefault("internal_data", {})
    if not isinstance(internal_data, dict):
        internal_data = {}
        config["internal_data"] = internal_data
    internal_data.pop("hostname", None)
    if "XP-520" in config:
        internal_data["default_model"] = "XP-520"

    app = EpsonPrinterUI(conf_dict=config)
    app.mainloop()


if __name__ == "__main__":
    main()
