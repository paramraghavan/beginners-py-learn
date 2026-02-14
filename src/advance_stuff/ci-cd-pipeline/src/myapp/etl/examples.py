#!/usr/bin/env python3
"""
Example ETL Pipelines

This script demonstrates various ETL pipeline configurations and use cases.
Run with: python -m myapp.etl.examples
"""

import sys
from pathlib import Path

from myapp.etl import (
    CSVExtractor,
    CSVLoader,
    ETLPipeline,
    InMemoryExtractor,
    InMemoryLoader,
    JSONExtractor,
    JSONLoader,
    JSONLLoader,
    PipelineConfig,
    Transformer,
    add_timestamp,
    clean_whitespace,
    compute_field,
    convert_types,
    filter_fields,
    filter_records,
    lowercase_keys,
    rename_fields,
    validate_required,
)


def example_json_to_csv():
    """Example: Transform JSON employee data to CSV."""
    print("\n" + "=" * 60)
    print("Example 1: JSON to CSV with field selection")
    print("=" * 60)

    # Define paths
    input_file = Path("data/sample_employees.json")
    output_file = Path("output/employees_summary.csv")

    if not input_file.exists():
        print(f"Skipping: {input_file} not found")
        return

    # Build transformer
    transformer = (
        Transformer()
        .add(clean_whitespace)
        .add(lowercase_keys)
        .add(rename_fields({
            "first_name": "name",
            "last_name": "surname",
        }))
        .add(convert_types({
            "id": int,
            "salary": int,
            "active": bool,
        }))
        .add(filter_records(lambda r: r.get("active") is True))
        .add(filter_fields(["id", "name", "surname", "email", "department", "salary"]))
        .add(compute_field("annual_bonus", lambda r: int(r.get("salary", 0) * 0.1)))
    )

    # Build and run pipeline
    pipeline = (
        ETLPipeline(PipelineConfig(name="json-to-csv"))
        .extract_from(JSONExtractor(input_file))
        .transform_with(transformer)
        .load_to(CSVLoader(output_file))
    )

    stats = pipeline.run()
    print(f"✅ Output: {output_file}")
    print(f"   Loaded {stats.records_loaded} active employees")


def example_csv_aggregation():
    """Example: Process orders CSV with aggregation."""
    print("\n" + "=" * 60)
    print("Example 2: CSV Order Processing with Calculations")
    print("=" * 60)

    input_file = Path("data/sample_orders.csv")
    output_file = Path("output/orders_enriched.json")

    if not input_file.exists():
        print(f"Skipping: {input_file} not found")
        return

    # Build transformer with computed fields
    transformer = (
        Transformer()
        .add(clean_whitespace)
        .add(lowercase_keys)
        .add(convert_types({
            "order_id": int,
            "quantity": int,
            "unit_price": float,
        }))
        .add(filter_records(lambda r: r.get("status") != "cancelled"))
        .add(compute_field(
            "total_amount",
            lambda r: round(r.get("quantity", 0) * r.get("unit_price", 0), 2)
        ))
        .add(compute_field(
            "is_large_order",
            lambda r: r.get("total_amount", 0) > 2000
        ))
        .add(add_timestamp("processed_at"))
    )

    # Build and run pipeline
    pipeline = (
        ETLPipeline(PipelineConfig(name="order-enrichment"))
        .extract_from(CSVExtractor(input_file))
        .transform_with(transformer)
        .load_to(JSONLoader(output_file))
    )

    stats = pipeline.run()
    print(f"✅ Output: {output_file}")
    print(f"   Processed {stats.records_loaded} orders")


def example_data_validation():
    """Example: Data validation and cleaning pipeline."""
    print("\n" + "=" * 60)
    print("Example 3: Data Validation Pipeline")
    print("=" * 60)

    # Sample messy data
    raw_data = [
        {"name": "  John Doe  ", "email": "john@example.com", "age": "25"},
        {"name": "Jane Smith", "email": "jane@example.com", "age": "30"},
        {"name": "", "email": "invalid@example.com", "age": "28"},  # Invalid: empty name
        {"name": "Bob Wilson", "email": "", "age": "35"},  # Invalid: empty email
        {"name": "Alice Brown", "email": "alice@example.com", "age": "invalid"},  # Invalid age
        {"name": "Charlie Davis", "email": "charlie@example.com", "age": "42"},
    ]

    # Build validation transformer
    transformer = (
        Transformer()
        .add(clean_whitespace)
        .add(lowercase_keys)
        .add(validate_required(["name", "email"]))  # Drop records missing name or email
        .add(convert_types({"age": int}))
        .add(filter_records(lambda r: isinstance(r.get("age"), int)))  # Drop invalid ages
        .add(compute_field("age_group", lambda r: "senior" if r.get("age", 0) >= 40 else "adult"))
        .add(add_timestamp())
    )

    # Use in-memory loader for demonstration
    loader = InMemoryLoader()

    # Build and run pipeline
    pipeline = (
        ETLPipeline(PipelineConfig(name="validation-pipeline"))
        .extract_from(InMemoryExtractor(raw_data))
        .transform_with(transformer)
        .load_to(loader)
    )

    stats = pipeline.run()

    print(f"✅ Input records:  {stats.records_extracted}")
    print(f"   Valid records:  {stats.records_loaded}")
    print(f"   Invalid/dropped: {stats.records_extracted - stats.records_loaded}")

    # Show cleaned data
    print("\nCleaned Data:")
    for record in loader.get_data():
        print(f"   - {record['name']} ({record['email']}): {record['age']} ({record['age_group']})")


def example_multi_output():
    """Example: Single input to multiple outputs."""
    print("\n" + "=" * 60)
    print("Example 4: Multi-format Output")
    print("=" * 60)

    # Sample data
    sample_data = [
        {"id": 1, "name": "Product A", "price": 19.99, "category": "electronics"},
        {"id": 2, "name": "Product B", "price": 29.99, "category": "clothing"},
        {"id": 3, "name": "Product C", "price": 9.99, "category": "electronics"},
        {"id": 4, "name": "Product D", "price": 49.99, "category": "home"},
        {"id": 5, "name": "Product E", "price": 14.99, "category": "clothing"},
    ]

    # Common transformer
    transformer = (
        Transformer()
        .add(lowercase_keys)
        .add(compute_field("price_tier", lambda r: "premium" if r.get("price", 0) > 25 else "standard"))
        .add(add_timestamp())
    )

    extractor = InMemoryExtractor(sample_data)
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # Output to multiple formats
    formats = [
        ("products.json", JSONLoader(output_dir / "products.json")),
        ("products.jsonl", JSONLLoader(output_dir / "products.jsonl")),
        ("products.csv", CSVLoader(output_dir / "products.csv")),
    ]

    for filename, loader in formats:
        pipeline = (
            ETLPipeline(PipelineConfig(name=f"multi-output-{filename}"))
            .extract_from(extractor)
            .transform_with(transformer)
            .load_to(loader)
        )
        stats = pipeline.run()
        print(f"✅ {filename}: {stats.records_loaded} records")


def example_department_split():
    """Example: Split data by department into separate files."""
    print("\n" + "=" * 60)
    print("Example 5: Split by Category")
    print("=" * 60)

    input_file = Path("data/sample_employees.json")

    if not input_file.exists():
        print(f"Skipping: {input_file} not found")
        return

    # First, extract all data
    extractor = JSONExtractor(input_file)
    all_records = extractor.extract()

    # Apply base transformations
    base_transformer = (
        Transformer()
        .add(clean_whitespace)
        .add(lowercase_keys)
        .add(convert_types({"salary": int, "active": bool}))
        .add(filter_records(lambda r: r.get("active") is True))
    )

    transformed = base_transformer.transform(all_records)

    # Group by department
    departments: dict[str, list] = {}
    for record in transformed:
        dept = record.get("department", "unknown")
        if dept not in departments:
            departments[dept] = []
        departments[dept].append(record)

    # Write each department to separate file
    output_dir = Path("output/by_department")
    output_dir.mkdir(parents=True, exist_ok=True)

    for dept, records in departments.items():
        output_file = output_dir / f"{dept.lower()}.json"
        loader = JSONLoader(output_file)
        loader.load(records)
        print(f"✅ {dept}: {len(records)} employees -> {output_file}")


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("    ETL PIPELINE EXAMPLES")
    print("=" * 60)

    # Create output directory
    Path("output").mkdir(exist_ok=True)

    # Run examples
    example_json_to_csv()
    example_csv_aggregation()
    example_data_validation()
    example_multi_output()
    example_department_split()

    print("\n" + "=" * 60)
    print("All examples completed!")
    print("Check the 'output/' directory for results.")
    print("=" * 60 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
