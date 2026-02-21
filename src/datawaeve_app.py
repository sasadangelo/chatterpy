# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
import argparse
import sys
from argparse import ArgumentParser, Namespace

from core import LoggerManager, chatterpy_config, setup_logging
from datawaeve.datawaeve_cli import DataWeaveCLI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging first
setup_logging(
    level=chatterpy_config.datawave_log.level,
    console=chatterpy_config.datawave_log.console,
    file=chatterpy_config.datawave_log.file,
    rotation=chatterpy_config.datawave_log.rotation,
    retention=chatterpy_config.datawave_log.retention,
    compression=chatterpy_config.datawave_log.compression,
)

# Create a main logger
logger = LoggerManager.get_logger(name="main")


# This is the main entry point of the DataWeave command-line interface.
def main() -> None:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="DataWeave CLI: Populate a vector database with data coming from different sources."
    )
    parser.add_argument(
        "--pdf",
        type=str,
        action="append",
        required=False,
        help="Specify the path of a PDF file or a folder containing multiple PDF files.",
    )
    parser.add_argument(
        "--wikipedia", type=str, action="append", required=False, help="Specify the URL of a Wikipedia page."
    )

    args: Namespace = parser.parse_args()

    # Check if at least one source is provided
    if not args.pdf and not args.wikipedia:
        parser.print_help()
        return

    # Load data from all the supported data sources
    try:
        datawaeve_cli: DataWeaveCLI = DataWeaveCLI()
        datawaeve_cli.load_pdf_sources(pdf_paths=args.pdf) if args.pdf else []
        datawaeve_cli.load_wikipedia_sources(wikipedia_urls=args.wikipedia) if args.wikipedia else []
        datawaeve_cli.process_sources()
    except ConnectionError as e:
        logger.error(f"Connection error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
