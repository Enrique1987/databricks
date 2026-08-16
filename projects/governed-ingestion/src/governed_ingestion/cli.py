"""Command-line contract for Databricks job parameters."""

from __future__ import annotations

import argparse
from typing import Sequence

from governed_ingestion.config import IngestionConfig
from governed_ingestion.pipeline import run_ingestion


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-path", required=True)
    parser.add_argument("--target-table", required=True)
    parser.add_argument("--checkpoint-path", required=True)
    parser.add_argument("--schema-path", required=True)
    parser.add_argument("--source-format", default="json")
    parser.add_argument("--max-files-per-trigger", type=int, default=1000)
    return parser


def config_from_args(arguments: Sequence[str] | None = None) -> IngestionConfig:
    args = build_parser().parse_args(arguments)
    config = IngestionConfig(
        source_path=args.source_path,
        target_table=args.target_table,
        checkpoint_path=args.checkpoint_path,
        schema_path=args.schema_path,
        source_format=args.source_format,
        max_files_per_trigger=args.max_files_per_trigger,
    )
    config.validate()
    return config


def main(arguments: Sequence[str] | None = None) -> None:
    """Resolve the active Spark session and execute the validated pipeline."""

    from pyspark.sql import SparkSession

    run_ingestion(SparkSession.builder.getOrCreate(), config_from_args(arguments))
