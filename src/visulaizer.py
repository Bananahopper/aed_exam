import matplotlib.pyplot as plt
import fireducks.pandas as pd
import numpy as np
from src import OUTPUT_DIR


class Visualizer:
    def __init__(self, data):
        self.data = data

    def plot_region_by_sector(self):
        """
        Create visualizations for region distribution by sector
        """
        # Group by SURVEY_ID and SECTOR, then aggregate REGION
        unique_data = (
            self.data.groupby(["SURVEY_ID", "SECTOR"])
            .agg({"REGION": lambda x: "NON LU" if "NON LU" in x.values else x.iloc[0]})
            .reset_index()
        )

        # Create figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 6))

        # 1. Stacked bar chart - absolute counts
        region_sector = pd.crosstab(unique_data["SECTOR"], unique_data["REGION"])
        region_sector.plot(
            kind="bar", stacked=True, ax=ax1, color=["#2E86AB", "#E63946"]
        )

        ax1.set_title(
            "Distribution des Clients par Région et Secteur",
            fontsize=14,
            fontweight="bold",
        )
        ax1.set_xlabel("Secteur", fontsize=12, fontweight="bold")
        ax1.set_ylabel("Nombre de Clients", fontsize=12)
        ax1.legend(title="Région", bbox_to_anchor=(1.05, 1), loc="upper left")
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)

        for container in ax1.containers:
            ax1.bar_label(container, label_type="center", fontsize=10)

        # 2. Percentage bar chart - proportion of NON LU
        region_sector_pct = region_sector.div(region_sector.sum(axis=1), axis=0) * 100

        if "NON LU" in region_sector_pct.columns:
            non_lu_pct = region_sector_pct["NON LU"]
            bars = ax2.bar(
                non_lu_pct.index,
                non_lu_pct.values,
                color=["#70E639", "#6534B4", "#F77F00"],
            )

            ax2.set_title(
                "Pourcentage de Clients NON LU par Secteur",
                fontsize=14,
                fontweight="bold",
            )
            ax2.set_xlabel("Secteur", fontsize=12, fontweight="bold")
            ax2.set_ylabel("Pourcentage (%)", fontsize=12)
            ax2.set_ylim(
                0, max(non_lu_pct.values) * 1.2 if non_lu_pct.values.any() else 100
            )

            for bar, value in zip(bars, non_lu_pct.values):
                height = bar.get_height()
                ax2.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 1,
                    f"{value:.1f}%",
                    ha="center",
                    va="bottom",
                    fontsize=11,
                )

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR + "/charts/region_by_sector.png", dpi=300, bbox_inches="tight"
        )

    def plot_suspect_operations_by_sector(self):
        """
        Analyze suspicious operations requiring mandatory declarations (DOS = Déclaration d'Opérations Suspectes)
        """

        # Entries that are X should be Y and entries that are None should be N
        self.data["BU_REL_REFUSAL"] = self.data["BU_REL_REFUSAL"].replace(
            {"X": "Y", None: "N"}
        )
        self.data["BU_REL_TERM"] = self.data["BU_REL_TERM"].replace(
            {"X": "Y", None: "N"}
        )
        self.data["SUSP_TRANS_SURVEY"] = self.data["SUSP_TRANS_SURVEY"].replace(
            {"X": "Y", None: "N"}
        )

        unique_data = self.data.drop_duplicates(subset=["SURVEY_ID"])

        fig, ax1 = plt.subplots(1, 1, figsize=(12, 10))

        # Calculate suspicious operations by sector
        suspicious_ops = pd.DataFrame()

        for sector in unique_data["SECTOR"].unique():
            sector_data = unique_data[unique_data["SECTOR"] == sector]

            # Count refusals
            refusals = (sector_data["BU_REL_REFUSAL"] == "Y").sum()

            # Count refusals WITHOUT DOS declaration
            refusals_no_dos = (
                (sector_data["BU_REL_REFUSAL"] == "Y")
                & (sector_data["SUSP_TRANS_SURVEY"] != "Y")
            ).sum()

            # Count terminations
            terminations = (sector_data["BU_REL_TERM"] == "Y").sum()

            suspicious_ops.loc[sector, "Refus Suspect"] = refusals
            suspicious_ops.loc[sector, "Refus SANS Déclaration DOS"] = refusals_no_dos
            suspicious_ops.loc[sector, "Mise à Terme Suspecte"] = terminations

        # Create the stacked bar chart
        suspicious_ops[
            ["Refus Suspect", "Mise à Terme Suspecte", "Refus SANS Déclaration DOS"]
        ].plot(
            kind="bar",
            ax=ax1,
            color=[
                "#2E86AB",
                "#F77F00",
                "#E63946",
            ],  # Blue, Orange, Red (red for non-compliance)
            stacked=True,
        )

        ax1.set_title(
            "Opérations Suspectes par Secteur (avec analyse de conformité DOS)",
            fontsize=14,
            fontweight="bold",
        )
        ax1.set_xlabel("Secteur", fontsize=12)
        ax1.set_ylabel("Nombre d'Opérations", fontsize=12)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0)
        ax1.legend(
            [
                "Refus d'entrée en relation",
                "Mise à terme d'une relation",
                "Refus SANS DOS",
            ]
        )

        # Add value labels
        for container in ax1.containers:
            labels = [int(v) if v > 0 else "" for v in container.datavalues]
            ax1.bar_label(container, labels=labels, label_type="center")

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR + "/charts/suspicious_operations_by_sector.png",
            dpi=300,
            bbox_inches="tight",
        )

    def plot_identification_compliance(self):
        """
        Analyze identification compliance
        """
        # will get columns Sector, client_id_status, beneficiary_id_status, survey_id. can be avancee, simple or na

        unique_data = self.data.drop_duplicates(subset=["SURVEY_ID"])

        fig, axes = plt.subplots(3, 1, figsize=(12, 15))

        # Conditions
        condition1 = (unique_data["CLIENT_ID_STATUS"] == "AVANCEE") & (
            unique_data["BENIFICIARY_ID_STATUS"] == "AVANCEE"
        )
        condition2 = (unique_data["CLIENT_ID_STATUS"] == "SIMPLE") & (
            unique_data["BENIFICIARY_ID_STATUS"] == "SIMPLE"
        )
        condition3 = (
            unique_data["CLIENT_ID_STATUS"] != unique_data["BENIFICIARY_ID_STATUS"]
        )

        choices = ["AVANCEE", "SIMPLE", "RISK"]

        unique_data["IDENTIFICATION_COMPLIANCE"] = np.select(
            [condition1, condition2, condition3], choices, default="NA"
        )

        sectors = [
            {"name": "IMMO", "color": "#2E86AB", "ax": axes[0]},
            {"name": "SERVICE", "color": "#E63946", "ax": axes[1]},
            {"name": "ECO", "color": "#F77F00", "ax": axes[2]}
        ]

        for sector_info in sectors:
            sector_name = sector_info["name"]
            color = sector_info["color"]
            ax = sector_info["ax"]
            
            sector_compliance = unique_data[unique_data["SECTOR"] == sector_name]
            sector_compliance_counts = (
                sector_compliance.groupby("IDENTIFICATION_COMPLIANCE")
                .size()
                .reset_index(name="Count")
            )
            
            bars = sector_compliance_counts.plot(
                kind="bar",
                x="IDENTIFICATION_COMPLIANCE",
                y="Count",
                ax=ax,
                color=color,
                legend=False
            )
            
            for i, bar in enumerate(ax.patches):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                        f'{int(height)}',
                        ha='center', va='bottom', fontweight='bold', fontsize=10)
            
            ax.set_title(
                f"Conformité d'Identification dans le Secteur {sector_name}",
                fontsize=14,
                fontweight="bold",
            )
            ax.set_xlabel("Conformité d'Identification", fontsize=12)
            ax.set_ylabel("Nombre de Clients", fontsize=12)
            ax.tick_params(axis='x', rotation=0)

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR + "/charts/identification_compliance_by_sector.png",
            dpi=300,
            bbox_inches="tight",
        )

    def plot_document_archiving_compliance_by_sector(self):
        """
        Analyze CRF refusal by transaction type and KYC
        """

        unique_data = self.data.drop_duplicates(subset=["SURVEY_ID"])

        unique_data["COMPLIANCE"] = unique_data.apply(
            lambda row: (
                "Conforme"
                if row["DOCUMENT_ARCHIVING"] == "5A"
                or row["DOCUMENT_ARCHIVING"] == "5A+"
                else "Non Conforme"
            ),
            axis=1,
        )

        sectors = ["IMMO", "SERVICE", "ECO"]
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

        for sector, ax in zip(sectors, [ax1, ax2, ax3]):
            sector_data = unique_data[unique_data["SECTOR"] == sector]
            compliance_counts = sector_data["COMPLIANCE"].value_counts()

            colors = [
                "#2E86AB" if x == "Conforme" else "#E63946"
                for x in compliance_counts.index
            ]
            compliance_counts.plot(kind="bar", ax=ax, color=colors)

            ax.set_title(
                f"Conformité d'Archivage des Documents dans le Secteur {sector}",
                fontsize=14,
                fontweight="bold",
            )
            ax.set_xlabel("Conformité d'Archivage", fontsize=12)
            ax.set_ylabel("Nombre de Clients", fontsize=12)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

            for i, v in enumerate(compliance_counts.values):
                ax.text(i, v + 1, str(v), ha="center", va="bottom")

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR + "/charts/document_archiving_compliance_by_sector.png",
            dpi=300,
            bbox_inches="tight",
        )

    def plot_cash_transactions_by_sector(self):
        """
        Analyze cash transactions by sector
        """
        unique_data = self.data.drop_duplicates(subset=["SURVEY_ID"])

        fig, ax = plt.subplots(figsize=(12, 6))

        cash_clients = (
            unique_data[unique_data["PAYMENT_METHOD"] == "CASH"]
            .groupby("SECTOR")
            .size()
        )

        cash_clients.plot(kind="bar", ax=ax, color="#E63946")

        ax.set_title(
            "Clients Utilisant des Paiements en Espèces par Secteur",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_xlabel("Secteur", fontsize=12)
        ax.set_ylabel("Nombre de Clients", fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

        for i, v in enumerate(cash_clients.values):
            ax.text(i, v + 0.5, str(v), ha="center", va="bottom")

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR + "/charts/cash_transactions_by_sector.png",
            dpi=300,
            bbox_inches="tight",
        )

        summary = pd.DataFrame(
            {
                "Total Clients": unique_data.groupby("SECTOR")["SURVEY_ID"].nunique(),
                "Clients Espèces": cash_clients.fillna(0).astype(int),
            }
        )
        summary["% Utilisant Espèces"] = (
            summary["Clients Espèces"] / summary["Total Clients"] * 100
        ).round(1)

        summary.to_excel(
            OUTPUT_DIR + "/tables/cash_transactions_by_sector_summary.xlsx"
        )

    def summarize_high_risk_revenue_by_sector(self):
        """
        Analyze high-risk revenue types by sector including IMMO transactions
        """

        high_risk_revenues = ["SERV_CREATION_S", "SERV_FONCTION", "SERV_VIRTUEL"]

        high_risk_clients = (
            self.data[self.data["REVENUE_KIND"].isin(high_risk_revenues)]
            .groupby("SECTOR")["SURVEY_ID"]
            .nunique()
        )

        immo_transactions = (
            self.data[self.data["REVENUE_KIND"] == "IMMO_ACHAT_VENT"]
            .groupby("SURVEY_ID")["NB_TRANSACTIONS"]
            .sum()
            .reset_index()
        )

        if not immo_transactions.empty:
            transaction_threshold = immo_transactions["NB_TRANSACTIONS"].quantile(0.75)
            high_volume_clients = immo_transactions[
                immo_transactions["NB_TRANSACTIONS"] > transaction_threshold
            ]["SURVEY_ID"]

            immo_high_risk = (
                self.data[self.data["SURVEY_ID"].isin(high_volume_clients)]
                .groupby("SECTOR")["SURVEY_ID"]
                .nunique()
            )

            # Calculate IMMO statistics
            immo_stats = {
                "Min Transactions IMMO": immo_transactions["NB_TRANSACTIONS"].min(),
                "Médiane Transactions IMMO": immo_transactions[
                    "NB_TRANSACTIONS"
                ].median(),
                "Max Transactions IMMO": immo_transactions["NB_TRANSACTIONS"].max(),
                "Seuil 75e Percentile": transaction_threshold,
            }
        else:
            immo_high_risk = pd.Series(dtype=int)
            immo_stats = {}

        total_high_risk = high_risk_clients.add(immo_high_risk, fill_value=0)

        summary = pd.DataFrame(
            {
                "Total Clients": self.data.groupby("SECTOR")["SURVEY_ID"].nunique(),
                "Clients Revenus Services Risque": high_risk_clients.fillna(0).astype(
                    int
                ),
                "Clients IMMO Volume Élevé": immo_high_risk.fillna(0).astype(int),
                "Total Clients Risque Élevé": total_high_risk.fillna(0).astype(int),
            }
        )

        summary["% Total Risque Élevé"] = (
            summary["Total Clients Risque Élevé"] / summary["Total Clients"] * 100
        ).round(1)

        with pd.ExcelWriter(
            OUTPUT_DIR + "/tables/high_risk_revenue_complete_summary.xlsx"
        ) as writer:
            summary.to_excel(writer, sheet_name="Résumé par Secteur")

            if immo_stats:
                immo_stats_df = pd.DataFrame([immo_stats])
                immo_stats_df.to_excel(
                    writer, sheet_name="Statistiques IMMO", index=False
                )


    def plot_risk_assesment_by_sector(self):
        """
        Visualize risk assessment by sector
        """
        unique_data = self.data.drop_duplicates(subset=["SURVEY_ID"])
        sectors = ["IMMO", "SERVICE", "ECO"]

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

        for sector, ax in zip(sectors, [ax1, ax2, ax3]):

            sector_low_risk_count = unique_data[
                (unique_data["SECTOR"] == sector)
                & (unique_data["RISK_CATEGORY"] == "Low")
            ].shape[0]
            sector_medium_risk_count = unique_data[
                (unique_data["SECTOR"] == sector)
                & (unique_data["RISK_CATEGORY"] == "Medium")
            ].shape[0]
            sector_high_risk_count = unique_data[
                (unique_data["SECTOR"] == sector)
                & (unique_data["RISK_CATEGORY"] == "High")
            ].shape[0]

            # Create a bar chart for risk assessment
            risk_counts = pd.Series(
                {
                    "Low Risk": sector_low_risk_count,
                    "Medium Risk": sector_medium_risk_count,
                    "High Risk": sector_high_risk_count,
                }
            )

            bars = risk_counts.plot(
                kind="bar",
                ax=ax,
                color=["#2E86AB", "#F77F00", "#E63946"],
                edgecolor="black",
            )

            # Annotate bar heights
            for idx, value in enumerate(risk_counts):
                ax.text(
                    idx,
                    value + max(risk_counts) * 0.01,
                    str(value),
                    ha="center",
                    va="bottom",
                    fontsize=11,
                    fontweight="bold",
                )

            ax.set_title(
                f"Évaluation des Risques dans le Secteur {sector}",
                fontsize=14,
                fontweight="bold",
            )
            ax.set_xlabel("Catégorie de Risque", fontsize=12)
            ax.set_ylabel("Nombre de Clients", fontsize=12)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

        plt.tight_layout()
        plt.savefig(
            OUTPUT_DIR + "/charts/risk_assessment_by_sector.png",
            dpi=300,
            bbox_inches="tight",
        )

        summary = pd.DataFrame(
            {
                "Total Clients": unique_data.groupby("SECTOR")["SURVEY_ID"].nunique(),
                "Low Risk": unique_data[unique_data["RISK_CATEGORY"] == "Low"]
                .groupby("SECTOR")["SURVEY_ID"]
                .nunique(),
                "Medium Risk": unique_data[unique_data["RISK_CATEGORY"] == "Medium"]
                .groupby("SECTOR")["SURVEY_ID"]
                .nunique(),
                "High Risk": unique_data[unique_data["RISK_CATEGORY"] == "High"]
                .groupby("SECTOR")["SURVEY_ID"]
                .nunique(),
            }
        )
        summary["% Low Risk"] = (
            summary["Low Risk"] / summary["Total Clients"] * 100
        ).round(1)
        summary["% Medium Risk"] = (
            summary["Medium Risk"] / summary["Total Clients"] * 100
        ).round(1)
        summary["% High Risk"] = (
            summary["High Risk"] / summary["Total Clients"] * 100
        ).round(1)

        summary.to_excel(OUTPUT_DIR + "/tables/risk_assessment_summary.xlsx")
