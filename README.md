# 💊 Pharma Sales Interactive Dashboard 
This repository contains a Streamlit-based interactive dashboard for visualizing pharmaceutical sales data. 

It includes various filters and visualizations to explore sales trends, geographical distribution, and key performance indicators (KPIs).

## Features
- *Product Selection*: Filter data based on specific products.
- *Date Range Selection*: Adjust the date range to visualize sales within a specific period.
- *KPIs*: Display total units sold, total profit, and total margin.
- *Map Visualization*: View total units sold per city on an interactive map of Italy.
- *Line Chart*: Analyze price, cost, and margin over time.
- *Bar Charts*: Visualize units sold by weekday, month, and region.
- *Data Download*: Export filtered data as a CSV file.

## Installation
Installation
1. Clone the repository:
`git clone https://github.com/yourusername/pharma-sales-dashboard.git
cd pharma-sales-dashboard`
2. Install the required packages:
`pip install -r requirements.txt`
3. If you want to use your data, place your sales data CSV file (transactional, unpivotted) in the data/ directory and name it sales_augmented_final.csv. Place your logo image in the root directory and name it logo.png.
4. Run `streamlit run app.py`

## License
This project is licensed under the MIT License - see the LICENSE file for details.
