"""Validated configuration for the governed ingestion pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping


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
        """Reject unsafe paths, identifiers, formats, and trigger limits."""

        for field_name in ("source_path", "checkpoint_path", "schema_path"):
            value = getattr(self, field_name)
            if not value.startswith("/Volumes/"):
                raise ValueError(
                    f"{field_name} must be an absolute Unity Catalog volume path"
                )

        source_root = self.source_path.rstrip("/")
        for state_name in ("checkpoint_path", "schema_path"):
            state_path = getattr(self, state_name).rstrip("/")
            if state_path == source_root or state_path.startswith(f"{source_root}/"):
                raise ValueError(f"{state_name} must not be stored below source_path")

        if self.checkpoint_path.rstrip("/") == self.schema_path.rstrip("/"):
            raise ValueError("checkpoint_path and schema_path must be different")

        table_parts = self.target_table.split(".")
        if len(table_parts) != 3 or any(
            not _IDENTIFIER.fullmatch(part) for part in table_parts
        ):
            raise ValueError("target_table must be a three-part Unity Catalog identifier")

        if self.source_format not in SUPPORTED_FORMATS:
            supported = ", ".join(sorted(SUPPORTED_FORMATS))
            raise ValueError(f"source_format must be one of: {supported}")

        if self.max_files_per_trigger < 1:
            raise ValueError("max_files_per_trigger must be greater than zero")

    def reader_options(self) -> Mapping[str, str]:
        """Return explicit Auto Loader state, drift, and workload options."""

        self.validate()
        return {
            "cloudFiles.format": self.source_format,
            "cloudFiles.schemaLocation": self.schema_path,
            "cloudFiles.schemaEvolutionMode": "rescue",
            "cloudFiles.maxFilesPerTrigger": str(self.max_files_per_trigger),
            "rescuedDataColumn": "_rescued_data",
        }
