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

<img width="1901" height="962" alt="image" src="https://github.com/user-attachments/assets/a262c69f-b1ba-4a09-a5c2-fc2b6d422545" />

<img width="1860" height="933" alt="image" src="https://github.com/user-attachments/assets/8e2de8a9-24b9-4faf-9f91-b5120db9f151" />

<img width="1883" height="735" alt="image" src="https://github.com/user-attachments/assets/ccacd2dd-6f29-448d-9e3b-c2fec6ad0293" />

<img width="1826" height="972" alt="image" src="https://github.com/user-attachments/assets/ba9e3cb5-4736-440a-8d74-48fcdb9e9e00" />

<img width="1876" height="1035" alt="image" src="https://github.com/user-attachments/assets/e1bcf357-debb-4d2c-93fb-18c438a47e8a" />



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

