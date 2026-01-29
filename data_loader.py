# data_loader.py
# ERPACAD – Robust Curriculum Data Loader
# Supports Nursery to Class 12 without numeric casting errors

import pandas as pd
import os

# -------------------------------------------------
# DATA FILE LOCATIONS (TRY IN ORDER)
# -------------------------------------------------

DATA_PATHS = [
    "data/master.tsv",
    "data/Teachshank_Master_Database_FINAL_v2.tsv"
]

# -------------------------------------------------
# ACCEPTABLE COLUMN NAME VARIATIONS
# -------------------------------------------------

COLUMN_ALIASES = {
    "grade": ["grade", "class"],
    "subject": ["subject"],
    "chapter": ["chapter", "chapter name", "lesson"],
    "learning_outcome": ["learning outcome", "learning outcomes", "lo"]
}

# -------------------------------------------------
# LOAD DATA FUNCTION (SINGLE SOURCE OF TRUTH)
# -------------------------------------------------

def load_data():
    """
    Loads the curriculum TSV file safely.
    Returns a DataFrame with canonical columns:
    grade | subject | chapter | learning_outcome
    """

    # ---------- locate file ----------
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

    # ---------- read TSV ----------
    df = pd.read_csv(file_path, sep="\t")

    # ---------- normalize column headers ----------
    df.columns = [c.strip().lower() for c in df.columns]

    # ---------- resolve aliases ----------
    resolved = {}

    for canonical, options in COLUMN_ALIASES.items():
        for opt in options:
            if opt in df.columns:
                resolved[canonical] = opt
                break
        if canonical not in resolved:
            raise KeyError(
                f"❌ Required column missing: {canonical}\n"
                f"Accepted names: {options}"
            )

    # ---------- rename to canonical ----------
    df = df.rename(columns={
        resolved["grade"]: "grade",
        resolved["subject"]: "subject",
        resolved["chapter"]: "chapter",
        resolved["learning_outcome"]: "learning_outcome"
    })

    # ---------- CLEAN VALUES (NO INT CASTING) ----------
    df["grade"] = df["grade"].astype(str).str.strip()
    df["subject"] = df["subject"].astype(str).str.strip()
    df["chapter"] = df["chapter"].astype(str).str.strip()
    df["learning_outcome"] = df["learning_outcome"].astype(str).str.strip()

    # ---------- drop empty rows ----------
    df = df[
        (df["grade"] != "") &
        (df["subject"] != "") &
        (df["chapter"] != "") &
        (df["learning_outcome"] != "")
    ]

    return df
