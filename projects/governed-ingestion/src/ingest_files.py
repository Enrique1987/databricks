"""Bounded Auto Loader ingestion for the governed-ingestion portfolio project."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


SUPPORTED_FORMATS = frozenset({"json", "parquet"})
RESERVED_COLUMNS = (
    "_ingestion_source_file",
    "_ingestion_source_modified_at",
    "_ingestion_recorded_at",
    "_rescued_data",
)
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


@dataclass(frozen=True)
class IngestionConfig:
    """Validated inputs for one incremental ingestion stream."""

    source_path: str
    target_table: str
    checkpoint_path: str
    schema_path: str
    source_format: str = "json"
    max_files_per_trigger: int = 1000

    def validate(self) -> None:
        for field_name in ("source_path", "checkpoint_path", "schema_path"):
            value = getattr(self, field_name)
            if not value.startswith("/Volumes/"):
                raise ValueError(f"{field_name} must be an absolute Unity Catalog volume path")

        source_root = self.source_path.rstrip("/")
        for state_name in ("checkpoint_path", "schema_path"):
            state_path = getattr(self, state_name).rstrip("/")
            if state_path == source_root or state_path.startswith(f"{source_root}/"):
                raise ValueError(f"{state_name} must not be stored below source_path")

        if self.checkpoint_path.rstrip("/") == self.schema_path.rstrip("/"):
            raise ValueError("checkpoint_path and schema_path must be different")

        table_parts = self.target_table.split(".")
        if len(table_parts) != 3 or any(not _IDENTIFIER.fullmatch(part) for part in table_parts):
            raise ValueError("target_table must be a three-part Unity Catalog identifier")

        if self.source_format not in SUPPORTED_FORMATS:
            supported = ", ".join(sorted(SUPPORTED_FORMATS))
            raise ValueError(f"source_format must be one of: {supported}")

        if self.max_files_per_trigger < 1:
            raise ValueError("max_files_per_trigger must be greater than zero")

    def reader_options(self) -> Mapping[str, str]:
        """Return the explicit Auto Loader state and drift policy."""

        self.validate()
        return {
            "cloudFiles.format": self.source_format,
            "cloudFiles.schemaLocation": self.schema_path,
            "cloudFiles.schemaEvolutionMode": "rescue",
            "cloudFiles.maxFilesPerTrigger": str(self.max_files_per_trigger),
            "rescuedDataColumn": "_rescued_data",
        }


def run_ingestion(
    spark: Any,
    config: IngestionConfig,
    *,
    functions: Any | None = None,
) -> Any:
    """Run one AvailableNow cycle and return the terminated query handle."""

    config.validate()

    if functions is None:
        from pyspark.sql import functions as spark_functions

        functions = spark_functions

    reader = spark.readStream.format("cloudFiles")
    for option, value in config.reader_options().items():
        reader = reader.option(option, value)

    raw = reader.load(config.source_path)
    collisions = find_reserved_columns(raw.columns)
    if collisions:
        joined = ", ".join(collisions)
        raise ValueError(f"source contains reserved ingestion columns: {joined}")

    incoming = raw.select(
        "*",
        functions.col("_metadata.file_path").alias("_ingestion_source_file"),
        functions.col("_metadata.file_modification_time").alias(
            "_ingestion_source_modified_at"
        ),
        functions.current_timestamp().alias("_ingestion_recorded_at"),
    )

    query = (
        incoming.writeStream.option("checkpointLocation", config.checkpoint_path)
        .outputMode("append")
        .trigger(availableNow=True)
        .toTable(config.target_table)
    )
    query.awaitTermination()
    return query


def find_reserved_columns(columns: Sequence[str]) -> tuple[str, ...]:
    """Return reserved metadata names already present in a source schema."""

    return tuple(sorted(set(RESERVED_COLUMNS).intersection(columns)))


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
    from pyspark.sql import SparkSession

    run_ingestion(SparkSession.builder.getOrCreate(), config_from_args(arguments))


if __name__ == "__main__":
    main()
