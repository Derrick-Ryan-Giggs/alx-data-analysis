"""
Water Access Data Analysis and Visualization Script
====================================================
This script performs advanced analysis and creates visualizations
for the cleaned water access data.

Author: ALX Data Analysis Project
Date: February 2026

Prerequisites: Run water_data_cleaning.py first
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

print("=" * 80)
print("WATER ACCESS DATA ANALYSIS AND VISUALIZATION")
print("=" * 80)

# ============================================================================
# 1. LOAD CLEANED DATA
# ============================================================================
print("\n1. LOADING CLEANED DATA FROM 'cleaned_data/' FOLDER...")
print("-" * 80)

try:
    df = pd.read_csv('cleaned_data/water_access_cleaned.csv')
    print(f"✓ Loaded cleaned data: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"  Year range: {df['year'].min()} - {df['year'].max()}")
    print(f"  Countries: {df['name'].nunique()}")
    print(f"  Regions: {df['region'].nunique()}")
except FileNotFoundError:
    print("✗ Error: cleaned_data/water_access_cleaned.csv not found!")
    print("\nPlease run water_data_cleaning.py first to generate the cleaned data.")
    print("\nCommand:")
    print("  python scripts/water_data_cleaning.py")
    exit(1)

# ============================================================================
# 2. EXPLORATORY DATA ANALYSIS
# ============================================================================
print("\n\n2. EXPLORATORY DATA ANALYSIS...")
print("-" * 80)

# 2.1 Temporal trends
print("\n2.1 Temporal Trends Analysis")
temporal_trends = df.groupby('year').agg({
    'wat_bas_n': 'mean',
    'wat_bas_r': 'mean',
    'wat_bas_u': 'mean',
    'pop_without_basic_water': 'sum'
}).round(2)

print("\nGlobal average water access by year:")
print(temporal_trends)

# Calculate year-over-year change
temporal_trends['yoy_change_national'] = temporal_trends['wat_bas_n'].diff()
print("\nYear-over-year change in national access:")
print(temporal_trends[['wat_bas_n', 'yoy_change_national']].tail(10))

# 2.2 Regional analysis
print("\n\n2.2 Regional Analysis")
regional_summary = df.groupby('region').agg({
    'wat_bas_n': ['mean', 'std', 'min', 'max'],
    'pop_without_basic_water': 'sum',
    'name': 'nunique'
}).round(2)
regional_summary.columns = ['Avg_Access_%', 'Std_Dev', 'Min_%', 'Max_%', 
                             'Total_Unserved_Pop', 'Num_Countries']
print("\nRegional water access summary:")
print(regional_summary.sort_values('Avg_Access_%', ascending=False))

# 2.3 Rural vs Urban analysis
print("\n\n2.3 Rural vs Urban Access Analysis")
latest_year = df['year'].max()
rural_urban = df[df['year'] == latest_year].copy()

print(f"\nAverage access in {latest_year}:")
print(f"  Rural:  {rural_urban['wat_bas_r'].mean():.2f}%")
print(f"  Urban:  {rural_urban['wat_bas_u'].mean():.2f}%")
print(f"  Gap:    {rural_urban['rural_urban_gap'].mean():.2f}% (positive = urban advantage)")

# ============================================================================
# 3. STATISTICAL ANALYSIS
# ============================================================================
print("\n\n3. STATISTICAL ANALYSIS...")
print("-" * 80)

# 3.1 Correlation analysis
print("\n3.1 Correlation Analysis")
correlation_vars = ['wat_bas_n', 'wat_bas_r', 'wat_bas_u', 'pop_u_pct', 
                    'rural_urban_gap', 'pop_n']
corr_matrix = df[correlation_vars].corr().round(3)
print("\nCorrelation matrix:")
print(corr_matrix)

# 3.2 Statistical tests - comparing regions
print("\n\n3.2 Regional Comparison (ANOVA Test)")
print("Testing if there are significant differences between regions...")

regions = df['region'].dropna().unique()
regional_groups = [df[df['region'] == region]['wat_bas_n'].dropna() for region in regions]

# Perform ANOVA
f_stat, p_value = stats.f_oneway(*regional_groups)
print(f"\nF-statistic: {f_stat:.4f}")
print(f"P-value: {p_value:.6f}")

if p_value < 0.05:
    print("✓ Significant difference between regions (p < 0.05)")
    print("  → Regional differences in water access are statistically significant")
else:
    print("✗ No significant difference between regions (p >= 0.05)")

# ============================================================================
# 4. CREATE VISUALIZATIONS
# ============================================================================
print("\n\n4. CREATING VISUALIZATIONS...")
print("-" * 80)

# Ensure visualizations folder exists
if not os.path.exists('visualizations'):
    os.makedirs('visualizations')
    print("✓ Created 'visualizations' directory")

# 4.1 Temporal trends plot
print("\n4.1 Creating temporal trends visualization...")
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Water Access Trends Over Time (2000-2020)', fontsize=16, fontweight='bold')

# Plot 1: Overall trends
temporal_data = df.groupby('year')[['wat_bas_n', 'wat_bas_r', 'wat_bas_u']].mean()
axes[0, 0].plot(temporal_data.index, temporal_data['wat_bas_n'], marker='o', linewidth=2, label='National', color='navy')
axes[0, 0].plot(temporal_data.index, temporal_data['wat_bas_r'], marker='s', linewidth=2, label='Rural', color='green')
axes[0, 0].plot(temporal_data.index, temporal_data['wat_bas_u'], marker='^', linewidth=2, label='Urban', color='orangered')
axes[0, 0].set_xlabel('Year', fontsize=11)
axes[0, 0].set_ylabel('% Population with Basic Water Access', fontsize=11)
axes[0, 0].set_title('Global Average Water Access by Type', fontsize=12, fontweight='bold')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].set_ylim([80, 100])

# Plot 2: Total unserved population
unserved_by_year = df.groupby('year')['pop_without_basic_water'].sum() / 1000  # Convert to millions
axes[0, 1].bar(unserved_by_year.index, unserved_by_year.values, color='coral', alpha=0.7, edgecolor='darkred')
axes[0, 1].set_xlabel('Year', fontsize=11)
axes[0, 1].set_ylabel('Population (Millions)', fontsize=11)
axes[0, 1].set_title('Total Population Without Basic Water Access', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(unserved_by_year.values):
    if i % 5 == 0:  # Label every 5th bar
        axes[0, 1].text(unserved_by_year.index[i], v, f'{v:.0f}M', ha='center', va='bottom', fontsize=8)

# Plot 3: Regional trends
regional_temporal = df.groupby(['year', 'region'])['wat_bas_n'].mean().reset_index()
for region in df['region'].dropna().unique():
    region_data = regional_temporal[regional_temporal['region'] == region]
    axes[1, 0].plot(region_data['year'], region_data['wat_bas_n'], marker='o', label=region, linewidth=1.5, markersize=4)
axes[1, 0].set_xlabel('Year', fontsize=11)
axes[1, 0].set_ylabel('% Population with Basic Water Access', fontsize=11)
axes[1, 0].set_title('Regional Water Access Trends', fontsize=12, fontweight='bold')
axes[1, 0].legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
axes[1, 0].grid(True, alpha=0.3)

# Plot 4: Rural-Urban gap over time
gap_by_year = df.groupby('year')['rural_urban_gap'].mean()
axes[1, 1].plot(gap_by_year.index, gap_by_year.values, marker='o', linewidth=2, color='darkgreen', markersize=6)
axes[1, 1].axhline(y=0, color='red', linestyle='--', alpha=0.5, linewidth=1.5)
axes[1, 1].fill_between(gap_by_year.index, 0, gap_by_year.values, where=(gap_by_year.values > 0), alpha=0.3, color='green', interpolate=True)
axes[1, 1].set_xlabel('Year', fontsize=11)
axes[1, 1].set_ylabel('Urban - Rural Gap (%)', fontsize=11)
axes[1, 1].set_title('Average Rural-Urban Access Gap', fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/temporal_trends.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/temporal_trends.png")
plt.close()

# 4.2 Regional comparison plot
print("\n4.2 Creating regional comparison visualization...")
latest_data = df[df['year'] == latest_year].copy()

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle(f'Regional Water Access Comparison ({latest_year})', fontsize=16, fontweight='bold')

# Plot 1: Box plot by region
axes[0, 0].set_title('Distribution of National Access by Region', fontsize=12, fontweight='bold')
regional_data = latest_data.dropna(subset=['region', 'wat_bas_n'])
regions_sorted = regional_data.groupby('region')['wat_bas_n'].median().sort_values(ascending=False).index
box_plot = sns.boxplot(data=regional_data, y='region', x='wat_bas_n', order=regions_sorted, ax=axes[0, 0], palette='Set2')
axes[0, 0].set_xlabel('% Population with Basic Water Access', fontsize=11)
axes[0, 0].set_ylabel('Region', fontsize=11)
axes[0, 0].grid(True, alpha=0.3, axis='x')

# Plot 2: Bar chart of regional averages
regional_avg = latest_data.groupby('region')['wat_bas_n'].mean().sort_values(ascending=True)
colors = plt.cm.RdYlGn(regional_avg.values / 100)  # Color based on value
axes[0, 1].barh(range(len(regional_avg)), regional_avg.values, color=colors, alpha=0.8, edgecolor='black')
axes[0, 1].set_yticks(range(len(regional_avg)))
axes[0, 1].set_yticklabels(regional_avg.index, fontsize=9)
axes[0, 1].set_xlabel('Average % Population with Basic Water Access', fontsize=11)
axes[0, 1].set_title('Regional Average Water Access', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='x')
# Add value labels
for i, v in enumerate(regional_avg.values):
    axes[0, 1].text(v + 0.5, i, f'{v:.1f}%', va='center', fontsize=8)

# Plot 3: Rural vs Urban by region
rural_urban_regional = latest_data.groupby('region')[['wat_bas_r', 'wat_bas_u']].mean().sort_values('wat_bas_r')
x = np.arange(len(rural_urban_regional))
width = 0.35
bars1 = axes[1, 0].barh(x - width/2, rural_urban_regional['wat_bas_r'], width, label='Rural', alpha=0.8, color='forestgreen')
bars2 = axes[1, 0].barh(x + width/2, rural_urban_regional['wat_bas_u'], width, label='Urban', alpha=0.8, color='steelblue')
axes[1, 0].set_yticks(x)
axes[1, 0].set_yticklabels(rural_urban_regional.index, fontsize=9)
axes[1, 0].set_xlabel('% Population with Basic Water Access', fontsize=11)
axes[1, 0].set_title('Rural vs Urban Access by Region', fontsize=12, fontweight='bold')
axes[1, 0].legend()
axes[1, 0].grid(True, alpha=0.3, axis='x')

# Plot 4: Unserved population by region
unserved_regional = latest_data.groupby('region')['pop_without_basic_water'].sum().sort_values(ascending=False) / 1000
colors = plt.cm.Reds(unserved_regional.values / unserved_regional.max())
axes[1, 1].bar(range(len(unserved_regional)), unserved_regional.values, color=colors, alpha=0.8, edgecolor='darkred')
axes[1, 1].set_xticks(range(len(unserved_regional)))
axes[1, 1].set_xticklabels(unserved_regional.index, rotation=45, ha='right', fontsize=8)
axes[1, 1].set_ylabel('Population (Millions)', fontsize=11)
axes[1, 1].set_title('Population Without Basic Water Access', fontsize=12, fontweight='bold')
axes[1, 1].grid(True, alpha=0.3, axis='y')
# Add value labels
for i, v in enumerate(unserved_regional.values):
    axes[1, 1].text(i, v, f'{v:.0f}M', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('visualizations/regional_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/regional_comparison.png")
plt.close()

# 4.3 Correlation heatmap
print("\n4.3 Creating correlation heatmap...")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax,
            vmin=-1, vmax=1)
plt.title('Correlation Matrix of Key Variables', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('visualizations/correlation_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/correlation_heatmap.png")
plt.close()

# 4.4 Top and bottom performers
print("\n4.4 Creating top/bottom performers visualization...")
latest_complete = latest_data.dropna(subset=['wat_bas_n'])
top_10 = latest_complete.nlargest(10, 'wat_bas_n')
bottom_10 = latest_complete.nsmallest(10, 'wat_bas_n')

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle(f'Water Access Leaders and Laggards ({latest_year})', fontsize=16, fontweight='bold')

# Top 10
colors_top = plt.cm.Greens(np.linspace(0.4, 0.9, len(top_10)))
axes[0].barh(range(len(top_10)), top_10['wat_bas_n'].values, color=colors_top, edgecolor='darkgreen')
axes[0].set_yticks(range(len(top_10)))
axes[0].set_yticklabels(top_10['name'].values, fontsize=10)
axes[0].set_xlabel('% Population with Basic Water Access', fontsize=11)
axes[0].set_title('Top 10 Countries', fontsize=13, fontweight='bold')
axes[0].invert_yaxis()
axes[0].grid(True, alpha=0.3, axis='x')
axes[0].set_xlim([98, 100.2])
# Add value labels
for i, v in enumerate(top_10['wat_bas_n'].values):
    axes[0].text(v + 0.02, i, f'{v:.2f}%', va='center', fontsize=9)

# Bottom 10
colors_bottom = plt.cm.Reds(np.linspace(0.9, 0.4, len(bottom_10)))
axes[1].barh(range(len(bottom_10)), bottom_10['wat_bas_n'].values, color=colors_bottom, edgecolor='darkred')
axes[1].set_yticks(range(len(bottom_10)))
axes[1].set_yticklabels(bottom_10['name'].values, fontsize=10)
axes[1].set_xlabel('% Population with Basic Water Access', fontsize=11)
axes[1].set_title('Bottom 10 Countries', fontsize=13, fontweight='bold')
axes[1].invert_yaxis()
axes[1].grid(True, alpha=0.3, axis='x')
# Add value labels
for i, v in enumerate(bottom_10['wat_bas_n'].values):
    axes[1].text(v + 1, i, f'{v:.2f}%', va='center', fontsize=9)

plt.tight_layout()
plt.savefig('visualizations/top_bottom_performers.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/top_bottom_performers.png")
plt.close()

# ============================================================================
# 5. GENERATE INSIGHTS REPORT
# ============================================================================
print("\n\n5. GENERATING INSIGHTS REPORT...")
print("-" * 80)

# Create a comprehensive report
report_lines = []
report_lines.append("=" * 80)
report_lines.append("WATER ACCESS DATA ANALYSIS - INSIGHTS REPORT")
report_lines.append("=" * 80)
report_lines.append(f"\nGenerated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"Data Period: {df['year'].min()} - {df['year'].max()}")
report_lines.append(f"Number of Countries: {df['name'].nunique()}")
report_lines.append(f"Number of Regions: {df['region'].nunique()}")
report_lines.append(f"Total Records: {len(df):,}")

report_lines.append("\n\n1. GLOBAL OVERVIEW")
report_lines.append("-" * 80)
report_lines.append(f"\nLatest Year ({latest_year}) Statistics:")
latest_stats = latest_data.agg({
    'wat_bas_n': 'mean',
    'wat_bas_r': 'mean',
    'wat_bas_u': 'mean',
    'pop_without_basic_water': 'sum'
})
report_lines.append(f"  Average National Access:          {latest_stats['wat_bas_n']:.2f}%")
report_lines.append(f"  Average Rural Access:             {latest_stats['wat_bas_r']:.2f}%")
report_lines.append(f"  Average Urban Access:             {latest_stats['wat_bas_u']:.2f}%")
report_lines.append(f"  Total Unserved Population:        {latest_stats['pop_without_basic_water']/1000:.1f} million")
report_lines.append(f"  Rural-Urban Gap:                  {(latest_stats['wat_bas_u'] - latest_stats['wat_bas_r']):.2f}%")

# Progress over time
first_year = df['year'].min()
first_year_data = df[df['year'] == first_year]
first_stats = first_year_data.agg({
    'wat_bas_n': 'mean',
    'wat_bas_r': 'mean',
    'wat_bas_u': 'mean',
    'pop_without_basic_water': 'sum'
})

progress_national = latest_stats['wat_bas_n'] - first_stats['wat_bas_n']
progress_rural = latest_stats['wat_bas_r'] - first_stats['wat_bas_r']
progress_urban = latest_stats['wat_bas_u'] - first_stats['wat_bas_u']

report_lines.append(f"\nProgress from {first_year} to {latest_year}:")
report_lines.append(f"  National Access Improvement:      {progress_national:+.2f} percentage points")
report_lines.append(f"  Rural Access Improvement:         {progress_rural:+.2f} percentage points")
report_lines.append(f"  Urban Access Improvement:         {progress_urban:+.2f} percentage points")
report_lines.append(f"  Reduction in Unserved Population: {(first_stats['pop_without_basic_water'] - latest_stats['pop_without_basic_water'])/1000:.1f} million")

report_lines.append("\n\n2. REGIONAL INSIGHTS")
report_lines.append("-" * 80)
regional_latest = latest_data.groupby('region').agg({
    'wat_bas_n': 'mean',
    'wat_bas_r': 'mean',
    'wat_bas_u': 'mean',
    'pop_without_basic_water': 'sum',
    'rural_urban_gap': 'mean',
    'name': 'nunique'
}).round(2).sort_values('wat_bas_n', ascending=False)

for idx, (region, row) in enumerate(regional_latest.iterrows(), 1):
    report_lines.append(f"\n{idx}. {region}")
    report_lines.append(f"   Countries:              {int(row['name'])}")
    report_lines.append(f"   Avg National Access:    {row['wat_bas_n']:.2f}%")
    report_lines.append(f"   Avg Rural Access:       {row['wat_bas_r']:.2f}%")
    report_lines.append(f"   Avg Urban Access:       {row['wat_bas_u']:.2f}%")
    report_lines.append(f"   Rural-Urban Gap:        {row['rural_urban_gap']:+.2f}%")
    report_lines.append(f"   Unserved Population:    {row['pop_without_basic_water']/1000:.2f} million")

report_lines.append("\n\n3. RURAL-URBAN DIVIDE")
report_lines.append("-" * 80)
gap_stats = latest_data['rural_urban_gap'].describe()
report_lines.append(f"Rural-Urban Gap Statistics ({latest_year}):")
report_lines.append(f"  Mean Gap:               {gap_stats['mean']:+.2f}% (positive = urban advantage)")
report_lines.append(f"  Median Gap:             {gap_stats['50%']:+.2f}%")
report_lines.append(f"  Standard Deviation:     {gap_stats['std']:.2f}%")
report_lines.append(f"  Maximum Gap:            {gap_stats['max']:+.2f}% (largest urban advantage)")
report_lines.append(f"  Minimum Gap:            {gap_stats['min']:+.2f}% (largest rural advantage)")

# Countries with largest gaps
largest_gaps = latest_data.nsmallest(10, 'rural_urban_gap')[['name', 'region', 'rural_urban_gap', 'wat_bas_r', 'wat_bas_u']]
report_lines.append("\nTop 10 Countries with Largest Rural Disadvantage:")
for idx, (_, row) in enumerate(largest_gaps.iterrows(), 1):
    if pd.notna(row['rural_urban_gap']):
        report_lines.append(f"  {idx:2d}. {row['name']:30s} ({row['region']:25s})")
        report_lines.append(f"      Gap: {abs(row['rural_urban_gap']):6.2f}% | Rural: {row['wat_bas_r']:6.2f}% | Urban: {row['wat_bas_u']:6.2f}%")

report_lines.append("\n\n4. COUNTRIES REQUIRING ATTENTION")
report_lines.append("-" * 80)
low_access = latest_data[latest_data['wat_bas_n'] < 75].sort_values('wat_bas_n')
report_lines.append(f"Countries with <75% National Access: {len(low_access)}")

if len(low_access) > 0:
    report_lines.append(f"\nBottom 15 Countries by National Access:")
    for idx, (_, row) in enumerate(low_access.head(15).iterrows(), 1):
        report_lines.append(f"  {idx:2d}. {row['name']:30s} ({row['region']:25s}): {row['wat_bas_n']:6.2f}%")
        report_lines.append(f"      Unserved: {row['pop_without_basic_water']/1000:6.2f}M | Rural: {row['wat_bas_r']:6.2f}% | Urban: {row['wat_bas_u']:6.2f}%")

report_lines.append("\n\n5. STATISTICAL FINDINGS")
report_lines.append("-" * 80)
report_lines.append(f"ANOVA Test Results:")
report_lines.append(f"  F-statistic:            {f_stat:.4f}")
report_lines.append(f"  P-value:                {p_value:.6f}")
if p_value < 0.05:
    report_lines.append(f"  Interpretation:         Regional differences are statistically significant (p < 0.05)")
else:
    report_lines.append(f"  Interpretation:         No significant regional differences detected (p >= 0.05)")

report_lines.append("\n\nKey Correlations:")
report_lines.append(f"  Rural vs Urban Access:              r = {corr_matrix.loc['wat_bas_r', 'wat_bas_u']:.3f}")
report_lines.append(f"  Urban % vs National Access:         r = {corr_matrix.loc['pop_u_pct', 'wat_bas_n']:.3f}")
report_lines.append(f"  Population vs National Access:      r = {corr_matrix.loc['pop_n', 'wat_bas_n']:.3f}")

report_lines.append("\n\n6. KEY RECOMMENDATIONS")
report_lines.append("-" * 80)
report_lines.append("1. PRIORITY REGIONS:")
worst_regions = regional_latest.nsmallest(3, 'wat_bas_n')
for idx, (region, row) in enumerate(worst_regions.iterrows(), 1):
    report_lines.append(f"   {idx}. {region} ({row['wat_bas_n']:.1f}% access, {row['pop_without_basic_water']/1000:.1f}M unserved)")

report_lines.append("\n2. RURAL DEVELOPMENT:")
report_lines.append(f"   - Average rural-urban gap is {gap_stats['mean']:.1f}%")
report_lines.append(f"   - Focus on countries with gaps >15%")
report_lines.append(f"   - Prioritize rural infrastructure in lagging regions")

report_lines.append("\n3. POPULATION IMPACT:")
report_lines.append(f"   - {latest_stats['pop_without_basic_water']/1000:.1f} million people still lack basic water access")
report_lines.append(f"   - Most concentrated in {unserved_regional.index[0]} ({unserved_regional.values[0]:.1f}M)")

report_lines.append("\n4. PROGRESS MONITORING:")
report_lines.append(f"   - Track SDG 6 progress toward universal access by 2030")
report_lines.append(f"   - Current trajectory: {progress_national/(latest_year-first_year):.2f}% improvement per year")
report_lines.append(f"   - Need to accelerate in low-performing countries")

report_lines.append("\n" + "=" * 80)
report_lines.append("END OF REPORT")
report_lines.append("=" * 80)

# Save report
report_text = "\n".join(report_lines)
report_output = 'reports/analysis_insights_report.txt'
with open(report_output, 'w') as f:
    f.write(report_text)
print(f"✓ Saved insights report to: {report_output}")

# Also print to console
print("\n" + report_text)

# ============================================================================
# 6. EXPORT ANALYSIS RESULTS
# ============================================================================
print("\n\n6. EXPORTING ANALYSIS RESULTS TO 'cleaned_data/' FOLDER...")
print("-" * 80)

# Export country rankings
rankings = latest_data[['name', 'region', 'wat_bas_n', 'wat_bas_r', 'wat_bas_u', 
                        'rural_urban_gap', 'pop_without_basic_water']].copy()
rankings = rankings.sort_values('wat_bas_n', ascending=False)
rankings.to_csv('cleaned_data/country_rankings_latest.csv', index=False)
print("✓ Saved: cleaned_data/country_rankings_latest.csv")

# Export temporal analysis
temporal_export = df.groupby(['year']).agg({
    'wat_bas_n': ['mean', 'min', 'max'],
    'wat_bas_r': ['mean', 'min', 'max'],
    'wat_bas_u': ['mean', 'min', 'max'],
    'pop_without_basic_water': 'sum'
}).round(2)
temporal_export.columns = ['_'.join(col) for col in temporal_export.columns]
temporal_export = temporal_export.reset_index()
temporal_export.to_csv('cleaned_data/temporal_analysis.csv', index=False)
print("✓ Saved: cleaned_data/temporal_analysis.csv")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE!")
print("=" * 80)
print("\nGenerated files:")
print("\nVisualizations:")
print("  1. visualizations/temporal_trends.png")
print("  2. visualizations/regional_comparison.png")
print("  3. visualizations/correlation_heatmap.png")
print("  4. visualizations/top_bottom_performers.png")
print("\nReports:")
print("  5. reports/analysis_insights_report.txt")
print("\nData:")
print("  6. cleaned_data/country_rankings_latest.csv")
print("  7. cleaned_data/temporal_analysis.csv")
print("\nYou can now use these insights for your project assessment!")
print("=" * 80)
