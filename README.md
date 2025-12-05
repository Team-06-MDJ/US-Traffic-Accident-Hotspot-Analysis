
# 🛣️ US Traffic Accident Analysis (2020–2023)
### **End-to-End Big Data Engineering Project**
Python • AWS S3 • AWS Glue • Athena • Power BI • Streamlit • Parquet • VS Code

---

## 📌 **Project Overview**
Road traffic accidents in the United States cause thousands of injuries and billions in economic loss every year.  
The goal of this project is to build a **scalable, cloud-based data pipeline** to analyze **U.S. traffic accident data (2020–2023)** and identify:

- High-risk accident **hotspots**
- Weather and road conditions influencing accidents
- Time-based accident patterns (rush hours, weekends, seasons)
- State-wise accident severity and frequency trends

This is a **full data engineering & analytics project**, including:
- Cloud storage  
- ETL pipeline  
- Data transformation  
- Query engine  
- Web dashboards  
- Power BI business insights  

---

# 🚀 **Architecture**

Local Machine (VS Code)  
→ Python ETL Pipeline  
→ AWS S3 (Data Lake: raw + processed data)  
→ AWS Glue (Jobs, Crawlers, Data Catalog)  
→ AWS Athena (SQL Analytics)  
→ Power BI (Business Dashboard)  
→ Streamlit Web App (Interactive Visualization)

---

# 🧰 **Tech Stack**

### **Languages**
- Python 3.10+
- SQL

### **Python Libraries**
- pandas  
- numpy  
- boto3  
- s3fs  
- pyarrow / fastparquet  
- streamlit  
- plotly  

### **AWS Services**
- Amazon S3 – Data Lake  
- AWS Glue – ETL, Crawlers, Catalog  
- AWS Athena – Serverless SQL  
- IAM – Permissions  

### **Visualization Tools**
- Power BI Desktop  
- Streamlit Web App  

---

# 🗂️ **Dataset**
The project uses the **US Traffic Accident Dataset (Kaggle)** containing:

- ~1.4 million accident records (filtered to 2020–2023)
- 49 US states
- 50+ features including:
  - Latitude & Longitude  
  - Weather conditions  
  - Visibility  
  - Severity  
  - Traffic signals  
  - Dates & Times  

---

# 🏗️ **Data Engineering Pipeline**

## **1️⃣ Ingestion**
Upload raw dataset to S3:

```
s3://us-traffic-accidents-datalake/raw/
```

Structure:

```
raw/
processed/
analytics/
logs/
```

---

## **2️⃣ ETL Pipeline (Python)**

### **Extract**
Read CSV directly from S3.

### **Transform**
- Clean missing values  
- Filter years 2020–2023  
- Drop invalid coordinates  
- Feature engineering  
- Hotspot grid generation  

### **Load**
Store the clean dataset as **Parquet** in S3:

```
s3://us-traffic-accidents-datalake/processed/accidents_2020_2023.parquet
```

---

# ☁️ **3️⃣ AWS Glue & Athena**

### **Glue Crawler**
- Detects schema in S3  
- Builds Glue Data Catalog  

### **Athena**
Example queries:

#### Top states:
```
SELECT state, COUNT(*) 
FROM accidents 
GROUP BY state 
ORDER BY 2 DESC;
```

#### Hotspots:
```
SELECT Tile_Lat, Tile_Lng, COUNT(*) 
FROM accidents 
GROUP BY 1,2 
ORDER BY 3 DESC 
LIMIT 50;
```

---

# 📊 **4️⃣ Visualizations**

## **Power BI Dashboard**
Includes:
- Hotspot map  
- Accidents by hour  
- Severity distribution  
- Weather impact  
- Filters for year, state, severity  

## **Streamlit Web App**
Features:
- Interactive map  
- State comparison  
- Severity filters  

Run:
```
streamlit run dashboard.py
```

---

# 📁 **Project Folder Structure**

```
US_Traffic_Project/
│
├── venv/
├── etl_pipeline.py
├── dashboard.py
├── README.md
└── requirements.txt
```

---

# ▶️ **How to Run**

### Create venv
```
python -m venv venv
```
Activate:

Windows:
```
venv\Scripts\activate
```

Mac/Linux:
```
source venv/bin/activate
```

### Install libraries:
```
pip install -r requirements.txt
```

### Run ETL:
```
python etl_pipeline.py
```

### Run dashboard:
```
streamlit run dashboard.py
```

---

# 📈 **Goals Achieved**
✔ Cloud-native pipeline  
✔ Automated ETL  
✔ 1.4M+ rows processed  
✔ Hotspot detection  
✔ Dashboards for insights  
✔ Scalable and production-ready  

---

# 🔮 **Future Work**
- Add ML accident severity predictor  
- Add Kafka/Kinesis for streaming  
- Deploy Streamlit on AWS EC2  
- Add Redshift/Snowflake warehouse  

---

# 🙌 **Team**
- Mohit Raiyani 
- Dharmika Gali   
- Jagdish Kumar  
