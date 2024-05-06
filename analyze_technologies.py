import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame
from pandas.core.series import Series


def load_data(filename: str) -> DataFrame:
    """Load data from a CSV file."""
    return pd.read_csv(filename)


def plot_top_vacancies(
    data: DataFrame,
    column: str,
    n: int = 5,
) -> None:
    """Plot top n vacancies based on the specified column."""
    top_vacancies = data.nlargest(n, column)
    top_vacancies.plot(kind="bar", x="vacancy_title", y=column)
    plt.title(f"Top {n} Vacancies by '{' '.join(column.split('_'))}'")
    plt.ylabel("Amount")
    plt.xlabel("")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


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

    plot_top_vacancies(data, "vacancy_views_amount")
    plot_top_vacancies(data, "vacancy_reviews_amount")
