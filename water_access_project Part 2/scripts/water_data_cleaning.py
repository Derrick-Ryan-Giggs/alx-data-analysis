"""
Water Access Data Cleaning and Transformation Script
=====================================================
This script cleans and transforms water access data (2000-2020) and regional data.

Author: ALX Data Analysis Project
Date: February 2026

Folder Structure:
- scripts/            (this file)
- cleaned_data/       (all output CSV files)
- visualizations/     (plots from analysis script)
- reports/            (text reports)
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options for better readability
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# ============================================================================
# CREATE FOLDER STRUCTURE
# ============================================================================
print("=" * 80)
print("WATER ACCESS DATA CLEANING AND TRANSFORMATION")
print("=" * 80)
print(f"Script executed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Create necessary folders
folders = ['cleaned_data', 'visualizations', 'reports']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"✓ Created folder: {folder}/")
    else:
        print(f"✓ Folder exists: {folder}/")

print("\n")

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("1. LOADING DATA...")
print("-" * 80)

try:
    # Load the main water access dataset (with space in filename)
    water_df = pd.read_csv('Estimates of the use of water (2000-2020).csv')
    print(f"✓ Water access data loaded: {water_df.shape[0]} rows, {water_df.shape[1]} columns")
    
    # Load the regions dataset
    regions_df = pd.read_csv('Regions.csv')
    print(f"✓ Regions data loaded: {regions_df.shape[0]} rows, {regions_df.shape[1]} columns")
    
except FileNotFoundError as e:
    print(f"✗ Error: Could not find file - {e}")
    print("\nPlease ensure both CSV files are in the current directory:")
    print("  - Estimates of the use of water (2000-2020).csv")
    print("  - Regions.csv")
    exit(1)

print("\n")

# ============================================================================
# 2. EXPLORE DATA STRUCTURE
# ============================================================================
print("2. EXPLORING DATA STRUCTURE...")
print("-" * 80)

print("\nWater Access Dataset - First 5 rows:")
print(water_df.head())

print("\n\nWater Access Dataset - Column Info:")
print(f"Total columns: {len(water_df.columns)}")
print(f"Columns: {list(water_df.columns)}")

print("\n\nData types:")
print(water_df.dtypes)

print("\n\nBasic statistics:")
print(water_df.describe())

print("\n\nRegions Dataset - First 5 rows:")
print(regions_df.head())

print("\n\nUnique regions:")
print(regions_df['region'].value_counts())

# ============================================================================
# 3. DATA CLEANING - WATER ACCESS DATASET
# ============================================================================
print("\n\n3. CLEANING WATER ACCESS DATASET...")
print("-" * 80)

# Create a copy for cleaning
water_clean = water_df.copy()

# 3.1 Handle 'null' strings (convert to actual NaN)
print("\n3.1 Converting 'null' strings to NaN...")
water_clean = water_clean.replace('null', np.nan)
print(f"✓ Converted 'null' strings to NaN")

# 3.2 Convert data types
print("\n3.2 Converting data types...")
# Columns that should be numeric
numeric_cols = [col for col in water_clean.columns if col not in ['name', 'year']]

for col in numeric_cols:
    water_clean[col] = pd.to_numeric(water_clean[col], errors='coerce')

print(f"✓ Converted {len(numeric_cols)} columns to numeric type")

# Ensure year is integer
water_clean['year'] = water_clean['year'].astype(int)

# 3.3 Check for missing values
print("\n3.3 Missing values analysis:")
missing_summary = pd.DataFrame({
    'Column': water_clean.columns,
    'Missing_Count': water_clean.isnull().sum().values,
    'Missing_Percentage': (water_clean.isnull().sum().values / len(water_clean) * 100).round(2)
})
missing_summary = missing_summary[missing_summary['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
if len(missing_summary) > 0:
    print(missing_summary.to_string(index=False))
else:
    print("No missing values found!")

# 3.4 Check for duplicates
print("\n3.4 Checking for duplicates...")
duplicates = water_clean.duplicated(subset=['name', 'year']).sum()
print(f"Number of duplicate country-year combinations: {duplicates}")

if duplicates > 0:
    print("Removing duplicates...")
    water_clean = water_clean.drop_duplicates(subset=['name', 'year'], keep='first')
    print(f"✓ Removed {duplicates} duplicate rows")

# 3.5 Year validation
print("\n3.5 Validating years...")
print(f"Year range: {water_clean['year'].min()} to {water_clean['year'].max()}")
print(f"Unique years: {sorted(water_clean['year'].unique())}")

# ============================================================================
# 4. DATA CLEANING - REGIONS DATASET
# ============================================================================
print("\n\n4. CLEANING REGIONS DATASET...")
print("-" * 80)

regions_clean = regions_df.copy()

# 4.1 Check for missing values
print("\n4.1 Missing values in regions dataset:")
regions_missing = regions_clean.isnull().sum()
if regions_missing.sum() > 0:
    print(regions_missing)
else:
    print("✓ No missing values in regions dataset")

# 4.2 Check for duplicates
print("\n4.2 Checking for duplicate countries...")
duplicates_regions = regions_clean.duplicated(subset=['name']).sum()
print(f"Number of duplicate countries: {duplicates_regions}")

if duplicates_regions > 0:
    print("Removing duplicates...")
    regions_clean = regions_clean.drop_duplicates(subset=['name'], keep='first')
    print(f"✓ Removed {duplicates_regions} duplicate countries")

# 4.3 Show unique regions
print("\n4.3 Unique regions and country count:")
unique_regions = regions_clean['region'].value_counts().sort_values(ascending=False)
print(unique_regions)

# ============================================================================
# 5. MERGE DATASETS
# ============================================================================
print("\n\n5. MERGING DATASETS...")
print("-" * 80)

# Merge water access data with regions
merged_df = water_clean.merge(regions_clean, on='name', how='left')

print(f"✓ Merged dataset shape: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")

# Check for countries without region information
countries_without_region = merged_df[merged_df['region'].isnull()]['name'].unique()
if len(countries_without_region) > 0:
    print(f"\n⚠ Warning: {len(countries_without_region)} countries without region information:")
    for country in countries_without_region[:10]:  # Show first 10
        print(f"  - {country}")
    if len(countries_without_region) > 10:
        print(f"  ... and {len(countries_without_region) - 10} more")
else:
    print("\n✓ All countries have region information")

# ============================================================================
# 6. FEATURE ENGINEERING
# ============================================================================
print("\n\n6. FEATURE ENGINEERING...")
print("-" * 80)

# 6.1 Calculate rural population
print("\n6.1 Creating population features...")
merged_df['pop_r'] = merged_df['pop_n'] - merged_df['pop_u']  # Rural population (in thousands)
merged_df['pop_r_pct'] = (merged_df['pop_r'] / merged_df['pop_n'] * 100).round(2)
merged_df['pop_u_pct'] = (merged_df['pop_u'] / merged_df['pop_n'] * 100).round(2)
print("✓ Created rural and urban population percentages")

# 6.2 Calculate national water access as weighted average where missing
print("\n6.2 Calculating national-level water access...")
merged_df['wat_bas_n_calc'] = (
    (merged_df['wat_bas_r'] * merged_df['pop_r'] + 
     merged_df['wat_bas_u'] * merged_df['pop_u']) / merged_df['pop_n']
).round(2)

# Fill missing national values with calculated values
before_fill = merged_df['wat_bas_n'].isnull().sum()
merged_df['wat_bas_n'] = merged_df['wat_bas_n'].fillna(merged_df['wat_bas_n_calc'])
after_fill = merged_df['wat_bas_n'].isnull().sum()
print(f"✓ Filled {before_fill - after_fill} missing national access values using weighted average")

# 6.3 Calculate unserved population (in thousands)
print("\n6.3 Calculating unserved populations...")

# National level
merged_df['pop_without_basic_water'] = (
    merged_df['pop_n'] * (100 - merged_df['wat_bas_n']) / 100
).round(2)

# Rural level
merged_df['pop_r_without_basic_water'] = (
    merged_df['pop_r'] * (100 - merged_df['wat_bas_r']) / 100
).round(2)

# Urban level
merged_df['pop_u_without_basic_water'] = (
    merged_df['pop_u'] * (100 - merged_df['wat_bas_u']) / 100
).round(2)

print("✓ Created unserved population features (in thousands)")

# 6.4 Create access level categories
print("\n6.4 Creating access level categories...")

def categorize_access(percentage):
    """Categorize water access percentage into levels"""
    if pd.isna(percentage):
        return 'Unknown'
    elif percentage >= 99:
        return 'Universal'
    elif percentage >= 90:
        return 'High'
    elif percentage >= 75:
        return 'Medium-High'
    elif percentage >= 50:
        return 'Medium'
    else:
        return 'Low'

merged_df['access_category_national'] = merged_df['wat_bas_n'].apply(categorize_access)
merged_df['access_category_rural'] = merged_df['wat_bas_r'].apply(categorize_access)
merged_df['access_category_urban'] = merged_df['wat_bas_u'].apply(categorize_access)

print("✓ Created access level categories (Universal, High, Medium-High, Medium, Low)")

# 6.5 Calculate rural-urban gap
print("\n6.5 Calculating rural-urban access gap...")

merged_df['rural_urban_gap'] = (merged_df['wat_bas_u'] - merged_df['wat_bas_r']).round(2)
merged_df['has_significant_gap'] = merged_df['rural_urban_gap'] > 10

gap_count = merged_df['has_significant_gap'].sum()
print(f"✓ Created rural-urban gap features")
print(f"  - Number of country-years with gap >10%: {gap_count}")

# 6.6 Calculate improvement over time
print("\n6.6 Calculating year-over-year improvements...")

merged_df = merged_df.sort_values(['name', 'year'])
merged_df['wat_bas_n_prev_year'] = merged_df.groupby('name')['wat_bas_n'].shift(1)
merged_df['yoy_improvement'] = (merged_df['wat_bas_n'] - merged_df['wat_bas_n_prev_year']).round(2)

print("✓ Created year-over-year improvement metric")

# ============================================================================
# 7. DATA QUALITY SUMMARY
# ============================================================================
print("\n\n7. DATA QUALITY SUMMARY...")
print("-" * 80)

print(f"\nFinal dataset shape: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
print(f"Number of countries: {merged_df['name'].nunique()}")
print(f"Number of years: {merged_df['year'].nunique()}")
print(f"Number of regions: {merged_df['region'].nunique()}")
print(f"Year range: {merged_df['year'].min()} - {merged_df['year'].max()}")

print("\nData completeness by key variables:")
completeness = pd.DataFrame({
    'Variable': ['National Basic Water', 'Rural Basic Water', 'Urban Basic Water', 
                 'Population', 'Urban Population', 'Region'],
    'Complete_Records': [
        merged_df['wat_bas_n'].notna().sum(),
        merged_df['wat_bas_r'].notna().sum(),
        merged_df['wat_bas_u'].notna().sum(),
        merged_df['pop_n'].notna().sum(),
        merged_df['pop_u'].notna().sum(),
        merged_df['region'].notna().sum()
    ],
    'Percentage': [
        (merged_df['wat_bas_n'].notna().sum() / len(merged_df) * 100).round(2),
        (merged_df['wat_bas_r'].notna().sum() / len(merged_df) * 100).round(2),
        (merged_df['wat_bas_u'].notna().sum() / len(merged_df) * 100).round(2),
        (merged_df['pop_n'].notna().sum() / len(merged_df) * 100).round(2),
        (merged_df['pop_u'].notna().sum() / len(merged_df) * 100).round(2),
        (merged_df['region'].notna().sum() / len(merged_df) * 100).round(2)
    ]
})
print(completeness.to_string(index=False))

# ============================================================================
# 8. SAVE CLEANED DATA
# ============================================================================
print("\n\n8. SAVING CLEANED DATA TO 'cleaned_data/' FOLDER...")
print("-" * 80)

# Save the main cleaned and merged dataset
output_file = 'cleaned_data/water_access_cleaned.csv'
merged_df.to_csv(output_file, index=False)
print(f"✓ Saved main cleaned data to: {output_file}")

# Save a summary statistics file by region
summary_file = 'cleaned_data/regional_summary_statistics.csv'
summary_stats = merged_df.groupby('region').agg({
    'wat_bas_n': ['mean', 'min', 'max', 'std'],
    'wat_bas_r': ['mean', 'min', 'max', 'std'],
    'wat_bas_u': ['mean', 'min', 'max', 'std'],
    'pop_n': 'sum',
    'pop_without_basic_water': 'sum',
    'name': 'nunique'
}).round(2)
summary_stats.columns = ['_'.join(col) for col in summary_stats.columns]
summary_stats = summary_stats.reset_index()
summary_stats.to_csv(summary_file, index=False)
print(f"✓ Saved regional summary to: {summary_file}")

# Save year-over-year comparison
yearly_file = 'cleaned_data/yearly_trends.csv'
yearly_trends = merged_df.groupby(['year', 'region']).agg({
    'wat_bas_n': 'mean',
    'wat_bas_r': 'mean',
    'wat_bas_u': 'mean',
    'pop_without_basic_water': 'sum',
    'name': 'nunique'
}).reset_index().round(2)
yearly_trends.columns = ['year', 'region', 'avg_national_access', 'avg_rural_access', 
                          'avg_urban_access', 'total_unserved_pop', 'num_countries']
yearly_trends.to_csv(yearly_file, index=False)
print(f"✓ Saved yearly trends to: {yearly_file}")

# Save latest year data (for quick reference)
latest_year = merged_df['year'].max()
latest_data = merged_df[merged_df['year'] == latest_year].copy()
latest_file = f'cleaned_data/water_access_{latest_year}.csv'
latest_data.to_csv(latest_file, index=False)
print(f"✓ Saved {latest_year} data to: {latest_file}")

# ============================================================================
# 9. GENERATE DATA DICTIONARY
# ============================================================================
print("\n\n9. GENERATING DATA DICTIONARY...")
print("-" * 80)

column_descriptions = [
    'Country name',
    'Year of observation',
    'National population (thousands)',
    'Urban population (thousands)',
    'National % with at least basic water',
    'National % with limited water',
    'National % with unimproved water',
    'National % using surface water',
    'Rural % with at least basic water',
    'Rural % with limited water',
    'Rural % with unimproved water',
    'Rural % using surface water',
    'Urban % with at least basic water',
    'Urban % with limited water',
    'Urban % with unimproved water',
    'Urban % using surface water',
    'Geographic region',
    'Rural population (thousands)',
    'Rural population percentage',
    'Urban population percentage',
    'Calculated national basic water access',
    'National pop without basic water (thousands)',
    'Rural pop without basic water (thousands)',
    'Urban pop without basic water (thousands)',
    'National access category',
    'Rural access category',
    'Urban access category',
    'Urban - Rural access gap (%)',
    'Boolean: gap > 10%',
    'Previous year national access',
    'Year-over-year improvement (%)'
]

data_dict = pd.DataFrame({
    'Column_Name': merged_df.columns,
    'Data_Type': [str(dtype) for dtype in merged_df.dtypes.values],
    'Non_Null_Count': merged_df.notna().sum().values,
    'Description': column_descriptions
})

dict_file = 'cleaned_data/data_dictionary.csv'
data_dict.to_csv(dict_file, index=False)
print(f"✓ Saved data dictionary to: {dict_file}")

# ============================================================================
# 10. GENERATE SUMMARY REPORT
# ============================================================================
print("\n\n10. GENERATING SUMMARY REPORT...")
print("-" * 80)

report_lines = []
report_lines.append("=" * 80)
report_lines.append("WATER ACCESS DATA CLEANING - SUMMARY REPORT")
report_lines.append("=" * 80)
report_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"\nData Period: {merged_df['year'].min()} - {merged_df['year'].max()}")
report_lines.append(f"Total Records: {len(merged_df):,}")
report_lines.append(f"Countries: {merged_df['name'].nunique()}")
report_lines.append(f"Regions: {merged_df['region'].nunique()}")

report_lines.append("\n\n1. DATA QUALITY METRICS")
report_lines.append("-" * 80)
report_lines.append(f"Completeness of key variables:")
for idx, row in completeness.iterrows():
    report_lines.append(f"  {row['Variable']:25s}: {row['Complete_Records']:6,} / {len(merged_df):6,} ({row['Percentage']:5.1f}%)")

report_lines.append("\n\n2. GLOBAL OVERVIEW")
report_lines.append("-" * 80)
latest_stats = latest_data.agg({
    'wat_bas_n': 'mean',
    'wat_bas_r': 'mean',
    'wat_bas_u': 'mean',
    'pop_without_basic_water': 'sum'
})
report_lines.append(f"\n{latest_year} Statistics:")
report_lines.append(f"  Average National Access:          {latest_stats['wat_bas_n']:.2f}%")
report_lines.append(f"  Average Rural Access:             {latest_stats['wat_bas_r']:.2f}%")
report_lines.append(f"  Average Urban Access:             {latest_stats['wat_bas_u']:.2f}%")
report_lines.append(f"  Total Unserved Population:        {latest_stats['pop_without_basic_water']/1000:.1f} million")

report_lines.append("\n\n3. REGIONAL BREAKDOWN")
report_lines.append("-" * 80)
regional_latest = latest_data.groupby('region').agg({
    'wat_bas_n': 'mean',
    'pop_without_basic_water': 'sum',
    'name': 'nunique'
}).round(2).sort_values('wat_bas_n', ascending=False)

for region, row in regional_latest.iterrows():
    report_lines.append(f"\n{region}:")
    report_lines.append(f"  Countries:          {int(row['name'])}")
    report_lines.append(f"  Avg Access:         {row['wat_bas_n']:.2f}%")
    report_lines.append(f"  Unserved Pop:       {row['pop_without_basic_water']/1000:.2f} million")

report_lines.append("\n\n4. TOP 10 COUNTRIES (Highest Access)")
report_lines.append("-" * 80)
top_10 = latest_data.nlargest(10, 'wat_bas_n')[['name', 'region', 'wat_bas_n']]
for idx, (_, row) in enumerate(top_10.iterrows(), 1):
    report_lines.append(f"{idx:2d}. {row['name']:30s} ({row['region']:25s}): {row['wat_bas_n']:6.2f}%")

report_lines.append("\n\n5. BOTTOM 10 COUNTRIES (Lowest Access)")
report_lines.append("-" * 80)
bottom_10 = latest_data.nsmallest(10, 'wat_bas_n')[['name', 'region', 'wat_bas_n']]
for idx, (_, row) in enumerate(bottom_10.iterrows(), 1):
    report_lines.append(f"{idx:2d}. {row['name']:30s} ({row['region']:25s}): {row['wat_bas_n']:6.2f}%")

report_lines.append("\n\n6. FILES CREATED")
report_lines.append("-" * 80)
report_lines.append(f"  1. {output_file}")
report_lines.append(f"  2. {summary_file}")
report_lines.append(f"  3. {yearly_file}")
report_lines.append(f"  4. {latest_file}")
report_lines.append(f"  5. {dict_file}")
report_lines.append(f"  6. reports/data_cleaning_summary.txt")

report_lines.append("\n" + "=" * 80)
report_lines.append("END OF REPORT")
report_lines.append("=" * 80)

# Save report
report_text = "\n".join(report_lines)
report_output = 'reports/data_cleaning_summary.txt'
with open(report_output, 'w') as f:
    f.write(report_text)
print(f"✓ Saved summary report to: {report_output}")

# Also print to console
print("\n" + report_text)

print("\n" + "=" * 80)
print("DATA CLEANING COMPLETE!")
print("=" * 80)
print("\nNext steps:")
print("  1. Review the cleaned data in 'cleaned_data/' folder")
print("  2. Check the summary report in 'reports/' folder")
print("  3. Run the analysis script: python scripts/water_data_analysis.py")
print("  4. Or use Jupyter Notebook for interactive analysis")
print("=" * 80)
