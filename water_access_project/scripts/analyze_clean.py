#!/usr/bin/env python3
"""
Water Data Analysis Script - Clean Version
Analyzes the cleaned WHO/UNICEF water access data
"""

import pandas as pd
import sys
import os

def main():
    print("=" * 70)
    print("WATER ACCESS DATA ANALYSIS")
    print("=" * 70)
    print()
    
    # Find the cleaned data file
    possible_files = [
        "data/cleaned/water_data_cleaned.csv",
        "../data/cleaned/water_data_cleaned.csv",
        "water_data_cleaned.csv"
    ]
    
    data_file = None
    for f in possible_files:
        if os.path.exists(f):
            data_file = f
            break
    
    if data_file is None:
        print("ERROR: Cleaned data file not found!")
        print("Expected location: data/cleaned/water_data_cleaned.csv")
        sys.exit(1)
    
    print(f"Loading data from: {data_file}")
    
    # Load data
    df = pd.read_csv(data_file, na_values=['NAN'])
    
    # Convert numeric columns
    numeric_cols = ['pop_n', 'pop_u', 'wat_bas_n', 'wat_lim_n', 'wat_unimp_n', 
                    'wat_sur_n', 'wat_bas_r', 'wat_lim_r', 'wat_unimp_r', 
                    'wat_sur_r', 'wat_bas_u', 'wat_lim_u', 'wat_unimp_u', 'wat_sur_u']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"Data loaded: {df.shape[0]} rows x {df.shape[1]} columns")
    print()
    
    # BASIC STATISTICS
    print("=" * 70)
    print("1. INCOME GROUP DISTRIBUTION")
    print("=" * 70)
    print(df['income_group'].value_counts(dropna=False))
    print()
    
    # WATER ACCESS STATISTICS
    print("=" * 70)
    print("2. NATIONAL WATER ACCESS STATISTICS")
    print("=" * 70)
    print(df['wat_bas_n'].describe())
    print()
    
    print(f"Countries with 100% basic access: {(df['wat_bas_n'] == 100).sum()}")
    print(f"Countries with <50% basic access: {(df['wat_bas_n'] < 50).sum()}")
    print(f"Countries with <80% basic access: {(df['wat_bas_n'] < 80).sum()}")
    print()
    
    # LOWEST ACCESS
    print("=" * 70)
    print("3. COUNTRIES WITH LOWEST BASIC WATER ACCESS")
    print("=" * 70)
    lowest = df.nsmallest(10, 'wat_bas_n')[['name', 'income_group', 'wat_bas_n']]
    print(lowest.to_string(index=False))
    print()
    
    # INCOME GROUP ANALYSIS
    print("=" * 70)
    print("4. WATER ACCESS BY INCOME GROUP")
    print("=" * 70)
    df_income = df[df['income_group'].notna()].copy()
    income_stats = df_income.groupby('income_group')['wat_bas_n'].agg(['mean', 'median', 'min', 'max', 'count'])
    print(income_stats.round(2))
    print()
    
    # URBAN VS RURAL
    print("=" * 70)
    print("5. URBAN VS RURAL ACCESS")
    print("=" * 70)
    urban_avg = df['wat_bas_u'].mean()
    rural_avg = df['wat_bas_r'].mean()
    print(f"Urban average:  {urban_avg:.2f}%")
    print(f"Rural average:  {rural_avg:.2f}%")
    print(f"Gap:            {urban_avg - rural_avg:.2f} percentage points")
    print()
    
    # LARGEST GAPS
    df['urban_rural_gap'] = df['wat_bas_u'] - df['wat_bas_r']
    gaps = df.nlargest(5, 'urban_rural_gap')[['name', 'wat_bas_u', 'wat_bas_r', 'urban_rural_gap']]
    print("Countries with largest urban-rural gap:")
    print(gaps.to_string(index=False))
    print()
    
    # POPULATION ANALYSIS
    print("=" * 70)
    print("6. POPULATION WITHOUT BASIC ACCESS")
    print("=" * 70)
    df['pop_without_basic'] = df['pop_n'] * (100 - df['wat_bas_n']) / 100
    
    total_pop = df['pop_n'].sum()
    total_without = df['pop_without_basic'].sum()
    
    print(f"Total population:           {total_pop:,.0f} thousand")
    print(f"Population without access:  {total_without:,.0f} thousand")
    print(f"Percentage without access:  {(total_without/total_pop)*100:.2f}%")
    print()
    
    most_affected = df.nlargest(10, 'pop_without_basic')[['name', 'pop_n', 'wat_bas_n', 'pop_without_basic']]
    most_affected['pop_without_basic'] = most_affected['pop_without_basic'].round(0)
    print("Countries with most people lacking access (absolute numbers):")
    print(most_affected.to_string(index=False))
    print()
    
    # SERVICE LEVELS
    print("=" * 70)
    print("7. GLOBAL SERVICE LEVEL DISTRIBUTION")
    print("=" * 70)
    print(f"At least basic:  {df['wat_bas_n'].mean():6.2f}%")
    print(f"Limited:         {df['wat_lim_n'].mean():6.2f}%")
    print(f"Unimproved:      {df['wat_unimp_n'].mean():6.2f}%")
    print(f"Surface water:   {df['wat_sur_n'].mean():6.2f}%")
    print()
    
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    main()
