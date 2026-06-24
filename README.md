# ALX Data Analysis — SQL & Data Projects

A collection of SQL and data analysis projects completed as part of the **ALX/ExploreAI Data Analytics programme**. Work spans database querying, water access analysis, and integrated data projects across multiple real-world datasets.

---

## Projects

### 1. Maji Ndogo Water Services Analysis
**Notebook:** `Md_water_services.ipynb`  
**Database:** `md_water_services.db`

End-to-end analysis of water access across Maji Ndogo's provinces and towns. Covers:
- Querying water source types and visit records
- Identifying pollution and quality issues
- Aggregating access statistics by province and town
- Surfacing actionable insights for infrastructure improvement

---

### 2. Water Access Project (Parts 1 & 2)
**Folders:** `water_access_project/`, `water_access_project Part 2/`

Extended investigation into water access inequality. Work includes:
- Multi-table joins across sources, visits, and population data
- Window functions for ranking water sources
- Conditional aggregation to profile underserved communities
- Building summary reports for decision-making

---

### 3. SQL Exam
**Notebook:** `SQL_Exam.ipynb`

Demonstrates core SQL competency across:
- Aggregate functions (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`)
- `GROUP BY`, `HAVING`, `ORDER BY`
- Subqueries and nested SELECT statements
- Window functions (`ROW_NUMBER`, `RANK`, `LEAD`, `LAG`)
- NULL handling and conditional logic (`CASE WHEN`)

---

### 4. Final Exam — ALX
**Folder:** `final exam alx/`

Capstone assessment covering the full data analysis workflow — data extraction via SQL, cleaning, and insight generation across integrated datasets.

---

## Datasets

The `.db` files are not included in this repo. Download and place them in the project root before running any notebook.

| Database | Description | Source |
|---|---|---|
| `md_water_services.db` | Maji Ndogo water infrastructure data | ALX/ExploreAI |
| `united_nations.db` | UN socioeconomic indicators | ALX/ExploreAI |
| `chinook.db` | Digital music store — invoices, tracks, customers | [chinook-database](https://github.com/lerocha/chinook-database) |
| `Northwind.db` | Classic retail orders and suppliers dataset | [northwind-SQLite3](https://github.com/jpwhite3/northwind-SQLite3) |
| `SoftDevEmployees.db` | Software developer employee records | ALX/ExploreAI |

---

## Tech Stack

| Tool | Use |
|---|---|
| Python 3 | Core language |
| Pandas | Data manipulation |
| SQLite3 | Database engine |
| Jupyter Notebook | Interactive analysis environment |
| Matplotlib / Seaborn | Visualisation |

---

## Setup

```bash
# Clone the repo
git clone https://github.com/derrrick-ryan-giggs/alx-data-analysis.git
cd alx-data-analysis

# Install dependencies
pip install pandas matplotlib seaborn jupyter

# Launch Jupyter
jupyter notebook
```

Place the `.db` files in the same root folder before opening any notebook.

---

## Certification

These projects were completed as part of the **ALX Data Analytics** programme by ExploreAI.  
**Credential ID:** 9PSxB3EHm2

---

## Author

**Ryan** — Data Engineer  

[LinkedIn](https://www.linkedin.com/in/ryan-giggs-a19330265/) · [GitHub](https://github.com/Derrick-Ryan-Giggs)
