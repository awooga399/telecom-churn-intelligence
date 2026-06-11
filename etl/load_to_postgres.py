import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # читает .env и кладёт переменные в окружение

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.loc[(df["tenure"] == 0) & (df["TotalCharges"].isna()), "TotalCharges"] = 0
    df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})
    df.columns = df.columns.str.lower()
    return df

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

def main():
    df = pd.read_csv("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    df = clean_data(df)

    df.to_sql(
        name="customers",
        con=engine,
        if_exists="append",   # <-- подумай над этим параметром
        index=False,
    )
    print(f"Загружено строк: {len(df)}")


if __name__ == "__main__":
    main()

