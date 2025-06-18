# Copyright (C) 2023 Salvatore D'Angelo
# Maintainer: Salvatore D'Angelo <sasadangelo@gmail.com>
#
# This file is part of the ChatterPy project maintained by Salvatore D'Angelo.
#
# SPDX-License-Identifier: MIT
"""
DataWeave CLI Application Module

This module contains the main functionality for the DataWeave CLI application.
It includes functions for loading configuration, processing data from various
sources, and setting up the command-line interface.

Functions:
- load_config: Loads and returns configuration data from a YAML file.
- main: Main entry point of the DataWeave command-line interface.

Usage:
This is the main application of the Datawaeve CLI. It is supposed you call
it with this command:

python3 datawaeve_app.py -c configg.yml
"""

import argparse
import yaml
from typing import Dict
from datawaeve.datawaeve_cli import DataWeaveCLI


def load_config(config_file: str) -> Dict:
    """
    Load a YAML configuration file.

    Args:
        config_file (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration data loaded from the file.
    """
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"[ERROR] Config file not found: {config_file}")
        exit(1)
    except yaml.YAMLError as e:
        print(f"[ERROR] Invalid YAML syntax: {e}")
        exit(1)


def main():
    """
    Main entry point of the DataWeave command-line interface.

    This function sets up the argument parser for the DataWeave CLI and
    defines the command-line arguments that can be used to populate a vector
    database with data coming from different sources.
    """
    parser = argparse.ArgumentParser(
        description=("DataWeave CLI: Populate a vector database with data coming from " "different sources.")
    )
    parser.add_argument("--config", "-c", type=str, required=True, help="Path to the config file")
    parser.add_argument(
        "--pdf",
        type=str,
        action="append",
        required=False,
        help=("Specify the path of a PDF file or a folder containing multiple " "PDF files."),
    )
    parser.add_argument(
        "--wikipedia",
        type=str,
        action="append",
        required=False,
        help="Specify the URL of a Wikipedia page.",
    )

    args = parser.parse_args()

    # Load the configuration file
    config = load_config(args.config)

    if not args.pdf and not args.wikipedia:
        print("[INFO] No data sources provided. Use --pdf or --wikipedia.")
        exit(0)

    # Load data from all the supported data sources
    datawaeve_cli = DataWeaveCLI(config)
    if args.pdf:
        datawaeve_cli.load_pdf_sources(args.pdf)
    if args.wikipedia:
        datawaeve_cli.load_wikipedia_sources(args.wikipedia)
    datawaeve_cli.process_sources()


if __name__ == "__main__":
    main()
