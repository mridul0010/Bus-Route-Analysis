<div align="center">

# 🚌 Bus Route Analysis

**Explore customer travel behavior and booking patterns through interactive data analysis**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Live Demo](https://bus-route-analysis.streamlit.app/) · [Report Bug](https://github.com/mridul0010/Bus-Route-Analysis/issues) · [Request Feature](https://github.com/mridul0010/Bus-Route-Analysis/issues)

</div>

---

## Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Data Description](#data-description)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## About the Project

This project analyzes ticket-level bus travel data provided by Freshbus to uncover customer travel behavior and booking patterns. It includes a **Jupyter notebook** for in-depth exploratory data analysis (EDA) and a **Streamlit dashboard** for interactive visualization.

### Objectives

1. Understand how different customer segments travel across routes, time of travel, and bus type.
2. Analyze how far in advance customers book their journeys.

The insights derived can help improve service scheduling, bus configuration, and overall customer experience.

---

## Key Features

### Exploratory Analysis — `travelling_analysis.ipynb`

| Area | Details |
|---|---|
| **Feature Engineering** | Route extraction, sleeper/seater classification, departure time parsing from service numbers |
| **Time Categorization** | Early Morning, Day, Evening, Overnight travel buckets |
| **Booking Analysis** | Booking gap calculation (days between booking and journey) |
| **Segmentation** | Age group bucketing for demographic analysis |
| **Visualizations** | Bus type preferences, fare distributions, route revenue, booking behavior heatmaps, and more |

### Interactive Dashboard — `app.py`

| Capability | Details |
|---|---|
| **Filters** | Route, Category, Time of Travel, Gender, Age Group |
| **Metrics** | Total Tickets, Avg Seat Fare, Total Revenue, Max Booking |
| **Charts** | Category-wise fare comparison, Top 10 routes by revenue, demographic distributions, scatter plots, heatmaps |
| **Insights** | Dynamic strategic insights generated from filtered data |
| **Export** | Download filtered data as CSV |

---

## Tech Stack

| Technology | Purpose |
|---|---|
| [Python 3](https://www.python.org/) | Core programming language |
| [Streamlit](https://streamlit.io/) | Interactive web dashboard |
| [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) | Data manipulation and analysis |
| [Plotly](https://plotly.com/python/) | Interactive charts |
| [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) | Static visualizations |
| [Jupyter Notebook](https://jupyter.org/) | Exploratory analysis environment |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mridul0010/Bus-Route-Analysis.git
   cd Bus-Route-Analysis
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### Usage

**Launch the Streamlit dashboard:**

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`.

**Run the Jupyter notebook:**

```bash
jupyter notebook travelling_analysis.ipynb
```

> 🌐 **Live Demo:** [bus-route-analysis.streamlit.app](https://bus-route-analysis.streamlit.app/)

---

## Project Structure

```
Bus-Route-Analysis/
├── app.py                      # Streamlit dashboard application
├── travelling_analysis.ipynb   # Jupyter notebook with full EDA
├── ticket.csv                  # Raw ticket-level dataset
├── Final_bus.csv               # Processed dataset used by the dashboard
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT license
└── README.md                   # Project documentation
```

---

## Data Description

### `ticket.csv` — Raw Data

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

### `Final_bus.csv` — Processed Data

Includes all raw columns plus the following derived fields:

| Column | Description |
|---|---|
| Encode Route | Extracted route (e.g., BN-TP, CHN-BNG) |
| isSleeper | Binary flag — 1 for sleeper, 0 for seater |
| Time Of Travel | Categorized time bucket (Early Morning, Day, Evening, Overnight) |
| Departure Date Time | Combined journey date and departure time |
| Booking Gap Days | Number of days between booking and journey |
| Age Group | Age demographic bucket (e.g., 18-25, 26-40) |

---

## Screenshots

<details>
<summary>Click to expand dashboard screenshots</summary>

<br>

<img width="1524" height="485" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/10ad9644-5d21-4c99-8d29-0c28d85bd03b" />

<img width="1916" height="820" alt="Key Metrics" src="https://github.com/user-attachments/assets/715ec6ea-53bc-4db7-9aba-d158c96993b6" />

<img width="1891" height="763" alt="Route Analysis" src="https://github.com/user-attachments/assets/eaed05d0-1008-46bd-84ab-0e5fe08bdcba" />

<img width="1919" height="823" alt="Demographic Distribution" src="https://github.com/user-attachments/assets/5f7273d9-e561-4ef3-a117-8175d312daaf" />

<img width="1919" height="763" alt="Fare Analysis" src="https://github.com/user-attachments/assets/ea97f780-532e-458b-9571-7a1fec38bbcd" />

<img width="1911" height="701" alt="Scatter Plot" src="https://github.com/user-attachments/assets/9dfa172f-fec0-498c-95cc-947c441c5b56" />

<img width="1892" height="762" alt="Heatmap" src="https://github.com/user-attachments/assets/4dfa0195-4a40-4d86-aea9-7715617bcb53" />

<img width="1919" height="834" alt="Strategic Insights" src="https://github.com/user-attachments/assets/1016adac-32d4-41b1-b3f5-82cacc587292" />

<img width="1530" height="464" alt="Data Export" src="https://github.com/user-attachments/assets/221b7500-5684-4db3-a633-451be7df3967" />

</details>

---


## License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

## Author

**Mridul Lata** — Aspiring Data Analyst · Jaipur, India

[![LinkedIn](https://img.shields.io/badge/LinkedIn-mridullata-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mridullata)
[![GitHub](https://img.shields.io/badge/GitHub-mridul0010-181717?logo=github&logoColor=white)](https://github.com/mridul0010)

---

<div align="center">

⭐ If you found this project helpful, please consider giving it a star!

</div>

