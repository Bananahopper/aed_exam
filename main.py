import os
import sys
from src import RAW_DATA_DIR, PROCESSED_DATA_DIR, OUTPUT_DIR
from src.data_loader import DataLoader
from src.visulaizer import Visualizer
from src.risk_analyzer import RiskAnalyzer

# Create directories if they do not exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "charts"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_DIR, "tables"), exist_ok=True)

# Set the src to the Python path
if os.path.join(os.getcwd(), "src") not in sys.path:
    sys.path.append(os.path.join(os.getcwd(), "src"))


# Question 1 - Load and merge data
data_loader = DataLoader(xlsx_file_dir=RAW_DATA_DIR, output_dir=PROCESSED_DATA_DIR)
data_loader.merge_all_data()


# Question 2: Analysis 1 - Country of origin by sector
data = data_loader.open_merged_data(columns=["SURVEY_ID", "SECTOR", "REGION"])
visualizer = Visualizer(data)
visualizer.plot_region_by_sector()


# Question 2: Analysis 2 - Suspect operations by sector
data = data_loader.open_merged_data(
    columns=[
        "SURVEY_ID",
        "SECTOR",
        "BU_REL_REFUSAL",
        "BU_REL_TERM",
        "SUSP_TRANS_SURVEY",
    ]
)
visualizer = Visualizer(data)
visualizer.plot_suspect_operations_by_sector()


# Question 2: Analysis 3 - Identification compliance by sector
data = data_loader.open_merged_data(
    columns=["SURVEY_ID", "SECTOR", "CLIENT_ID_STATUS", "BENIFICIARY_ID_STATUS"]
)
visualizer = Visualizer(data)
visualizer.plot_identification_compliance()


# Question 2: Analysis 4 - Document archiving compliance by sector
data = data_loader.open_merged_data(
    columns=["SURVEY_ID", "SECTOR", "DOCUMENT_ARCHIVING"]
)
visualizer = Visualizer(data)
visualizer.plot_document_archiving_compliance_by_sector()


# Question 2: Analysis 5 - Cash transactions analysis by sector
data = data_loader.open_merged_data(columns=["SURVEY_ID", "SECTOR", "PAYMENT_METHOD"])
visualizer = Visualizer(data)
visualizer.plot_cash_transactions_by_sector()


# Question 2: Analysis 6 - High-risk revenue by sector
data = data_loader.open_merged_data(
    columns=["SURVEY_ID", "SECTOR", "REVENUE_KIND", "NB_TRANSACTIONS"]
)
visualizer = Visualizer(data)
visualizer.summarize_high_risk_revenue_by_sector()


# Question 3: Risk analysis
risk_analyzer = RiskAnalyzer(data_loader)
data = risk_analyzer.calculate_risk_scores()
visualizer = Visualizer(data)
visualizer.plot_risk_assesment_by_sector()
risk_analyzer.find_high_risk_clients()
