# US Traffic Accident Hotspot Analysis – Streamlit Platform

This repository contains a complete **end-to-end data analytics platform** for identifying and visualizing US traffic accident hotspots.  

The project includes:

- 🚗 **ETL pipeline** for data cleaning and transformation  
- 🛰️ **AWS connectivity check** to verify cloud data access  
- 📊 **Interactive Streamlit dashboard** for hotspot visualization  
- 🌐 **Streamlit-based website** serving as the project’s user-facing interface  

Power BI is **not** used in this version of the project.

---

## 🚀 Project Components

### 🔹 1. ETL Pipeline (`etl_pipeline.py`)
This module handles:

- Dataset ingestion  
- Missing value treatment  
- Feature extraction  
- Data formatting for visualization  
- Saving processed datasets  

It serves as the backbone for preparing clean data used by the dashboard and website.

---

### 🔹 2. AWS Connectivity Script (`check_aws.py`)
A utility script that:

- Verifies AWS resource access  
- Confirms credentials and S3 availability  
- Ensures connections work before running the ETL pipeline  

Useful when pulling large accident datasets from cloud storage.

---

### 🔹 3. Streamlit Dashboard (`dashboard.py`)
An interactive analytics dashboard that provides:

- Heatmap & clustering visualizations  
- Filtering by weather, severity, time, and state  
- Geospatial accident hotspot detection  
- Trend charts and severity analysis  

This file represents your **core analysis interface**.

---

### 🔹 4. Streamlit Website (`website/app.py`)
Your front-end Streamlit website that:

- Hosts the dashboard  
- Displays project introduction and documentation  
- Provides navigation to analysis sections  
- Offers a smoother user experience  

⚠️ **Note:**  
The website file was located inside `venv/`, but virtual environment folders should *never* contain project code.  
In the recommended structure below, the website is placed in its own folder.

---

## 🗂️ Recommended Project Structure

```
📁 traffic-accident-hotspot-analysis
│
├── etl_pipeline.py            # ETL process for cleaning & transforming data
├── check_aws.py               # AWS connectivity & validation script
├── dashboard.py               # Streamlit analytics dashboard
│
├── website/
│   └── app.py                 # Streamlit-based website UI
│
├── data/
│   └── processed/             # Output of ETL pipeline (optional)
│
├── requirements.txt
├── README.md
└── venv/                      # Virtual environment (excluded from GitHub)
```

⚠️ **Do not upload the `venv/` folder to GitHub.**

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository
```
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

### 2️⃣ Create & activate a virtual environment
```
python -m venv venv
source venv/bin/activate     # macOS / Linux
venv\Scripts\activate        # Windows
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Run ETL Pipeline
```
python etl_pipeline.py
```

### Run AWS Connectivity Test
```
python check_aws.py
```

### Launch the Streamlit Dashboard
```
streamlit run dashboard.py
```

### Launch the Streamlit Website
```
streamlit run website/app.py
```

---

## 🧪 Technologies Used

- **Python**
- **Streamlit**
- **Pandas / NumPy**
- **Plotly / Folium**
- **GeoPandas**
- **AWS S3 / boto3**
- **scikit-learn** (hotspot clustering)

---

## 🤝 Contributing

Contributions are welcome — whether you want to improve visuals, add new filters, optimize the ETL process, or extend cloud automation.

---

## 📬 Contact

For queries or collaboration, feel free to open an issue or contact the project owner.

---

### ⭐ If this project helps you, consider giving it a star on GitHub!
