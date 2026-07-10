from pathlib import Path
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """
    Load CSV safely.
    """

    try:
        return pd.read_csv(path)

    except Exception as e:
        raise Exception(f"Error loading {path}: {e}")


def save_csv(df: pd.DataFrame, path: str) -> None:
    """
    Save DataFrame safely.
    """

    output_path = Path(path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)

    print(f"Saved: {path}")
