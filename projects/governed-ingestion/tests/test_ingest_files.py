from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, call


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from governed_ingestion import IngestionConfig, find_reserved_columns, run_ingestion  # noqa: E402
from governed_ingestion.cli import config_from_args  # noqa: E402
from governed_ingestion.pipeline import add_ingestion_metadata  # noqa: E402


def valid_config(**overrides: object) -> IngestionConfig:
    values: dict[str, object] = {
        "source_path": "/Volumes/main/governed_ingestion_dev/landing/orders",
        "target_table": "main.governed_ingestion_dev.orders_raw",
        "checkpoint_path": "/Volumes/main/governed_ingestion_dev/operations/checkpoint",
        "schema_path": "/Volumes/main/governed_ingestion_dev/operations/schema",
        "source_format": "json",
        "max_files_per_trigger": 1000,
    }
    values.update(overrides)
    return IngestionConfig(**values)  # type: ignore[arg-type]


class PackageContractTests(unittest.TestCase):
    def test_wheel_metadata_matches_databricks_task_contract(self) -> None:
        metadata = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        job = (PROJECT_ROOT / "resources" / "ingestion.job.yml").read_text(
            encoding="utf-8"
        )

        self.assertIn('name = "governed_ingestion"', metadata)
        self.assertIn(
            'main = "governed_ingestion.cli:main"',
            metadata,
        )
        self.assertIn("package_name: governed_ingestion", job)
        self.assertIn("dependencies:\n              - ../dist/*.whl", job)


class IngestionConfigTests(unittest.TestCase):
    def test_reader_options_make_state_and_drift_policy_explicit(self) -> None:
        options = valid_config().reader_options()

        self.assertEqual(options["cloudFiles.schemaEvolutionMode"], "rescue")
        self.assertEqual(options["rescuedDataColumn"], "_rescued_data")
        self.assertEqual(options["cloudFiles.maxFilesPerTrigger"], "1000")

    def test_rejects_non_volume_paths(self) -> None:
        with self.assertRaisesRegex(ValueError, "absolute Unity Catalog volume path"):
            valid_config(source_path="s3://unmanaged-bucket/orders").validate()

    def test_rejects_checkpoint_below_source(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be stored below source_path"):
            valid_config(
                checkpoint_path=(
                    "/Volumes/main/governed_ingestion_dev/landing/orders/_checkpoint"
                )
            ).validate()

    def test_rejects_shared_checkpoint_and_schema_path(self) -> None:
        state_path = "/Volumes/main/governed_ingestion_dev/operations/state"
        with self.assertRaisesRegex(ValueError, "must be different"):
            valid_config(checkpoint_path=state_path, schema_path=state_path).validate()

    def test_rejects_invalid_table_identifier(self) -> None:
        with self.assertRaisesRegex(ValueError, "three-part Unity Catalog identifier"):
            valid_config(target_table="main.orders_raw").validate()

    def test_rejects_unsupported_source_format(self) -> None:
        with self.assertRaisesRegex(ValueError, "source_format must be one of"):
            valid_config(source_format="xml").validate()

    def test_rejects_non_positive_file_limit(self) -> None:
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            valid_config(max_files_per_trigger=0).validate()

    def test_cli_arguments_create_a_valid_config(self) -> None:
        config = config_from_args(
            [
                "--source-path",
                "/Volumes/main/governed_ingestion_dev/landing/orders",
                "--target-table",
                "main.governed_ingestion_dev.orders_raw",
                "--checkpoint-path",
                "/Volumes/main/governed_ingestion_dev/operations/checkpoint",
                "--schema-path",
                "/Volumes/main/governed_ingestion_dev/operations/schema",
                "--source-format",
                "parquet",
                "--max-files-per-trigger",
                "25",
            ]
        )

        self.assertEqual(config.source_format, "parquet")
        self.assertEqual(config.max_files_per_trigger, 25)

    def test_reserved_source_columns_are_detected(self) -> None:
        collisions = find_reserved_columns(
            ["order_id", "_rescued_data", "_ingestion_recorded_at"]
        )

        self.assertEqual(
            collisions,
            ("_ingestion_recorded_at", "_rescued_data"),
        )

    def test_metadata_projection_rejects_source_collision(self) -> None:
        frame = MagicMock()
        frame.columns = ["order_id", "_ingestion_source_file"]

        with self.assertRaisesRegex(ValueError, "reserved ingestion columns"):
            add_ingestion_metadata(frame, MagicMock())

        frame.select.assert_not_called()

    def test_run_uses_bounded_append_with_durable_checkpoint(self) -> None:
        reader = MagicMock()
        reader.format.return_value = reader
        reader.option.return_value = reader

        raw = MagicMock()
        raw.columns = ["order_id"]
        incoming = MagicMock()
        raw.select.return_value = incoming
        reader.load.return_value = raw

        writer = MagicMock()
        writer.option.return_value = writer
        writer.outputMode.return_value = writer
        writer.trigger.return_value = writer
        incoming.writeStream = writer

        query = MagicMock()
        writer.toTable.return_value = query

        spark = SimpleNamespace(readStream=reader)
        functions = MagicMock()
        functions.col.return_value.alias.return_value = MagicMock()
        functions.current_timestamp.return_value.alias.return_value = MagicMock()

        config = valid_config(max_files_per_trigger=25)
        result = run_ingestion(spark, config, functions=functions)

        self.assertIs(result, query)
        reader.format.assert_called_once_with("cloudFiles")
        reader.load.assert_called_once_with(config.source_path)
        self.assertIn(
            call("cloudFiles.schemaEvolutionMode", "rescue"),
            reader.option.call_args_list,
        )
        writer.option.assert_called_once_with(
            "checkpointLocation",
            config.checkpoint_path,
        )
        writer.outputMode.assert_called_once_with("append")
        writer.trigger.assert_called_once_with(availableNow=True)
        writer.toTable.assert_called_once_with(config.target_table)
        query.awaitTermination.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
