import json

# Create the notebook structure
notebook = {
    "cells": [],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 4,
}

# Add cells
cells = [
    # Title and setup
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "# Risk Analysis Pipeline\n\n"
            "This notebook performs comprehensive risk analysis on survey data, including:\n"
            "- Regional and sector analysis\n"
            "- Suspect operations detection\n"
            "- Compliance monitoring\n"
            "- Risk assessment and scoring\n\n"
            "## Setup Instructions\n\n"
            "1. Ensure your data is in the `data/raw` directory\n"
            "2. Install required packages: `pip install -r requirements.txt`\n"
            "3. Run cells sequentially"
        ],
    },
    {"cell_type": "markdown", "metadata": {}, "source": ["## 1. Setup and Imports"]},
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Import required modules\n"
            "from src.data_loader import DataLoader\n"
            "from src.visulaizer import Visualizer\n"
            "from src.risk_analyzer import RiskAnalyzer\n\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n\n"
            "# Set up plotting style\n"
            "plt.style.use('default')\n"
            'sns.set_palette("husl")\n\n'
            "# Display options\n"
            "pd.set_option('display.max_columns', None)\n"
            "pd.set_option('display.width', None)\n\n"
            'print("✅ All modules imported successfully")'
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 2. Data Loading and Preparation"],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Initialize data loader\n"
            'data_loader = DataLoader(xlsx_file_dir="data/raw", output_dir="data/processed")\n\n'
            "# Uncomment the line below if you need to merge raw data files first\n"
            "# data_loader.merge_all_data()\n\n"
            'print("✅ Data loader initialized")'
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Regional and Sector Analysis\n\n"
            "First, let's examine the distribution of survey responses across different regions and sectors."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load data for regional analysis\n"
            'regional_data = data_loader.open_merged_data(columns=["SURVEY_ID", "SECTOR", "REGION"])\n\n'
            "# Display basic info\n"
            'print(f"Dataset shape: {regional_data.shape}")\n'
            'print(f"\\nColumns: {list(regional_data.columns)}")\n'
            'print(f"\\nFirst few rows:")\n'
            "regional_data.head()"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Create regional visualization\n"
            "visualizer = Visualizer(regional_data)\n"
            "visualizer.plot_region_by_sector()\n\n"
            "# Display summary statistics\n"
            'print("\\n📊 Regional Distribution Summary:")\n'
            "print(regional_data['REGION'].value_counts())\n"
            'print("\\n📊 Sector Distribution Summary:")\n'
            "print(regional_data['SECTOR'].value_counts())"
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Suspect Operations Analysis\n\n"
            "Analyzing patterns in business relationship refusals, terminations, and suspicious transactions."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load data for suspect operations analysis\n"
            "suspect_data = data_loader.open_merged_data(\n"
            "    columns=[\n"
            '        "SURVEY_ID",\n'
            '        "SECTOR",\n'
            '        "BU_REL_REFUSAL",\n'
            '        "BU_REL_TERM",\n'
            '        "SUSP_TRANS_SURVEY",\n'
            "    ]\n"
            ")\n\n"
            'print(f"Suspect operations dataset shape: {suspect_data.shape}")\n'
            "suspect_data.head()"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Visualize suspect operations by sector\n"
            "visualizer = Visualizer(suspect_data)\n"
            "visualizer.plot_suspect_operations_by_sector()\n\n"
            "# Summary statistics for suspect operations\n"
            'print("\\n🚨 Suspect Operations Summary:")\n'
            'for col in ["BU_REL_REFUSAL", "BU_REL_TERM", "SUSP_TRANS_SURVEY"]:\n'
            "    if col in suspect_data.columns:\n"
            '        print(f"\\n{col}:")\n'
            "        print(suspect_data[col].value_counts())"
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 5. Identification Compliance Analysis\n\n"
            "Examining client and beneficiary identification compliance across sectors."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load identification compliance data\n"
            "id_compliance_data = data_loader.open_merged_data(\n"
            '    columns=["SURVEY_ID", "SECTOR", "CLIENT_ID_STATUS", "BENIFICIARY_ID_STATUS"]\n'
            ")\n\n"
            'print(f"ID compliance dataset shape: {id_compliance_data.shape}")\n'
            "id_compliance_data.head()"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Visualize identification compliance\n"
            "visualizer = Visualizer(id_compliance_data)\n"
            "visualizer.plot_identification_compliance()\n\n"
            "# Compliance summary\n"
            'print("\\n🆔 Identification Compliance Summary:")\n'
            'print("\\nClient ID Status:")\n'
            "print(id_compliance_data['CLIENT_ID_STATUS'].value_counts())\n"
            'print("\\nBeneficiary ID Status:")\n'
            "print(id_compliance_data['BENIFICIARY_ID_STATUS'].value_counts())"
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 6. Document Archiving Compliance\n\n"
            "Analyzing document archiving practices across different sectors."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load document archiving data\n"
            "archiving_data = data_loader.open_merged_data(\n"
            '    columns=["SURVEY_ID", "SECTOR", "DOCUMENT_ARCHIVING"]\n'
            ")\n\n"
            'print(f"Document archiving dataset shape: {archiving_data.shape}")\n'
            "archiving_data.head()"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Visualize document archiving compliance\n"
            "visualizer = Visualizer(archiving_data)\n"
            "visualizer.plot_document_archiving_compliance()\n\n"
            "# Document archiving summary\n"
            'print("\\n📁 Document Archiving Compliance Summary:")\n'
            "print(archiving_data['DOCUMENT_ARCHIVING'].value_counts())"
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 7. Cash Transactions Analysis\n\n"
            "Examining payment methods and cash transaction patterns by sector."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load payment method data\n"
            "payment_data = data_loader.open_merged_data(\n"
            '    columns=["SURVEY_ID", "SECTOR", "PAYMENT_METHOD"]\n'
            ")\n\n"
            'print(f"Payment method dataset shape: {payment_data.shape}")\n'
            "payment_data.head()"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Visualize cash transactions by sector\n"
            "visualizer = Visualizer(payment_data)\n"
            "visualizer.plot_cash_transactions_by_sector()\n\n"
            "# Payment method summary\n"
            'print("\\n💰 Payment Method Summary:")\n'
            "print(payment_data['PAYMENT_METHOD'].value_counts())"
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 8. High-Risk Revenue Analysis\n\n"
            "Analyzing revenue types and transaction volumes to identify high-risk patterns."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Load revenue and transaction data\n"
            "revenue_data = data_loader.open_merged_data(\n"
            '    columns=["SURVEY_ID", "SECTOR", "REVENUE_KIND", "NB_TRANSACTIONS"]\n'
            ")\n\n"
            'print(f"Revenue analysis dataset shape: {revenue_data.shape}")\n'
            "revenue_data.head()"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Summarize high-risk revenue by sector\n"
            "visualizer = Visualizer(revenue_data)\n"
            "visualizer.summarize_high_risk_revenue_by_sector()\n\n"
            "# Revenue summary statistics\n"
            'print("\\n📈 Revenue Analysis Summary:")\n'
            'print("\\nRevenue Types:")\n'
            "print(revenue_data['REVENUE_KIND'].value_counts())\n"
            'print("\\nTransaction Volume Statistics:")\n'
            "print(revenue_data['NB_TRANSACTIONS'].describe())"
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 9. Comprehensive Risk Assessment\n\n"
            "Computing overall risk scores and identifying high-risk clients based on multiple factors."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Initialize risk analyzer\n"
            "risk_analyzer = RiskAnalyzer(data_loader)\n\n"
            "# Calculate risk scores\n"
            'print("🔍 Calculating comprehensive risk scores...")\n'
            "risk_data = risk_analyzer.calculate_risk_scores()\n\n"
            'print(f"\\nRisk assessment dataset shape: {risk_data.shape}")\n'
            'print(f"\\nColumns in risk dataset: {list(risk_data.columns)}")\n'
            "risk_data.head()"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Visualize risk assessment by sector\n"
            "visualizer = Visualizer(risk_data)\n"
            "visualizer.plot_risk_assesment_by_sector()\n\n"
            "# Risk score statistics\n"
            "if 'risk_score' in risk_data.columns:\n"
            '    print("\\n⚠️ Risk Score Statistics:")\n'
            "    print(risk_data['risk_score'].describe())\n"
            "    \n"
            '    print("\\nRisk Distribution by Sector:")\n'
            "    if 'SECTOR' in risk_data.columns:\n"
            "        risk_by_sector = risk_data.groupby('SECTOR')['risk_score'].agg(['mean', 'median', 'std', 'count'])\n"
            "        print(risk_by_sector)"
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Identify high-risk clients\n"
            'print("🚨 Identifying high-risk clients...")\n'
            "high_risk_clients = risk_analyzer.find_high_risk_clients()\n\n"
            "if high_risk_clients is not None:\n"
            '    print(f"\\nNumber of high-risk clients identified: {len(high_risk_clients)}")\n'
            '    print("\\nHigh-risk clients preview:")\n'
            "    print(high_risk_clients.head(10))\n"
            "else:\n"
            '    print("No high-risk clients data returned")'
        ],
    },
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 10. Summary and Key Findings\n\n"
            "Let's summarize the key insights from our risk analysis pipeline."
        ],
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Generate summary statistics\n"
            'print("📋 RISK ANALYSIS PIPELINE SUMMARY")\n'
            'print("=" * 50)\n\n'
            "# Basic dataset info\n"
            "total_surveys = len(risk_data) if 'SURVEY_ID' in risk_data.columns else \"Unknown\"\n"
            "unique_sectors = risk_data['SECTOR'].nunique() if 'SECTOR' in risk_data.columns else \"Unknown\"\n\n"
            'print(f"📊 Total surveys analyzed: {total_surveys}")\n'
            'print(f"📈 Unique sectors: {unique_sectors}")\n\n'
            "if 'risk_score' in risk_data.columns:\n"
            "    avg_risk = risk_data['risk_score'].mean()\n"
            "    high_risk_threshold = risk_data['risk_score'].quantile(0.8)  # Top 20%\n"
            "    high_risk_count = len(risk_data[risk_data['risk_score'] > high_risk_threshold])\n"
            "    \n"
            '    print(f"⚠️ Average risk score: {avg_risk:.2f}")\n'
            '    print(f"🚨 High-risk entities (top 20%): {high_risk_count}")\n'
            '    print(f"🔢 High-risk threshold: {high_risk_threshold:.2f}")\n\n'
            'print("\\n✅ Analysis completed successfully!")\n'
            'print("\\n💡 Next steps:")\n'
            'print("   • Review high-risk clients for further investigation")\n'
            'print("   • Implement monitoring for identified risk patterns")\n'
            'print("   • Consider additional data sources for enhanced analysis")'
        ],
    },
]

# Add all cells to notebook
notebook["cells"] = cells

# Write to file
with open("notebook/risk_analysis_pipeline.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("✅ Notebook created successfully!")
print("📁 File saved as: risk_analysis_pipeline.ipynb")
print("🚀 You can now open it in VSCode!")
