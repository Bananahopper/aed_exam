import fireducks.pandas as pd
from src import PROCESSED_DATA_DIR


class DataLoader:
    """
    Class to process the single xlsx files into a single file, clean the data, and prepare it for analysis.
    """

    def __init__(self, xlsx_file_dir: list, output_dir: str = PROCESSED_DATA_DIR):
        self.xlsx_file_dir = xlsx_file_dir
        self.output_dir = output_dir

        self.file_mapping = {
            "master": "aml_master.xlsx",
            "quest": "aml_quest_data.xlsx",
            "payment": "aml_methode_paiement_client.xlsx",
            "revenue": "aml_revenu_professionnel.xlsx",
            "soft_check": "aml_soft_check.xlsx",
        }

    def merge_all_data(self):

        master = pd.read_excel(
            self.xlsx_file_dir + "/" + self.file_mapping["master"], sheet_name=0
        )
        quest = pd.read_excel(
            self.xlsx_file_dir + "/" + self.file_mapping["quest"], sheet_name=0
        )
        payment = pd.read_excel(
            self.xlsx_file_dir + "/" + self.file_mapping["payment"], sheet_name=0
        )
        revenue = pd.read_excel(
            self.xlsx_file_dir + "/" + self.file_mapping["revenue"], sheet_name=0
        )
        soft_check = pd.read_excel(
            self.xlsx_file_dir + "/" + self.file_mapping["soft_check"], sheet_name=0
        )

        merged = master.copy()

        # Quest has a column "YEAR_OF_SUBMISSION" taht has the same information as in master. Hence, we drop it.
        quest = quest.drop(columns=["YEAR_OF_SUBMISSION"])

        merged = pd.merge(
            merged, quest, on="SURVEY_ID", how="left", suffixes=("", "_dup")
        )
        merged = pd.merge(
            merged, payment, on="SURVEY_ID", how="left", suffixes=("", "_dup")
        )
        merged = pd.merge(
            merged, revenue, on="SURVEY_ID", how="left", suffixes=("", "_dup")
        )
        merged = pd.merge(
            merged, soft_check, on="SURVEY_ID", how="left", suffixes=("", "_dup")
        )

        # Remove duplicate columns
        duplicate_columns = [col for col in merged.columns if col.endswith("_dup")]
        merged.drop(columns=duplicate_columns, inplace=True)

        merged.to_excel(self.output_dir + "/merged_data.xlsx", index=False)

    def open_merged_data(self, columns: list = "all"):

        data = pd.read_excel(self.output_dir + "/merged_data.xlsx")
        if columns != "all":
            data = data[columns]

        return data
