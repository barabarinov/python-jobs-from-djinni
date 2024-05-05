import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series


def load_data(file_path: str) -> DataFrame:
    """Load data from a CSV file."""
    return pd.read_csv(file_path)


def preprocess_data(data: DataFrame) -> DataFrame:
    """Preprocess data by filling missing values."""
    data.fillna(value=pd.NA, inplace=True)
    return data


def analyze_technologies(data: DataFrame) -> Series:
    """Analyze technologies required for Python vacancies."""
    return data["required_technologies"].dropna().str.split(", ").explode()


def plot_top_technologies(technologies: Series) -> None:
    """Plot a pie chart for the top 10 technologies."""
    tech_counts = technologies.value_counts()
    plt.figure(figsize=(10, 8))
    tech_counts.head(10).plot(kind="pie", autopct="%1.1f%%")
    plt.title("Top 10 Technologies for Python Developers")
    plt.ylabel("")
    plt.show()


if __name__ == "__main__":
    file_path = "vacancies.csv"
    data = load_data(file_path)
    data = preprocess_data(data)
    tech_series = analyze_technologies(data)
    plot_top_technologies(tech_series)
