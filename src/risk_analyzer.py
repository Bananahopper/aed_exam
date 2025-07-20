import fireducks.pandas as pd
import numpy as np
import os
from src import OUTPUT_DIR


class RiskAnalyzer:
    """
    Class to analyze the risk data and generate visualizations.
    """

    def __init__(self, data_loader):
        self.data_loader = data_loader

    def load_data(self):
        """
        Load the merged data from the DataLoader.
        """
        if os.path.exists(
            self.data_loader.output_dir + "/risk_analysis_processed_data.xlsx"
        ):
            return pd.read_excel(
                self.data_loader.output_dir + "/risk_analysis_processed_data.xlsx"
            )

        return self.data_loader.open_merged_data()

    def process_data(self):
        """
        Process the data for risk analysis.
        """

        if os.path.exists(
            self.data_loader.output_dir + "/risk_analysis_processed_data.xlsx"
        ):
            return print("Data already processed. You can skip this step.")

        data = self.load_data()

        # First we normalize the data in the Refusal and Termination columns
        data["BU_REL_REFUSAL"] = data["BU_REL_REFUSAL"].replace({"X": "Y", None: "N"})
        data["BU_REL_TERM"] = data["BU_REL_TERM"].replace({"X": "Y", None: "N"})
        data["SUSP_TRANS_SURVEY"] = data["SUSP_TRANS_SURVEY"].replace(
            {"X": "Y", None: "N"}
        )

        # Then we create a column that tracks how well the identification compliance is done
        condition1 = (data["CLIENT_ID_STATUS"] == "AVANCEE") & (
            data["BENIFICIARY_ID_STATUS"] == "AVANCEE"
        )
        condition2 = (data["CLIENT_ID_STATUS"] == "SIMPLE") & (
            data["BENIFICIARY_ID_STATUS"] == "SIMPLE"
        )
        condition3 = data["CLIENT_ID_STATUS"] != data["BENIFICIARY_ID_STATUS"]

        choices = ["AVANCEE", "SIMPLE", "RISK"]

        data["IDENTIFICATION_COMPLIANCE"] = np.select(
            [condition1, condition2, condition3], choices, default="NA"
        )

        # We can also create a column for document archiving compliance
        data["ARCHIVING_COMPLIANCE"] = data.apply(
            lambda row: (
                "Conforme"
                if row["DOCUMENT_ARCHIVING"] == "5A"
                or row["DOCUMENT_ARCHIVING"] == "5A+"
                else "Non Conforme"
            ),
            axis=1,
        )

        # Also to track the country of origin of the client we can add a column
        non_lu_clients = data[data["REGION"] == "NON LU"]["SURVEY_ID"].unique()
        data["REGION_RISK"] = (
            data["SURVEY_ID"].isin(non_lu_clients).map({True: "NON LU", False: "LU"})
        )

        # We will keep only the relevant columns for the risk analysis
        relevant_columns = [
            "SURVEY_ID",
            "SECTOR",
            "REGION_RISK",
            "BU_REL_REFUSAL",
            "BU_REL_TERM",
            "IDENTIFICATION_COMPLIANCE",
            "ARCHIVING_COMPLIANCE",
            "PAYMENT_METHOD",
            "REVENUE_KIND",
            "NB_TRANSACTIONS",
        ]

        data = data[relevant_columns]

        data.to_excel(
            self.data_loader.output_dir + "/risk_analysis_processed_data.xlsx",
            index=False,
        )

        return data

    def calculate_risk_scores(self):
        """
        Calculate risk scores based on the processed data.
        """
        data = self.load_data()

        # So for each row we can calculate a risk score based on the following criteria:
        # - BU_REL_REFUSAL: if 'Y' then +1
        # - BU_REL_TERM: if 'Y' then +1
        # - IDENTIFICATION_COMPLIANCE: if 'RISK' then +1
        # - ARCHIVING_COMPLIANCE: if 'Non Conforme' then +1
        # - REGION_RISK: if 'NON LU' then +1
        # - PAYMENT_METHOD: if 'CASH' then +1
        # - REVENUE_KIND: if 'SERV_CREATION_S', 'SERV_FONCTION', 'SERV_VIRTUEL' then +1
        # - NB_TRANSACTIONS: if > 61 then +1
        # - If any cell is NaN, we will not count it as a risk factor.
        # This will give us a total possible risk score of 8

        data["RISK_SCORE"] = 0
        data.loc[data["BU_REL_REFUSAL"] == "Y", "RISK_SCORE"] += 1
        data.loc[data["BU_REL_TERM"] == "Y", "RISK_SCORE"] += 1
        data.loc[data["IDENTIFICATION_COMPLIANCE"] == "RISK", "RISK_SCORE"] += 1
        data.loc[data["ARCHIVING_COMPLIANCE"] == "Non Conforme", "RISK_SCORE"] += 1
        data.loc[data["REGION_RISK"] == "NON LU", "RISK_SCORE"] += 1
        data.loc[data["PAYMENT_METHOD"] == "CASH", "RISK_SCORE"] += 1
        data.loc[
            data["REVENUE_KIND"].isin(
                ["SERV_CREATION_S", "SERV_FONCTION", "SERV_VIRTUEL"]
            ),
            "RISK_SCORE",
        ] += 1
        data.loc[data["NB_TRANSACTIONS"] > 61, "RISK_SCORE"] += 1

        # Now we can categorize the risk score into low, medium, and high risk where:
        # - 0-1 is low risk
        # - 2-3 is medium risk
        # - >3 is high risk

        conditions = [
            (data["RISK_SCORE"] <= 1),
            (data["RISK_SCORE"] >= 2) & (data["RISK_SCORE"] <= 3),
            (data["RISK_SCORE"] > 3),
        ]
        choices = ["Low", "Medium", "High"]
        data["RISK_CATEGORY"] = np.select(conditions, choices, default="Unknown")

        data.to_excel(
            self.data_loader.output_dir + "/risk_analysis_scores.xlsx",
            index=False,
        )

        return data

    def find_high_risk_clients(self):
        """
        Find high risk clients based on the risk scores.
        """
        data = self.calculate_risk_scores()
        data = data.drop_duplicates(subset=["SURVEY_ID"])

        high_risk_clients = data[data["RISK_CATEGORY"] == "High"]

        high_risk_clients.to_excel(
            OUTPUT_DIR + "/tables/all_high_risk_clients.xlsx",
            index=False,
        )

        return high_risk_clients
