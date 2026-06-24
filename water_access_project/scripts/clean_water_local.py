#!/usr/bin/env python3
"""
Water Data Cleaning Script - Standalone Version
================================================
This script cleans the WHO/UNICEF JMP Estimates on the use of water dataset (2020)
Designed to run in any local environment.

Usage:
    python clean_water_local.py

The script will:
1. Look for the raw data file in the current directory or data/raw/
2. Clean the data by fixing separator issues
3. Save the cleaned version to data/cleaned/
"""

import os
import sys
from pathlib import Path

def find_data_file():
    """Find the raw data file in common locations"""
    possible_locations = [
        "Estimates-on-the-use-of-water-_2020_-a-3712.csv",
        "data/raw/Estimates-on-the-use-of-water-_2020_-a-3712.csv",
        "../data/raw/Estimates-on-the-use-of-water-_2020_-a-3712.csv",
        "water_data.csv",
        "data/raw/water_data.csv"
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            return location
    
    return None

def clean_water_data(input_file, output_file):
    """
    Clean the water access data by fixing separator issues
    
    Issues to fix:
    1. Header row uses semicolons instead of commas
    2. Five data rows have semicolons where commas should be
    """
    
    print("=" * 70)
    print("WATER DATA CLEANING SCRIPT")
    print("=" * 70)
    print()
    
    # Step 1: Read the file
    print("STEP 1: Reading the raw data file")
    print("-" * 70)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ ERROR: Could not find file: {input_file}")
        print("\nPlease ensure the data file is in one of these locations:")
        print("  - Current directory")
        print("  - data/raw/")
        sys.exit(1)
    
    print(f"✓ Successfully read {len(lines)} lines from: {input_file}")
    print()
    
    # Step 2: Identify problems
    print("STEP 2: Identifying problematic rows")
    print("-" * 70)
    
    problematic_lines = []
    
    # Check header
    if ';' in lines[0]:
        problematic_lines.append((1, "Header", lines[0].strip()[:80]))
    
    # Check data rows
    for i, line in enumerate(lines[1:], start=2):
        if ';' in line:
            country_name = line.split(',')[0] if ',' in line else "Unknown"
            problematic_lines.append((i, country_name, line.strip()[:80]))
    
    print(f"Found {len(problematic_lines)} problematic row(s):")
    for line_num, country, preview in problematic_lines:
        print(f"  Line {line_num:3d}: {country:30s} - {preview}...")
    print()
    
    # Step 3: Clean the data
    print("STEP 3: Cleaning the data")
    print("-" * 70)
    
    cleaned_lines = []
    for line in lines:
        # Replace all semicolons with commas
        cleaned_line = line.replace(';', ',')
        cleaned_lines.append(cleaned_line)
    
    print(f"✓ Cleaned {len(cleaned_lines)} lines")
    print()
    
    # Step 4: Save cleaned data
    print("STEP 4: Saving cleaned data")
    print("-" * 70)
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ Created directory: {output_dir}")
    
    try:
        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            f.writelines(cleaned_lines)
        print(f"✓ Cleaned data saved to: {output_file}")
    except Exception as e:
        print(f"❌ ERROR saving file: {e}")
        sys.exit(1)
    
    print()
    
    # Step 5: Verify the cleaned data
    print("STEP 5: Verifying cleaned data")
    print("-" * 70)
    
    try:
        import pandas as pd
        
        # Try to load the cleaned data
        df = pd.read_csv(output_file, na_values=['NAN'])
        
        print(f"✓ Successfully loaded cleaned CSV")
        print(f"✓ Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"✓ Expected: 16 columns, Got: {df.shape[1]} columns")
        
        if df.shape[1] == 16:
            print("✓ Column count is correct!")
        else:
            print(f"⚠ WARNING: Expected 16 columns but got {df.shape[1]}")
        
        print()
        print("Column names:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. {col}")
        
        print()
        print("First few rows:")
        print(df.head(3).to_string())
        
    except ImportError:
        print("⚠ pandas not installed - skipping verification")
        print("  Install pandas with: pip install pandas")
    except Exception as e:
        print(f"⚠ Verification error: {e}")
    
    print()
    print("=" * 70)
    print("✅ DATA CLEANING COMPLETE!")
    print("=" * 70)
    print()
    print("Summary:")
    print(f"  Input file:  {input_file}")
    print(f"  Output file: {output_file}")
    print(f"  Rows fixed:  {len(problematic_lines)}")
    print()
    print("Next steps:")
    print("  1. Import the cleaned CSV into Google Sheets")
    print("  2. Run the analysis script: python analyze_water_local.py")
    print()

def main():
    """Main function"""
    print()
    print("🌊 Water Access Data Cleaning Script")
    print()
    
    # Find input file
    input_file = find_data_file()
    
    if input_file is None:
        print("❌ ERROR: Could not find the raw data file!")
        print()
        print("Please ensure you have the file:")
        print("  'Estimates-on-the-use-of-water-_2020_-a-3712.csv'")
        print()
        print("In one of these locations:")
        print("  - Current directory")
        print("  - data/raw/")
        print()
        sys.exit(1)
    
    # Set output file
    output_file = "data/cleaned/water_data_cleaned.csv"
    
    # Clean the data
    clean_water_data(input_file, output_file)

if __name__ == "__main__":
    main()
