# Excel Primer: Data Engineer × Data Scientist × Financial Analyst

> A practical, role-blended reference for professionals who live across data pipelines, analytical models, and financial reporting.

---

## Table of Contents

1. [Workbook Setup & Navigation](#1-workbook-setup--navigation)
2. [Data Import & Cleaning](#2-data-import--cleaning)
3. [Core Formulas for Data Engineering](#3-core-formulas-for-data-engineering)
4. [Statistical & Data Science Functions](#4-statistical--data-science-functions)
5. [Financial Analysis Functions](#5-financial-analysis-functions)
6. [Lookup & Reference Mastery](#6-lookup--reference-mastery)
7. [Power Query (ETL in Excel)](#7-power-query-etl-in-excel)
8. [PivotTables & PivotCharts](#8-pivottables--pivotcharts)
9. [Data Visualization](#9-data-visualization)
10. [Dynamic Arrays & Spill Formulas](#10-dynamic-arrays--spill-formulas)
11. [Financial Modeling Standards](#11-financial-modeling-standards)
12. [Keyboard Shortcuts Cheat Sheet](#12-keyboard-shortcuts-cheat-sheet)
13. [Pro Tips & Common Pitfalls](#13-pro-tips--common-pitfalls)

---

## 1. Workbook Setup & Navigation

### Structuring a Professional Workbook

| Sheet Tab | Purpose |
|-----------|---------|
| `README` | Document assumptions, data sources, version history |
| `RAW_DATA` | Untouched source data — never edit here |
| `CLEAN_DATA` | Transformed, validated data ready for analysis |
| `ANALYSIS` | Calculations, summaries, statistical models |
| `FINANCIALS` | P&L, DCF, KPI dashboards |
| `OUTPUT` | Charts, tables for stakeholders |

### Steps: Freeze Panes for Large Datasets
1. Click the cell **below and to the right** of the rows/columns to freeze (e.g., B2 to freeze row 1 and column A)
2. Go to **View → Freeze Panes → Freeze Panes**
3. To unfreeze: **View → Freeze Panes → Unfreeze Panes**

### Steps: Name a Range (for readable formulas)
1. Select the cell or range
2. Click the **Name Box** (top-left, shows cell address)
3. Type a name (e.g., `Revenue_2024`) and press **Enter**
4. Use in formulas: `=SUM(Revenue_2024)`

### Steps: Protect a Sheet (lock raw data)
1. Go to **Review → Protect Sheet**
2. Set a password (optional)
3. Check only the actions you want to allow (e.g., "Select unlocked cells")
4. Click **OK**

---

## 2. Data Import & Cleaning

### Steps: Import CSV Data
1. Go to **Data → Get Data → From Text/CSV**
2. Browse to your file and click **Import**
3. In the preview dialog, confirm delimiter and data types
4. Click **Load** (to sheet) or **Transform Data** (to Power Query)

### Steps: Remove Duplicates
1. Select your data range or click inside a table
2. Go to **Data → Remove Duplicates**
3. Check the columns to evaluate for duplicates
4. Click **OK** — Excel reports how many rows were removed

### Steps: Text to Columns (split delimited fields)
1. Select the column with combined data (e.g., "FirstName LastName")
2. Go to **Data → Text to Columns**
3. Choose **Delimited** → click **Next**
4. Select delimiter (Space, Comma, Pipe, etc.) → click **Next**
5. Set column data formats → click **Finish**

### Essential Cleaning Formulas

```
Remove leading/trailing spaces:    =TRIM(A2)
Standardize case:                  =PROPER(A2) / =UPPER(A2) / =LOWER(A2)
Remove non-printable chars:        =CLEAN(A2)
Combine TRIM + CLEAN:              =TRIM(CLEAN(A2))
Replace a substring:               =SUBSTITUTE(A2, "old_text", "new_text")
Extract left N characters:         =LEFT(A2, 4)
Extract right N characters:        =RIGHT(A2, 5)
Extract from middle:               =MID(A2, start_pos, num_chars)
Find position of character:        =FIND("_", A2)
Check if cell is blank:            =ISBLANK(A2)
Convert text to number:            =VALUE(A2)  or  =A2*1
Convert number to text:            =TEXT(A2, "0.00")
```

### Steps: Flash Fill (pattern-based auto-fill)
1. Type the desired output manually in the first 1–2 rows next to your data
2. Press **Ctrl + E** — Excel detects the pattern and fills the rest
3. If the result is wrong, adjust your example and repeat

---

## 3. Core Formulas for Data Engineering

### Conditional Logic

```excel
Basic IF:
=IF(A2 > 100, "High", "Low")

Nested IF (up to 3 levels — use IFS beyond that):
=IF(A2 >= 90, "A", IF(A2 >= 70, "B", IF(A2 >= 50, "C", "F")))

IFS (cleaner multi-condition):
=IFS(A2 >= 90, "A", A2 >= 70, "B", A2 >= 50, "C", TRUE, "F")

AND / OR conditions:
=IF(AND(A2 > 50, B2 = "Active"), "Qualify", "No")
=IF(OR(A2 = "NY", A2 = "CA"), "Priority", "Standard")

Handle errors gracefully:
=IFERROR(A2/B2, 0)
=IFNA(VLOOKUP(A2, Table1, 2, 0), "Not Found")
```

### Counting & Aggregation

```excel
Count non-empty cells:            =COUNTA(A2:A1000)
Count cells meeting criteria:     =COUNTIF(A2:A100, "Active")
Count multi-criteria:             =COUNTIFS(A2:A100, "Active", B2:B100, ">50")
Sum with one condition:           =SUMIF(A2:A100, "West", C2:C100)
Sum with multiple conditions:     =SUMIFS(C2:C100, A2:A100, "West", B2:B100, "Q1")
Average with condition:           =AVERAGEIF(A2:A100, "Active", B2:B100)
Max/Min with condition:           =MAXIFS(C2:C100, A2:A100, "West")
                                  =MINIFS(C2:C100, A2:A100, "West")
```

### Date & Time Operations

```excel
Today's date:                     =TODAY()
Current datetime:                 =NOW()
Extract year/month/day:           =YEAR(A2)  =MONTH(A2)  =DAY(A2)
Day of week (1=Sun):              =WEEKDAY(A2)
Days between dates:               =DATEDIF(start_date, end_date, "D")
Add N business days:              =WORKDAY(A2, 30)
End of month:                     =EOMONTH(A2, 0)   ' same month
                                  =EOMONTH(A2, 1)   ' next month end
Quarter from date:                ="Q" & ROUNDUP(MONTH(A2)/3, 0)
Format date as text:              =TEXT(A2, "YYYY-MM-DD")
```

---

## 4. Statistical & Data Science Functions

### Descriptive Statistics

```excel
Mean:                             =AVERAGE(A2:A1000)
Median:                           =MEDIAN(A2:A1000)
Mode (single):                    =MODE(A2:A1000)
Standard deviation (sample):      =STDEV(A2:A1000)
Standard deviation (population):  =STDEVP(A2:A1000)
Variance (sample):                =VAR(A2:A1000)
Skewness:                         =SKEW(A2:A1000)
Kurtosis:                         =KURT(A2:A1000)
Percentile (0–1):                 =PERCENTILE(A2:A1000, 0.95)   ' 95th
Quartile (0–4):                   =QUARTILE(A2:A1000, 1)        ' Q1
Rank of a value:                  =RANK(A2, A$2:A$1000, 0)      ' 0=desc
Normalize (z-score):              =(A2 - AVERAGE(A$2:A$1000)) / STDEV(A$2:A$1000)
```

### Correlation & Regression

```excel
Pearson correlation:              =CORREL(A2:A100, B2:B100)
R-squared from correlation:       =CORREL(A2:A100, B2:B100)^2
Covariance (sample):              =COVARIANCE.S(A2:A100, B2:B100)

Linear regression slope:          =SLOPE(known_y, known_x)
Linear regression intercept:      =INTERCEPT(known_y, known_x)
Predict Y for given X:            =FORECAST.LINEAR(x_value, known_y, known_x)

R² via LINEST (array formula):
=INDEX(LINEST(known_y, known_x, TRUE, TRUE), 3, 1)
```

### Steps: Run Descriptive Statistics (Analysis ToolPak)
1. Go to **File → Options → Add-ins**
2. At the bottom, select **Excel Add-ins** and click **Go**
3. Check **Analysis ToolPak** → click **OK**
4. Go to **Data → Data Analysis → Descriptive Statistics**
5. Set Input Range, check **Summary Statistics**, choose output location → click **OK**

### Steps: Create a Histogram
1. Enable Analysis ToolPak (steps above)
2. Go to **Data → Data Analysis → Histogram**
3. Set **Input Range** (your data) and optional **Bin Range**
4. Check **Chart Output** → click **OK**
5. Alternatively, select data → **Insert → Recommended Charts → Histogram**

---

## 5. Financial Analysis Functions

### Time Value of Money

```excel
Net Present Value:                =NPV(discount_rate, cash_flow_range)
                                  Note: Add initial investment separately:
                                  =NPV(0.10, B3:B7) + B2   ' B2 = negative initial invest

Internal Rate of Return:          =IRR(cash_flow_range)
Modified IRR:                     =MIRR(cash_flows, finance_rate, reinvest_rate)

Future Value:                     =FV(rate, nper, pmt, [pv], [type])
Present Value:                    =PV(rate, nper, pmt, [fv], [type])
Payment (loan):                   =PMT(rate/12, nper*12, -loan_amount)
Number of periods:                =NPER(rate, pmt, pv)
Interest rate per period:         =RATE(nper, pmt, pv)

XNPV (irregular cash flows):      =XNPV(rate, values, dates)
XIRR (irregular cash flows):      =XIRR(values, dates)
```

### Financial Ratios (Inline Formulas)

```excel
Revenue Growth:                   =(C2-B2)/B2
Gross Margin:                     =(Revenue - COGS) / Revenue
EBITDA Margin:                    =EBITDA / Revenue
Net Margin:                       =Net_Income / Revenue
Return on Equity:                 =Net_Income / Avg_Equity
Current Ratio:                    =Current_Assets / Current_Liabilities
Debt-to-Equity:                   =Total_Debt / Total_Equity
EV/EBITDA:                        =Enterprise_Value / EBITDA
P/E Ratio:                        =Share_Price / EPS
Days Sales Outstanding (DSO):     =(Accounts_Receivable / Revenue) * 365
```

### Depreciation Functions

```excel
Straight-Line:                    =SLN(cost, salvage, life)
Double-Declining Balance:         =DDB(cost, salvage, life, period)
Sum-of-Years Digits:              =SYD(cost, salvage, life, period)
Variable Declining Balance:       =VDB(cost, salvage, life, start_period, end_period)
```

### Steps: Build a Simple DCF Model
1. **Set up assumptions**: Discount rate, terminal growth rate in named cells
2. **Project free cash flows** (FCF) across 5 years with growth formulas: `=B5*(1+$B$2)`
3. **Discount each FCF**: `=B5 / (1+$B$1)^B1_year_number`
4. **Terminal Value**: `=FCF_Year5 * (1 + terminal_growth) / (discount_rate - terminal_growth)`
5. **PV of Terminal Value**: `=Terminal_Value / (1+discount_rate)^5`
6. **Enterprise Value**: `=SUM(discounted_FCFs) + PV_Terminal_Value`

---

## 6. Lookup & Reference Mastery

### XLOOKUP (Modern — Excel 365/2021)

```excel
Basic lookup:
=XLOOKUP(lookup_value, lookup_array, return_array)

With fallback if not found:
=XLOOKUP(A2, Table[ID], Table[Name], "Not Found")

Approximate match (sorted data):
=XLOOKUP(A2, price_table[min], price_table[tier], "Unknown", 1)

Last match (reverse search):
=XLOOKUP(A2, Table[ID], Table[Date], , , -1)

Return multiple columns:
=XLOOKUP(A2, Table[ID], Table[[Name]:[Region]])
```

### INDEX / MATCH (Universal — all Excel versions)

```excel
Basic (replaces VLOOKUP):
=INDEX(return_range, MATCH(lookup_value, lookup_range, 0))

Two-way lookup (row + column):
=INDEX(data_range, MATCH(row_value, row_headers, 0), MATCH(col_value, col_headers, 0))

With error handling:
=IFERROR(INDEX(D:D, MATCH(A2, B:B, 0)), "Not Found")
```

### VLOOKUP vs XLOOKUP vs INDEX/MATCH

| Feature | VLOOKUP | INDEX/MATCH | XLOOKUP |
|---------|---------|-------------|---------|
| Lookup direction | Right only | Any direction | Any direction |
| Column shifts | Breaks | Stable | Stable |
| Multiple returns | No | No | Yes |
| Excel version | All | All | 365/2021+ |
| Speed (large data) | Slower | Fast | Fast |
| **Recommended** | Legacy | ✅ Universal | ✅ Modern |

---

## 7. Power Query (ETL in Excel)

> Power Query is Excel's built-in ETL tool. Think of it as a no-code pipeline.

### Steps: Open Power Query
1. Go to **Data → Get Data → Launch Power Query Editor**
2. Or: **Data → From Table/Range** after selecting your data

### Steps: Connect to a Data Source
1. **Data → Get Data** → select your source:
   - From File: Excel, CSV, JSON, XML, Folder
   - From Database: SQL Server, Access, Oracle
   - From Web: URL endpoint (REST APIs, public data)
2. Authenticate if required
3. Select tables/sheets → click **Transform Data**

### Common Power Query Transformations (M Language)

| Action | Steps in UI | M Code Equivalent |
|--------|------------|-------------------|
| Remove columns | Right-click column → Remove | `Table.RemoveColumns(...)` |
| Filter rows | Column dropdown → Number Filters | `Table.SelectRows(...)` |
| Change type | Transform → Data Type | `Table.TransformColumnTypes(...)` |
| Add column | Add Column → Custom Column | `Table.AddColumn(...)` |
| Group by | Transform → Group By | `Table.Group(...)` |
| Pivot column | Transform → Pivot Column | `Table.Pivot(...)` |
| Unpivot | Select cols → Unpivot Other Columns | `Table.UnpivotOtherColumns(...)` |
| Merge queries | Home → Merge Queries (SQL JOIN) | `Table.NestedJoin(...)` |
| Append queries | Home → Append Queries (SQL UNION) | `Table.Combine(...)` |

### Steps: Refresh a Power Query
1. Click inside the query output table
2. Press **Ctrl + Alt + F5** to refresh all, or **Data → Refresh All**
3. For scheduled refresh, publish to Power BI or use VBA automation

---

## 8. PivotTables & PivotCharts

### Steps: Create a PivotTable
1. Click anywhere inside your clean data table
2. Go to **Insert → PivotTable**
3. Confirm the range and choose **New Worksheet** → click **OK**
4. In the **PivotTable Fields** pane:
   - Drag categorical fields to **Rows** (e.g., Region, Category)
   - Drag date fields to **Columns** (or Rows for time series)
   - Drag numeric fields to **Values** (e.g., Revenue, Quantity)
5. Change aggregation: Click field in Values → **Value Field Settings** → choose Sum, Count, Average, etc.

### Steps: Add a Calculated Field
1. Click inside the PivotTable
2. Go to **PivotTable Analyze → Fields, Items & Sets → Calculated Field**
3. Name it (e.g., `Profit Margin`)
4. Enter formula using existing field names: `= Profit / Revenue`
5. Click **Add → OK**

### Steps: Create a PivotChart
1. Click inside an existing PivotTable
2. Go to **PivotTable Analyze → PivotChart**
3. Choose chart type → click **OK**
4. The chart will filter dynamically with the PivotTable slicers

### Steps: Add Slicers (interactive filters)
1. Click inside the PivotTable
2. Go to **Insert → Slicer**
3. Check the fields you want as filter buttons → click **OK**
4. Click slicer buttons to filter; hold **Ctrl** for multi-select
5. Connect one slicer to multiple PivotTables: Right-click slicer → **Report Connections**

---

## 9. Data Visualization

### Choosing the Right Chart

| Use Case | Chart Type |
|----------|-----------|
| Compare categories | Clustered Bar / Column |
| Show trend over time | Line Chart |
| Part-of-whole | Pie / Donut (≤5 categories) |
| Distribution of values | Histogram / Box & Whisker |
| Correlation between variables | Scatter Plot |
| Multi-metric comparison | Radar / Spider Chart |
| Financial OHLC data | Stock Chart / Candlestick |
| Hierarchical data | Treemap / Sunburst |
| Pipeline / funnel KPIs | Funnel Chart |
| Geographic data | Map Chart (Excel 365) |
| Two datasets, different scales | Combo Chart (dual axis) |

### Steps: Create a Combination Chart (Dual Axis)
1. Select your data (e.g., Revenue and Margin %)
2. Go to **Insert → Recommended Charts → All Charts → Combo**
3. For each series, choose chart type (e.g., Column for Revenue, Line for Margin)
4. Check **Secondary Axis** for the series with a different scale (e.g., Margin %)
5. Click **OK**, then format each axis independently

### Steps: Add a Trendline to a Chart
1. Click on the data series in the chart
2. Right-click → **Add Trendline**
3. Choose type: Linear, Exponential, Logarithmic, Polynomial, Moving Average
4. Check **Display Equation on chart** and **Display R-squared value**
5. Click **Close**

### Steps: Create a Dynamic Chart with Named Ranges
1. Define dynamic named ranges using OFFSET:
   `=OFFSET(Sheet1!$A$2, 0, 0, COUNTA(Sheet1!$A:$A)-1, 1)`
2. Create chart from static data first
3. Click on chart → **Select Data → Edit** each series
4. Replace hard-coded ranges with your named ranges
5. Chart now auto-expands as data grows

---

## 10. Dynamic Arrays & Spill Formulas

> Available in Excel 365 and Excel 2021. These eliminate the need for many array formulas.

### Key Dynamic Array Functions

```excel
Sort a range (ascending by col 1):
=SORT(A2:C100)

Sort by specific column descending:
=SORT(A2:C100, 2, -1)   ' col 2, desc

Filter to matching rows:
=FILTER(A2:C100, B2:B100="Active")

Filter with multiple conditions:
=FILTER(A2:C100, (B2:B100="Active") * (C2:C100 > 1000))

Get unique values:
=UNIQUE(A2:A100)

Unique from multiple columns:
=UNIQUE(A2:B100, FALSE)   ' FALSE = unique rows

Random sample (N rows without replacement):
=TAKE(SORTBY(data, RANDARRAY(ROWS(data))), N)

Sequence of numbers:
=SEQUENCE(10)           ' 1 to 10
=SEQUENCE(5, 3, 0, 10)  ' 5 rows, 3 cols, start=0, step=10

Dynamic rank table:
=SORT(FILTER(Table1, Table1[Region]="West"), 3, -1)
```

### XLOOKUP + Dynamic Arrays (Powerful Combo)

```excel
' Return all rows where ID matches (one-to-many)
=FILTER(Table1, Table1[CustomerID] = A2)

' Stack multiple filtered results:
=VSTACK(
   FILTER(Table1, Table1[Region]="North"),
   FILTER(Table1, Table1[Region]="South")
)
```

---

## 11. Financial Modeling Standards

### Color Coding Convention (Industry Standard)

| Color | Usage |
|-------|-------|
| 🔵 **Blue text** | Hardcoded inputs — numbers you change per scenario |
| ⚫ **Black text** | All formulas and calculations |
| 🟢 **Green text** | Links from other sheets within the same workbook |
| 🔴 **Red text** | External links to other files |
| 🟡 **Yellow background** | Key assumptions needing attention / cells to update |

### Number Formatting Rules

```
Currency (millions):   $#,##0,,"M"   →   shows $1.5M
Currency (thousands):  $#,##0,"K"    →   shows $1,500K
With negatives:        $#,##0;($#,##0);-
Percentages:           0.0%           →   one decimal
Valuation multiples:   0.0x           →   e.g., 12.5x
Years as text:         Format as text or use TEXT() to prevent comma formatting
```

### Steps: Build a Three-Statement Model (Skeleton)
1. **Income Statement** tab:
   - Revenue → COGS → Gross Profit → OPEX → EBITDA → D&A → EBIT → Interest → EBT → Tax → Net Income
2. **Balance Sheet** tab:
   - Assets (Cash, AR, Inventory, PP&E) = Liabilities (AP, Debt) + Equity (Retained Earnings)
   - Link Cash from Cash Flow Statement; plug Retained Earnings from Net Income
3. **Cash Flow Statement** tab:
   - Start with Net Income → add back non-cash (D&A) → Working Capital changes → CapEx → Financing
   - Ending Cash links back to Balance Sheet
4. **Check cell**: `=IF(Total_Assets = Total_Liabilities_Equity, "✅ BALANCED", "❌ ERROR")`

### Sensitivity Analysis (Data Tables)

**Steps: One-Variable Data Table**
1. Set up a column of input values (e.g., discount rates: 8%, 9%, 10%)
2. Place the formula you want to test one row above and one column to the right of inputs
3. Select the entire range (inputs + formula cell)
4. Go to **Data → What-If Analysis → Data Table**
5. Set **Column input cell** to your assumption cell → click **OK**

**Steps: Two-Variable Data Table**
1. Put one set of inputs in a column, another set in a row
2. Place the formula at the intersection (top-left of the grid)
3. Select the entire table
4. **Data → What-If Analysis → Data Table**
5. Set **Row input cell** and **Column input cell** → click **OK**

---

## 12. Keyboard Shortcuts Cheat Sheet

### Navigation

| Shortcut | Action |
|----------|--------|
| `Ctrl + End` | Go to last used cell |
| `Ctrl + Home` | Go to cell A1 |
| `Ctrl + Arrow` | Jump to edge of data region |
| `Ctrl + Shift + Arrow` | Select to edge of data region |
| `Ctrl + Page Up/Down` | Switch between sheets |
| `F5` or `Ctrl + G` | Go To (navigate to named ranges) |
| `Ctrl + F` | Find |
| `Ctrl + H` | Find & Replace |

### Data Entry & Editing

| Shortcut | Action |
|----------|--------|
| `Ctrl + D` | Fill Down |
| `Ctrl + R` | Fill Right |
| `Ctrl + ;` | Insert today's date |
| `Ctrl + Shift + ;` | Insert current time |
| `Ctrl + Enter` | Fill same value to multiple selected cells |
| `Alt + Enter` | New line within a cell |
| `F2` | Edit active cell |
| `Ctrl + Z / Y` | Undo / Redo |
| `Ctrl + E` | Flash Fill |

### Formatting

| Shortcut | Action |
|----------|--------|
| `Ctrl + 1` | Open Format Cells dialog |
| `Ctrl + Shift + $` | Currency format |
| `Ctrl + Shift + %` | Percentage format |
| `Ctrl + Shift + #` | Date format |
| `Ctrl + B / I / U` | Bold / Italic / Underline |
| `Alt + H + H` | Highlight color picker |
| `Alt + H + FC` | Font color picker |

### Formulas & Analysis

| Shortcut | Action |
|----------|--------|
| `F4` | Toggle absolute/relative reference ($) |
| `Ctrl + Shift + Enter` | Enter legacy array formula |
| `Ctrl + `` ` | Toggle show formulas |
| `Alt + =` | AutoSum |
| `F9` | Evaluate selected part of formula |
| `Ctrl + [` | Trace precedents (go to referenced cells) |
| `Ctrl + Shift + {` | Select all cells referenced by formula |

---

## 13. Pro Tips & Common Pitfalls

### ✅ Data Engineering Best Practices

- **Always keep RAW data untouched.** Work in a separate tab; use Power Query to transform.
- **Use Tables (`Ctrl + T`)** for all datasets. Tables auto-expand formulas, work with XLOOKUP, and make Power Query connections stable.
- **Document data lineage.** Add a `README` sheet noting source, date pulled, and any known issues.
- **Avoid merged cells** in data ranges — they break sorting, filtering, and PivotTables.
- **Use data validation** to enforce consistent categories: **Data → Data Validation → List**.

### ✅ Data Science Best Practices

- **Normalize before statistics.** Use z-scores or min-max scaling for fair comparisons.
- **Label outliers** using IQR: flag values where `value < Q1 - 1.5*IQR` or `value > Q3 + 1.5*IQR`.
- **Use scatter plots + trendlines** to visually validate correlation before computing `CORREL()`.
- **Always show n (sample size)** alongside averages and percentages.
- **LINEST returns an array.** Wrap it in `INDEX()` to extract individual coefficients.

### ✅ Financial Analysis Best Practices

- **Separate assumptions from formulas.** Hard-code only in dedicated assumption rows/cells (blue text).
- **Never hardcode a number in a formula.** Use `=B5 * (1 + $B$2)` not `=B5 * 1.05`.
- **Always build a balance check.** A model that doesn't balance has an error somewhere.
- **Use IFERROR() sparingly.** Hiding errors can mask real model problems.
- **Date your models.** Add version number and last-modified date to the README tab.

### ⚠️ Common Pitfalls to Avoid

| Pitfall | Problem | Fix |
|---------|---------|-----|
| VLOOKUP with column number | Breaks when columns are inserted | Switch to XLOOKUP or INDEX/MATCH |
| `=A1+B1` instead of `=SUM(A1:B1)` | Can't drag to expand; error-prone | Always use proper aggregation functions |
| Mixing data types in a column | Breaks sorting, filtering, COUNTIF | Standardize via Text to Columns or VALUE() |
| Hardcoded dates in formulas | Model goes stale | Use `=TODAY()` or cell references |
| Circular reference in cash model | Freezes iteration or gives wrong result | Use Excel's iterative calculation setting with caution |
| SUM range not adjusted as rows added | Misses new data | Use structured Table references: `=SUM(Table1[Revenue])` |
| NPV formula applied to all cash flows | NPV() assumes flows start at period 1, not 0 | Exclude Year 0 from NPV range; add it manually |

---

## Quick Reference Card

### Formulas by Role

| Role | Go-To Functions |
|------|----------------|
| **Data Engineer** | `TRIM`, `CLEAN`, `TEXT`, `SUBSTITUTE`, `COUNTIFS`, `SUMIFS`, `IFERROR`, Power Query, `UNIQUE`, `FILTER` |
| **Data Scientist** | `AVERAGE`, `STDEV`, `CORREL`, `PERCENTILE`, `QUARTILE`, `FORECAST.LINEAR`, `SLOPE`, `INTERCEPT`, `NORM.DIST`, `RANK` |
| **Financial Analyst** | `NPV`, `IRR`, `XNPV`, `XIRR`, `PMT`, `FV`, `PV`, `SUMIFS`, `IFERROR`, `INDEX/MATCH`, Data Tables, `SLN`, `DDB` |

---

*Last updated: May 2026 | Compatible with Excel 365, Excel 2021, Excel 2019 (dynamic arrays require 365/2021)*
