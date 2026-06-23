# 📊 Multi-Touch Marketing Attribution & ROI Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![SQL](https://img.shields.io/badge/SQL-Attribution%20Logic-orange)
![Tableau](https://img.shields.io/badge/Tableau-Dashboard-blueviolet)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed%20App-red)
![Status](https://img.shields.io/badge/Project-Completed-success)

---

## 🚀 Live Project Links

🔗 **GitHub Repository:**
https://github.com/chai0405-hub/Infotact_data_analytics

🌐 **Live Streamlit Dashboard:**
https://infotactdataanalytics-0405.streamlit.app/

---

## 📌 Project Title

**Multi-Touch Marketing Attribution and ROI Dashboard**

---

## 👤 Project Information

| Field            | Details                                                      |
| ---------------- | ------------------------------------------------------------ |
| **Name**         | Chaitanya Pawar                                              |
| **Organization** | Infotact Solutions & Co.                                     |
| **Domain**       | Data Analytics / Marketing Analytics                         |
| **Project Type** | Internship Project                                           |
| **Tools Used**   | Python, Pandas, NumPy, SQL, Tableau, Streamlit, Google Colab |
| **Deployment**   | Streamlit Community Cloud                                    |

---

## 🧠 Project Overview

Modern e-commerce and SaaS companies spend marketing budgets across multiple channels such as **Google Ads, Meta Ads, TikTok Ads, LinkedIn Ads, Email, Organic Search, Referral, and Direct traffic**.

However, customer journeys are not simple. A customer may interact with several marketing touchpoints before finally converting.

Example customer journey:

```text
Meta Ads → Organic Search → Email → Google Ads → Conversion
```

Traditional **Last-Click Attribution** gives all conversion credit to the final channel. This can lead to wrong budget decisions because earlier touchpoints may also influence the customer journey.

This project solves that problem by building a **Multi-Touch Marketing Attribution and ROI Dashboard** that compares different attribution models and calculates important marketing KPIs such as **ROAS**, **CAC**, **Attributed Revenue**, and **Attributed Conversions**.

---

## 🎯 Business Problem

Marketing teams need to understand:

* Which marketing channels generate the highest revenue?
* Which channels bring the best return on ad spend?
* Which channels have high customer acquisition cost?
* How does channel performance change under different attribution models?
* Which campaigns should receive more or less budget?

This project helps answer these questions using data analytics and interactive dashboarding.

---

## ✅ Business Objectives

The main objectives of this project are:

1. Clean and prepare marketing touchpoint data.
2. Identify converted customer journeys.
3. Build First-Touch, Last-Touch, and Linear Attribution models.
4. Calculate marketing KPIs such as ROAS and CAC.
5. Create channel-level and campaign-level performance analysis.
6. Build an interactive Streamlit dashboard.
7. Help marketing managers make better budget allocation decisions.

---

## 👥 User Personas

| Persona                     | Primary Need                                         | Dashboard Use                                          |
| --------------------------- | ---------------------------------------------------- | ------------------------------------------------------ |
| **Chief Marketing Officer** | Wants macro-level visibility of marketing efficiency | Reviews ROAS, CAC, revenue, and conversions by channel |
| **Performance Marketer**    | Wants campaign-level performance details             | Drills down into specific campaigns and channels       |
| **Data Analyst**            | Wants clean attribution logic and KPI outputs        | Uses Python, SQL, and processed datasets for analysis  |

---

## 🧾 Dataset Description

The project uses a marketing touchpoint dataset containing customer journey data.

### Key Dataset Columns

| Column                | Description                                       |
| --------------------- | ------------------------------------------------- |
| `event_id`            | Unique event identifier                           |
| `user_id`             | Unique customer/user identifier                   |
| `journey_id`          | Full journey of one customer                      |
| `session_id`          | Session-level identifier                          |
| `event_timestamp_utc` | Timestamp of customer interaction                 |
| `channel`             | Marketing channel                                 |
| `campaign`            | Campaign name                                     |
| `funnel_stage`        | Awareness, Consideration, Decision, or Purchase   |
| `ad_spend`            | Marketing cost                                    |
| `is_conversion`       | Conversion flag: 1 = converted, 0 = not converted |
| `conversion_value`    | Revenue generated from conversion                 |
| `device`              | Customer device                                   |
| `region`              | Customer region                                   |

---

## 📊 Dataset Snapshot

| Metric                   | Value |
| ------------------------ | ----: |
| Total Touchpoint Records | 1,926 |
| Total Columns            |    26 |
| Total Customer Journeys  |   500 |
| Converted Journeys       |   209 |
| Marketing Channels       |     8 |

---

## 🧹 Data Cleaning Process

Data cleaning was performed using **Python and Pandas**.

Steps performed:

1. Loaded the raw CSV dataset.
2. Converted timestamp columns into datetime format.
3. Converted `ad_spend` and `conversion_value` into numeric values.
4. Removed duplicate `event_id` records.
5. Sorted customer journeys by `journey_id` and `event_timestamp_utc`.
6. Saved the cleaned dataset for modeling and dashboarding.

Cleaned dataset:

```text
data/cleaned_multi_touch_attribution_dataset.csv
```

---

## 🔁 Attribution Models Used

### 1. First-Touch Attribution

The first marketing channel in a converted customer journey receives full credit.

```text
Google Ads → Email → Direct → Conversion
```

Credit goes to:

```text
Google Ads
```

---

### 2. Last-Touch Attribution

The final marketing channel before conversion receives full credit.

```text
Google Ads → Email → Direct → Conversion
```

Credit goes to:

```text
Direct
```

---

### 3. Linear Attribution

All touchpoints in the customer journey share credit equally.

```text
Google Ads → Email → Direct → Conversion
```

Credit is shared between:

```text
Google Ads + Email + Direct
```

---

## 📈 Key KPIs Calculated

| KPI                        | Formula                                         |
| -------------------------- | ----------------------------------------------- |
| **Total Spend**            | Sum of `ad_spend`                               |
| **Attributed Revenue**     | Revenue assigned by selected attribution model  |
| **Attributed Conversions** | Conversion credit assigned by attribution model |
| **ROAS**                   | Attributed Revenue ÷ Total Spend                |
| **CAC**                    | Total Spend ÷ Attributed Conversions            |

---

## 🧮 SQL Logic

SQL was used to demonstrate customer journey sequencing and attribution logic.

Important SQL concepts used:

* `ROW_NUMBER()`
* `PARTITION BY`
* `ORDER BY`
* Window functions
* First-touch ranking
* Last-touch ranking
* Channel-level aggregation
* ROAS and CAC calculation

SQL file:

```text
sql/02_attribution_model_queries.sql
```

---

## 📊 Dashboard Features

The deployed Streamlit dashboard includes:

### 1. Attribution Model Toggle

Users can switch between:

* First-Touch
* Last-Touch
* Linear

### 2. KPI Cards

The dashboard displays:

* Total Spend
* Attributed Revenue
* Attributed Conversions
* ROAS
* CAC

### 3. Channel Performance Charts

The dashboard includes:

* Channel Revenue
* ROAS by Channel
* CAC by Channel
* Conversions by Channel

### 4. ROI Scatter Plot

Shows the relationship between:

* Total Spend
* Attributed Revenue
* Attributed Conversions

### 5. Funnel Analysis

Shows customer funnel movement across:

```text
Awareness → Consideration → Decision → Purchase
```

### 6. Funnel Drop-off Table

Displays touchpoints and drop-off rates between funnel stages.

### 7. Campaign-Level Drilldown

Allows deeper analysis of campaign-level performance.

---

## 📸 Dashboard Preview

![Dashboard Screenshot](reports/dashboard_screenshot.png)

---

## 🗂️ Project Folder Structure

```text
Infotact_data_analytics
│
├── app.py
├── requirements.txt
├── README.md
│
├── data
│   ├── multi_touch_attribution_dataset.csv
│   ├── cleaned_multi_touch_attribution_dataset.csv
│   ├── attribution_model_output.csv
│   └── attribution_channel_summary.csv
│
├── notebooks
│   ├── 01_data_cleaning_and_eda.ipynb
│   └── 03_kpi_calculation_and_modeling.ipynb
│
├── sql
│   └── 02_attribution_model_queries.sql
│
├── dashboard
│   └── multi_touch_attribution_dashboard.twbx
│
├── reports
│   ├── dashboard_screenshot.png
│   ├── multi_touch_attribution_roi_report.docx
│   └── multi_touch_attribution_roi_report.pdf
│
└── presentation
    └── multi_touch_attribution_roi_presentation.pptx
```

---

## 🛠️ Tech Stack

| Tool             | Purpose                               |
| ---------------- | ------------------------------------- |
| **Python**       | Data cleaning and processing          |
| **Pandas**       | Data manipulation and KPI calculation |
| **NumPy**        | Numerical calculations                |
| **SQL**          | Attribution logic and journey ranking |
| **Google Colab** | Notebook-based development            |
| **Tableau**      | BI dashboard design                   |
| **Streamlit**    | Web app deployment                    |
| **GitHub**       | Version control and project hosting   |

---

## ▶️ How to Run Locally

### Step 1: Clone the Repository

```bash
git clone https://github.com/chai0405-hub/Infotact_data_analytics.git
```

### Step 2: Move Into the Project Folder

```bash
cd Infotact_data_analytics
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Streamlit App

```bash
streamlit run app.py
```

---

## 📦 Final Deliverables

| Deliverable       | Status    |
| ----------------- | --------- |
| Raw Dataset       | Completed |
| Cleaned Dataset   | Completed |
| Python Notebooks  | Completed |
| SQL Queries       | Completed |
| Tableau Dashboard | Completed |
| Streamlit Web App | Completed |
| Final Report      | Completed |
| Presentation PPT  | Completed |
| GitHub Repository | Completed |

---

## 🔍 Key Insights

Based on the analysis:

* Google Ads and Organic Search show strong attributed revenue contribution.
* Email shows strong ROAS due to low ad spend and meaningful conversion impact.
* Some paid channels show higher CAC and need budget monitoring.
* Attribution model selection changes how channel performance is interpreted.
* Linear Attribution gives a more balanced view of the full customer journey.

---

## 💡 Business Recommendations

1. Increase investment in channels with high ROAS and strong revenue contribution.
2. Monitor high-CAC channels before increasing budget.
3. Avoid depending only on Last-Touch Attribution.
4. Use Linear Attribution to understand the full customer journey.
5. Review campaign-level performance regularly to reduce wasted ad spend.
6. Use dashboard insights for smarter marketing budget allocation.

---

## 🌐 Deployment

The project is deployed using **Streamlit Community Cloud**.

Live app:

```text
https://infotactdataanalytics-0405.streamlit.app/
```

---

## 🧑‍💻 Author

**Chaitanya Pawar**

Data Analytics Internship Project
Infotact Solutions & Co.

---

## ⭐ Project Summary

This project demonstrates how data analytics can improve marketing decision-making by moving beyond traditional Last-Click Attribution.

By comparing **First-Touch**, **Last-Touch**, and **Linear Attribution**, the dashboard provides a clearer understanding of customer journeys and marketing channel performance.

The final deployed dashboard helps marketing managers identify high-performing channels, reduce wasted ad spend, analyze campaign-level results, and make data-driven budget allocation decisions.
