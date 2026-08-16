"""Spark pipeline assembly kept separate from CLI and configuration concerns."""

from __future__ import annotations

from typing import Any, Sequence

from governed_ingestion.config import IngestionConfig, RESERVED_COLUMNS


def find_reserved_columns(columns: Sequence[str]) -> tuple[str, ...]:
    """Return reserved metadata names already present in a source schema."""

    return tuple(sorted(set(RESERVED_COLUMNS).intersection(columns)))


def add_ingestion_metadata(frame: Any, functions: Any) -> Any:
    """Project source rows with traceable ingestion metadata."""

    collisions = find_reserved_columns(frame.columns)
    if collisions:
        joined = ", ".join(collisions)
        raise ValueError(f"source contains reserved ingestion columns: {joined}")

    return frame.select(
        "*",
        functions.col("_metadata.file_path").alias("_ingestion_source_file"),
        functions.col("_metadata.file_modification_time").alias(
            "_ingestion_source_modified_at"
        ),
        functions.current_timestamp().alias("_ingestion_recorded_at"),
    )


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

    incoming = add_ingestion_metadata(reader.load(config.source_path), functions)
    query = (
        incoming.writeStream.option("checkpointLocation", config.checkpoint_path)
        .outputMode("append")
        .trigger(availableNow=True)
        .toTable(config.target_table)
    )
    query.awaitTermination()
    return query
