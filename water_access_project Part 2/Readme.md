# Water Access Data Analysis Project

## Overview
This project analyzes global water access data from 2000-2020, focusing on safe and affordable drinking water access across different regions and the rural-urban divide.

## Folder Structure

```
water_access_project Part 2/
│
├── Estimates of the use of water (2000-2020).csv  (original data)
├── Regions.csv                                     (original data)
│
├── scripts/                         (Python scripts)
│   ├── water_data_cleaning.py
│   └── water_data_analysis.py
│
├── cleaned_data/                    (All cleaned CSV outputs)
│   ├── water_access_cleaned.csv
│   ├── regional_summary_statistics.csv
│   ├── yearly_trends.csv
│   ├── water_access_2020.csv
│   ├── data_dictionary.csv
│   ├── country_rankings_latest.csv
│   └── temporal_analysis.csv
│
├── visualizations/                  (All PNG plots)
│   ├── temporal_trends.png
│   ├── regional_comparison.png
│   ├── correlation_heatmap.png
│   └── top_bottom_performers.png
│
└── reports/                         (Text reports)
    ├── data_cleaning_summary.txt
    └── analysis_insights_report.txt
```

## Dataset Description

### 1. Estimates of the use of water (2000-2020).csv
Contains water access statistics for countries worldwide with the following columns:

**Demographic Data:**
- `name`: Country name
- `year`: Year of observation (2000-2020)
- `pop_n`: National population (thousands)
- `pop_u`: Urban population (thousands)

**National Level Water Access (%):**
- `wat_bas_n`: % with at least basic water services
- `wat_lim_n`: % with limited water services
- `wat_unimp_n`: % with unimproved water services
- `wat_sur_n`: % using surface water

**Rural Level Water Access (%):**
- `wat_bas_r`: % with at least basic water services
- `wat_lim_r`: % with limited water services
- `wat_unimp_r`: % with unimproved water services
- `wat_sur_r`: % using surface water

**Urban Level Water Access (%):**
- `wat_bas_u`: % with at least basic water services
- `wat_lim_u`: % with limited water services
- `wat_unimp_u`: % with unimproved water services
- `wat_sur_u`: % using surface water

### 2. Regions.csv
Maps countries to their geographic regions:
- `name`: Country name
- `region`: Geographic region



## Installation

Since you already have **Anaconda** which comes with Jupyter Notebook installed , you don't need to install any additional packages! All required libraries are already included:
- pandas
- numpy
- matplotlib
- seaborn
- scipy

## Setup Instructions

### 1. Create Folder Structure

In your project directory, create a `scripts` folder:

```bash
cd ~/Desktop/ALX\ Data\ Analysis/water_access_project\ Part\ 2
mkdir scripts
```

### 2. Save the Scripts

Save the two Python scripts to the `scripts/` folder:
- `water_data_cleaning.py` → `scripts/water_data_cleaning.py`
- `water_data_analysis.py` → `scripts/water_data_analysis.py`

Your directory should now look like:
```
water_access_project Part 2/
├── Estimates of the use of water (2000-2020).csv
├── Regions.csv
└── scripts/
    ├── water_data_cleaning.py
    └── water_data_analysis.py
```

## Usage

### Step 1: Data Cleaning and Transformation

Navigate to your project directory and run the cleaning script:

```bash
cd ~/Desktop/ALX\ Data\ Analysis/water_access_project\ Part\ 2
python scripts/water_data_cleaning.py
```

This script will:
- Create `cleaned_data/`, `visualizations/`, and `reports/` folders
- Load both CSV files
- Handle missing values (convert 'null' strings to NaN)
- Convert data types
- Check for duplicates
- Merge datasets
- Create new features:
  - Rural and urban population calculations
  - Unserved population estimates
  - Access level categories
  - Rural-urban gap metrics
  - Year-over-year improvements
- Generate summary statistics
- Save cleaned data to `cleaned_data/` folder

**Output Files (in cleaned_data/):**
1. `water_access_cleaned.csv` - Main cleaned dataset
2. `regional_summary_statistics.csv` - Regional summaries
3. `yearly_trends.csv` - Year-over-year trends
4. `water_access_2020.csv` - Latest year data
5. `data_dictionary.csv` - Column descriptions

**Output Report (in reports/):**
- `data_cleaning_summary.txt` - Detailed cleaning summary

### Step 2: Analysis and Visualization

After cleaning, run the analysis script:

```bash
python scripts/water_data_analysis.py
```

This script will:
- Load cleaned data from `cleaned_data/` folder
- Perform exploratory data analysis
- Generate temporal trend analysis
- Compare regional differences
- Analyze rural vs urban access
- Create correlation analysis
- Perform statistical tests (ANOVA)
- Generate comprehensive visualizations (saved to `visualizations/` folder)
- Create an insights report (saved to `reports/` folder)

**Output Files (in cleaned_data/):**
1. `country_rankings_latest.csv` - Country rankings for latest year
2. `temporal_analysis.csv` - Time series statistics

**Visualizations (in visualizations/):**
1. `temporal_trends.png` - Four-panel time series analysis
2. `regional_comparison.png` - Regional comparisons
3. `correlation_heatmap.png` - Variable correlations
4. `top_bottom_performers.png` - Best and worst countries

**Report (in reports/):**
- `analysis_insights_report.txt` - Comprehensive insights

### Alternative: Using Jupyter Notebook

You can also run the analysis interactively in Jupyter:

```bash
jupyter notebook
```

Then create a new notebook and run the scripts cell by cell, or import the cleaned data:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv('cleaned_data/water_access_cleaned.csv')

# Your analysis here
df.head()
df.describe()
# etc.
```

## Key Features Created

### Calculated Fields:
1. **pop_r**: Rural population (pop_n - pop_u)
2. **pop_r_pct**: Rural population percentage
3. **pop_u_pct**: Urban population percentage
4. **wat_bas_n_calc**: Calculated national access (weighted average)
5. **pop_without_basic_water**: People without basic water access (national)
6. **pop_r_without_basic_water**: Rural people without basic water
7. **pop_u_without_basic_water**: Urban people without basic water
8. **access_category_national/rural/urban**: Categorical access levels
9. **rural_urban_gap**: Urban minus rural access (%)
10. **has_significant_gap**: Boolean for gaps > 10%

### Access Categories:
- **Universal**: ≥99% access
- **High**: 90-99% access
- **Medium-High**: 75-90% access
- **Medium**: 50-75% access
- **Low**: <50% access

## Visualizations

### 1. Temporal Trends (temporal_trends.png)
Four-panel visualization showing:
- Global average water access trends (national, rural, urban)
- Total unserved population over time
- Regional trends
- Rural-urban gap evolution

### 2. Regional Comparison (regional_comparison.png)
Four-panel visualization showing:
- Distribution of access by region (box plots)
- Regional average access (bar chart)
- Rural vs urban access by region
- Unserved population by region

### 3. Correlation Heatmap (correlation_heatmap.png)
Shows relationships between:
- National, rural, and urban access
- Urban population percentage
- Rural-urban gap
- Total population

### 4. Top and Bottom Performers (top_bottom_performers.png)
- Top 10 countries with highest access
- Bottom 10 countries with lowest access

## Key Insights to Explore

1. **Global Progress**: Track improvements from 2000 to 2020
2. **Regional Disparities**: Compare access across regions
3. **Rural-Urban Divide**: Identify countries with largest gaps
4. **Population Impact**: Calculate people affected by water scarcity
5. **Trend Analysis**: Identify improving and declining countries

## Common Analysis Questions for MCQ Assessment

### Where to find answers:

1. **Which region has the highest/lowest average water access?**
   - Check `cleaned_data/regional_summary_statistics.csv`
   - Or see `reports/analysis_insights_report.txt` Section 2

2. **What's the global trend in water access?**
   - Check `cleaned_data/yearly_trends.csv`
   - Or see `visualizations/temporal_trends.png`

3. **Which countries improved/declined the most?**
   - Load `cleaned_data/water_access_cleaned.csv` and compare years
   - Use the `yoy_improvement` column for year-over-year changes

4. **What's the average rural-urban gap?**
   - Check `reports/analysis_insights_report.txt` Section 3
   - Or calculate from `rural_urban_gap` column in cleaned data

5. **How many people lack basic water access?**
   - Sum the `pop_without_basic_water` column (values in thousands)
   - See `reports/analysis_insights_report.txt` Section 1

6. **Which countries have the largest rural-urban gap?**
   - Check `reports/analysis_insights_report.txt` Section 3
   - Or sort `cleaned_data/water_access_2020.csv` by `rural_urban_gap`

7. **What percentage of countries have universal access (≥99%)?**
   - Count countries where `access_category_national == 'Universal'`
   - See the cleaned data file

8. **How has Sub-Saharan Africa's access changed?**
   - Filter `cleaned_data/yearly_trends.csv` for Sub-Saharan Africa
   - Compare earliest to latest year

## Tips for Project Success

1. **Data Quality Checks:**
   - Always check for missing values
   - Validate percentage calculations (should be 0-100)
   - Look for outliers or anomalies

2. **Feature Engineering:**
   - Create meaningful aggregations (regional, temporal)
   - Calculate per-capita and percentage metrics
   - Compare changes over time

3. **Visualization Best Practices:**
   - Use appropriate chart types
   - Include clear labels and titles
   - Choose color schemes wisely
   - Add context and interpretation

4. **Statistical Analysis:**
   - Test for significance when comparing groups
   - Calculate confidence intervals
   - Check for correlations

## Troubleshooting

### Issue: "FileNotFoundError"
- Ensure CSV files are in the same directory as scripts
- Check file names match exactly (case-sensitive)

### Issue: "ModuleNotFoundError"
- Install missing packages: `pip install [package_name] --break-system-packages`

### Issue: Plots not displaying
- Scripts save plots to files instead of displaying
- Check the `visualizations/` folder

### Issue: Encoding errors
- Ensure CSV files are UTF-8 encoded
- Try opening files with different encoding if needed

## Advanced Analysis Ideas

1. **Predict future trends** using time series analysis
2. **Cluster countries** based on access patterns
3. **Identify factors** correlated with high access (GDP, governance, etc.)
4. **Calculate SDG 6 progress** toward universal access
5. **Geospatial analysis** if you add coordinate data

## Contact & Support

For questions about the project or scripts:
- Review the comments in the Python scripts
- Check the generated insights report
- Refer to pandas/matplotlib documentation

## License

This project is for educational purposes (ALX Data Analysis).

---

**Last Updated**: February 2026
**Version**: 1.0
