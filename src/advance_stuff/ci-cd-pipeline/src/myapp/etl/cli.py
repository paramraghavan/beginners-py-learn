#!/usr/bin/env python3
"""
ETL Pipeline CLI

Command-line interface for running ETL pipelines.
Usage: python -m myapp.etl.cli --help
"""

import argparse
import json
import sys
from pathlib import Path

from myapp.etl.pipeline import (
    APIExtractor,
    CSVExtractor,
    CSVLoader,
    DataFormat,
    ETLPipeline,
    JSONExtractor,
    JSONLoader,
    JSONLLoader,
    PipelineConfig,
    Transformer,
    add_timestamp,
    clean_whitespace,
    convert_types,
    filter_fields,
    lowercase_keys,
    rename_fields,
    validate_required,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="ETL Pipeline - Extract, Transform, Load data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # CSV to JSON
  %(prog)s -i data.csv -o output.json --input-format csv

  # JSON to CSV with field filtering
  %(prog)s -i data.json -o output.csv --output-format csv --fields name,email,age

  # API to JSON Lines
  %(prog)s --api-url https://api.example.com/users -o users.jsonl --output-format jsonl

  # With type conversion
  %(prog)s -i data.json -o output.json --types '{"age": "int", "active": "bool"}'
        """,
    )

    # Input options
    input_group = parser.add_argument_group("Input")
    input_group.add_argument(
        "-i", "--input",
        type=str,
        help="Input file path",
    )
    input_group.add_argument(
        "--input-format",
        type=str,
        choices=["json", "csv", "jsonl"],
        default="json",
        help="Input file format (default: json)",
    )
    input_group.add_argument(
        "--api-url",
        type=str,
        help="API URL to extract data from",
    )
    input_group.add_argument(
        "--api-headers",
        type=str,
        help="API headers as JSON string",
    )
    input_group.add_argument(
        "--api-data-key",
        type=str,
        help="Key in API response containing data array",
    )

    # Output options
    output_group = parser.add_argument_group("Output")
    output_group.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="Output file path",
    )
    output_group.add_argument(
        "--output-format",
        type=str,
        choices=["json", "csv", "jsonl"],
        default="json",
        help="Output file format (default: json)",
    )

    # Transform options
    transform_group = parser.add_argument_group("Transformations")
    transform_group.add_argument(
        "--fields",
        type=str,
        help="Comma-separated list of fields to keep",
    )
    transform_group.add_argument(
        "--rename",
        type=str,
        help="Field rename mapping as JSON (e.g., '{\"old_name\": \"new_name\"}')",
    )
    transform_group.add_argument(
        "--types",
        type=str,
        help="Type conversions as JSON (e.g., '{\"age\": \"int\", \"active\": \"bool\"}')",
    )
    transform_group.add_argument(
        "--required",
        type=str,
        help="Comma-separated list of required fields (records missing these are dropped)",
    )
    transform_group.add_argument(
        "--no-timestamp",
        action="store_true",
        help="Don't add processing timestamp",
    )
    transform_group.add_argument(
        "--no-clean",
        action="store_true",
        help="Don't clean whitespace",
    )

    # Pipeline options
    pipeline_group = parser.add_argument_group("Pipeline")
    pipeline_group.add_argument(
        "--name",
        type=str,
        default="cli-pipeline",
        help="Pipeline name for logging",
    )
    pipeline_group.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Stop pipeline on first error",
    )
    pipeline_group.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )
    pipeline_group.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing",
    )

    return parser.parse_args()


def build_extractor(args: argparse.Namespace):
    """Build extractor from arguments."""
    if args.api_url:
        headers = {}
        if args.api_headers:
            headers = json.loads(args.api_headers)
        return APIExtractor(
            url=args.api_url,
            headers=headers,
            data_key=args.api_data_key,
        )
    elif args.input:
        input_path = Path(args.input)
        if args.input_format == "csv":
            return CSVExtractor(input_path)
        else:
            return JSONExtractor(input_path)
    else:
        raise ValueError("Either --input or --api-url must be provided")


def build_transformer(args: argparse.Namespace) -> Transformer:
    """Build transformer from arguments."""
    transformer = Transformer()

    # Clean whitespace
    if not args.no_clean:
        transformer.add(clean_whitespace)

    # Lowercase keys
    transformer.add(lowercase_keys)

    # Rename fields
    if args.rename:
        mapping = json.loads(args.rename)
        transformer.add(rename_fields(mapping))

    # Filter fields
    if args.fields:
        fields = [f.strip() for f in args.fields.split(",")]
        transformer.add(filter_fields(fields))

    # Validate required
    if args.required:
        required = [f.strip() for f in args.required.split(",")]
        transformer.add(validate_required(required))

    # Type conversions
    if args.types:
        type_mapping = json.loads(args.types)
        type_map = {}
        for field, type_name in type_mapping.items():
            if type_name == "int":
                type_map[field] = int
            elif type_name == "float":
                type_map[field] = float
            elif type_name == "bool":
                type_map[field] = bool
            elif type_name == "str":
                type_map[field] = str
        transformer.add(convert_types(type_map))

    # Add timestamp
    if not args.no_timestamp:
        transformer.add(add_timestamp("_processed_at"))

    return transformer


def build_loader(args: argparse.Namespace):
    """Build loader from arguments."""
    output_path = Path(args.output)

    if args.output_format == "csv":
        return CSVLoader(output_path)
    elif args.output_format == "jsonl":
        return JSONLLoader(output_path)
    else:
        return JSONLoader(output_path)


def main() -> int:
    """Main entry point."""
    args = parse_args()

    try:
        # Build pipeline components
        extractor = build_extractor(args)
        transformer = build_transformer(args)
        loader = build_loader(args)

        # Create pipeline
        config = PipelineConfig(
            name=args.name,
            fail_on_error=args.fail_on_error,
            log_level="DEBUG" if args.verbose else "INFO",
        )

        pipeline = (
            ETLPipeline(config)
            .extract_from(extractor)
            .transform_with(transformer)
            .load_to(loader)
        )

        if args.dry_run:
            print(f"Pipeline: {config.name}")
            print(f"  Extractor: {type(extractor).__name__}")
            print(f"  Transformer: {len(transformer._transformations)} operations")
            print(f"  Loader: {type(loader).__name__} -> {args.output}")
            print("\nDry run - no changes made")
            return 0

        # Run pipeline
        stats = pipeline.run()

        # Print summary
        print("\n" + "=" * 50)
        print("Pipeline Summary")
        print("=" * 50)
        print(f"  Records Extracted:   {stats.records_extracted}")
        print(f"  Records Transformed: {stats.records_transformed}")
        print(f"  Records Loaded:      {stats.records_loaded}")
        print(f"  Records Failed:      {stats.records_failed}")
        print(f"  Duration:            {stats.duration_seconds:.2f}s")
        print(f"  Success Rate:        {stats.success_rate:.1f}%")
        print("=" * 50)

        return 0 if stats.records_failed == 0 else 1

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
