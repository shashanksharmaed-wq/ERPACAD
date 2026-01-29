# data_loader.py
# ERPACAD – Safe Curriculum Data Loader
# Handles human-friendly TSV headers without breaking the app

import pandas as pd
import os

# -------------------------------------------------
# DATA FILE PATH (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------

DATA_PATHS = [
    "data/master.tsv",
    "data/Teachshank_Master_Database_FINAL_v2.tsv"
]

# -------------------------------------------------
# COLUMN NORMALIZATION MAP
# -------------------------------------------------

COLUMN_ALIASES = {
    "grade": ["grade", "class"],
    "subject": ["subject"],
    "chapter": ["chapter name", "chapter", "lesson"],
    "learning_outcome": ["learning outcomes", "learning outcome", "lo"]
}

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

def load_data():
    """
    Loads curriculum TSV safely.
    Returns a cleaned DataFrame with standardized columns:
    grade | subject | chapter | learning_outcome
    """

    # ---- locate file ----
    file_path = None
    for path in DATA_PATHS:
        if os.path.exists(path):
            file_path = path
            break

    if not file_path:
        raise FileNotFoundError(
            "❌ Curriculum data file not found.\n"
            "Expected one of:\n"
            " - data/master.tsv\n"
            " - data/Teachshank_Master_Database_FINAL_v2.tsv"
        )

    # ---- read TSV ----
    df = pd.read_csv(file_path, sep="\t")

    # ---- normalize headers ----
    df.columns = [c.strip().lower() for c in df.columns]

    # ---- resolve aliases ----
    resolved_columns = {}

    for standard_col, possible_names in COLUMN_ALIASES.items():
        for name in possible_names:
            if name in df.columns:
                resolved_columns[standard_col] = name
                break

        if standard_col not in resolved_columns:
            raise KeyError(
                f"❌ Required column missing: {standard_col}\n"
                f"Accepted names: {possible_names}"
            )

    # ---- rename to canonical names ----
    df = df.rename(columns={
        resolved_columns["grade"]: "grade",
        resolved_columns["subject"]: "subject",
        resolved_columns["chapter"]: "chapter",
        resolved_columns["learning_outcome"]: "learning_outcome"
    })

    # ---- clean values ----
    df["grade"] = df["grade"].astype(int)
    df["subject"] = df["subject"].astype(str).str.strip()
    df["chapter"] = df["chapter"].astype(str).str.strip()
    df["learning_outcome"] = df["learning_outcome"].astype(str).str.strip()

    return df
