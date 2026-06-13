# %%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

df = pd.read_sql("SELECT * FROM customers", engine)

# %%
sns.histplot(data=df, x="monthlycharges", hue="churn", bins=40,
             multiple="layer", kde=True, stat="probability", common_norm=False)
plt.title("Распределение месячного чека: ушедшие vs оставшиеся")
plt.xlabel("Месячный чек")
plt.ylabel("Доля клиентов")
plt.tight_layout()
plt.show()

# %%
sns.barplot(data=df, x="contract", y="churn", errorbar=None)
plt.title("Доля оттока по типу контракта")
plt.xlabel("Тип контракта")
plt.ylabel("Доля оттока (churn rate)")
plt.tight_layout()
plt.show()

# %%
sns.barplot(data=df, x="internetservice", y="churn", errorbar=None)
plt.title("Доля оттока по типу интернет-услуги")
plt.xlabel("Тип интернет-услуги")
plt.ylabel("Доля оттока (churn rate)")
plt.tight_layout()
plt.show()

# %%
fig, ax = plt.subplots(figsize=(9, 6))
hb = ax.hexbin(
    df["tenure"], df["monthlycharges"],
    C=df["churn"],                 # значение для агрегации
    reduce_C_function=np.mean,     # среднее от 0/1 = доля оттока
    gridsize=25, cmap="Reds", mincnt=5
)
ax.set_title("Churn rate в пространстве «стаж × чек»")
ax.set_xlabel("Стаж (месяцев)")
ax.set_ylabel("Месячный чек")
fig.colorbar(hb, ax=ax, label="Доля оттока в ячейке")
plt.tight_layout()
plt.show()

# %%
numeric_cols = ["tenure", "monthlycharges", "totalcharges"]
corr = df[numeric_cols].corr()

sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
plt.title("Корреляция числовых переменных")
plt.tight_layout()
plt.show()