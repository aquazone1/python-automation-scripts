"""
CSV/Excel Data Cleaner - Remove duplicates, fix formats, standardize data
Requirements: pip install pandas openpyxl
"""
import pandas as pd
from pathlib import Path


def clean_csv(input_file: str, output_file: str = None) -> dict:
    """
    Clean a CSV/Excel file:
    - Remove duplicate rows
    - Remove empty rows/columns
    - Strip whitespace from strings
    - Standardize column names
    """
    ext = Path(input_file).suffix.lower()
    df = pd.read_excel(input_file) if ext in (".xlsx", ".xls") else pd.read_csv(input_file)

    stats = {"original_rows": len(df), "original_cols": len(df.columns)}

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r"[^\w]", "", regex=True)
    )

    # Remove fully empty rows and columns
    df.dropna(how="all", inplace=True)
    df.dropna(axis=1, how="all", inplace=True)

    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Remove duplicate rows
    before_dedup = len(df)
    df.drop_duplicates(inplace=True)
    stats["duplicates_removed"] = before_dedup - len(df)

    stats["final_rows"] = len(df)
    stats["final_cols"] = len(df.columns)

    if output_file is None:
        stem = Path(input_file).stem
        output_file = str(Path(input_file).parent / f"{stem}_cleaned.csv")

    df.to_csv(output_file, index=False, encoding="utf-8-sig")
    stats["output_file"] = output_file
    return stats


def find_duplicates(input_file: str, subset: list = None) -> pd.DataFrame:
    """Return all duplicate rows for inspection."""
    ext = Path(input_file).suffix.lower()
    df = pd.read_excel(input_file) if ext in (".xlsx", ".xls") else pd.read_csv(input_file)
    return df[df.duplicated(subset=subset, keep=False)]


def standardize_phone_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Standardize phone numbers to +1XXXXXXXXXX format."""
    df[col] = (
        df[col].astype(str)
        .str.replace(r"[^\d+]", "", regex=True)
        .str.replace(r"^1(\d{10})$", r"+1\1", regex=True)
    )
    return df


def standardize_email_column(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Lowercase all emails and flag invalid ones."""
    df[col] = df[col].str.lower().str.strip()
    df[f"{col}_valid"] = df[col].str.match(r"^[\w.+-]+@[\w-]+\.[a-z]{2,}$")
    return df


if __name__ == "__main__":
    print("CSV Data Cleaner - Examples:")
    print()
    print("1. Clean a CSV file:")
    print("   stats = clean_csv('data.csv')")
    print("   print(stats)")
    print()
    print("2. Find duplicates:")
    print("   dupes = find_duplicates('data.csv', subset=['email'])")
    print("   print(dupes)")
