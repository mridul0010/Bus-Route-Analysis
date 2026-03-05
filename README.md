# 🚌 Bus Route Analysis

An interactive data analysis project that explores customer travel behavior and booking patterns using ticket-level bus travel data. It includes a Jupyter notebook for in-depth exploratory data analysis (EDA) and a Streamlit dashboard for interactive visualization.

## 📌 Problem Statement

The objective is to understand customer travel behavior and booking patterns using ticket-level data provided by Freshbus. The analysis focuses on:

1. Understanding how different customer segments travel across routes, time of travel, and bus type.
2. Understanding how far in advance customers book their journeys.

The insights derived can help improve service scheduling, bus configuration, and customer experience.

## ✨ Features

### Jupyter Notebook (`travelling_analysis.ipynb`)
- Feature engineering from service numbers (route extraction, sleeper/seater classification, departure time parsing)
- Time-of-travel categorization (Early Morning, Day, Evening, Overnight)
- Booking gap calculation (days between booking and journey)
- Age group segmentation
- Comprehensive EDA including:
  - Bus type preference analysis
  - Seat fare distribution and outlier detection
  - Bookings by age group, gender, and route
  - Revenue analysis by route and time of travel
  - Booking behavior and planning horizon analysis
  - Heatmaps for route × time-of-travel revenue and volume

### Streamlit Dashboard (`app.py`)
- Interactive filters for Route, Category, Time of Travel, Gender, and Age Group
- Key metric cards (Total Tickets, Avg Seat Fare, Total Revenue, Max Booking)
- Category-wise fare comparison (Seat Fare vs Total Amount)
- Top 10 routes by revenue
- Demographic distribution (Age Group Revenue, Gender Distribution)
- Seat Fare vs Transaction Total scatter plot
- Route × Time volume heatmap
- Dynamic strategic insights
- Filtered data download as CSV

## 🛠️ Tech Stack

- **Python 3**
- **Streamlit** — interactive web dashboard
- **Pandas** & **NumPy** — data manipulation
- **Plotly** — interactive charts
- **Matplotlib** & **Seaborn** — static visualizations
- **Jupyter Notebook** — exploratory analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mridul0010/Bus-Route-Analysis.git
   cd Bus-Route-Analysis
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

### Running the Notebook

```bash
jupyter notebook travelling_analysis.ipynb
```

### **Project Link**
```bash
https://bus-route-analysis.streamlit.app/
```

## 📁 Project Structure

```
Bus-Route-Analysis/
├── app.py                      # Streamlit dashboard application
├── travelling_analysis.ipynb   # Jupyter notebook with full EDA
├── ticket.csv                  # Raw ticket-level dataset
├── Final_bus.csv               # Processed dataset used by the dashboard
├── requirements.txt            # Python dependencies
├── LICENSE                     # GPL-3.0 license
└── README.md                   # Project documentation
```

## 📊 Data Description

### `ticket.csv` (Raw Data)
| Column | Description |
|---|---|
| Ticket No | Unique ticket identifier |
| Service Number | Encoded service info (route, bus type, departure time) |
| Journey Date | Date of travel |
| Seat Fare | Fare for a single seat |
| Total Ticket Amount | Total amount paid |
| Category | Booking platform (e.g., Redbus, Online) |
| Age | Passenger age |
| Gender | Passenger gender |
| Booked Date Time | Date and time of booking |
| Journey Date Time | Date and time of journey |

### `Final_bus.csv` (Processed Data)
Includes additional derived columns:
| Column | Description |
|---|---|
| Encode Route | Extracted route (e.g., BN-TP, CHN-BNG) |
| isSleeper | Binary flag — 1 for sleeper, 0 for seater |
| Time Of Travel | Categorized time bucket (Early Morning, Day, Evening, Overnight) |
| Departure Date Time | Combined journey date and departure time |
| Booking Gap Days | Number of days between booking and journey |
| Age Group | Age demographic bucket (e.g., 18-25, 26-40) |

## 📄 License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
