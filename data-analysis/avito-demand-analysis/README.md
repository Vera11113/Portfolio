# Avito Parser & Demand Analysis 📊

This project combines data collection and analysis to explore consumer demand in the context of Avito listings.

## 📂 Project Structure

- `avito_parser.py` – A web scraper that collects product listings from Avito.
- `demand_analysis.ipynb` – A notebook where demand is modeled based on price, income, and advertising variables.
- `data.csv` – A dataset containing parsed listing information.

## 📈 Goal

To identify how demand (measured as the number of views) depends on factors such as:
- Price of the product
- Consumer income (approximated by average salary in the region)
- Advertising efforts (measured via seller activity, e.g., number of comments)

## 🔧 Tools Used

- Python (undetected_chromedriver, selenium, pandas, seaborn, matplotlib)
- Basic econometric modeling (linear regression)

## 📌 Result

We built a linear demand function and analyzed elasticity by price, income, and advertising. The conclusion provides recommendations on what influences demand the most.

## 📁 Dataset

All data was collected from Avito using the custom-built parser.

---

*Note: This project is for educational purposes only and is not affiliated with Avito.*
