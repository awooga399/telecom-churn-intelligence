# %%
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import joblib

load_dotenv()
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
df = pd.read_sql("SELECT * FROM customers", engine)

# %%
df = df.drop(columns=["customerid", "totalcharges"])

y = df["churn"]
X = df.drop(columns=["churn"])

X = pd.get_dummies(X, drop_first=True)

# %%
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.25,
    random_state=42,
    stratify=y
)
num_cols = ["tenure", "monthlycharges"]
scaler = StandardScaler()

X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test_scaled[num_cols]  = scaler.transform(X_test[num_cols])

model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
model.fit(X_train_scaled, y_train)

y_pred  = model.predict(X_test_scaled)
y_proba = model.predict_proba(X_test_scaled)[:, 1]

coefs = pd.DataFrame({
    "feature": X_train_scaled.columns,
    "coef": model.coef_[0]
}).sort_values("coef", ascending=False)

print(coefs.to_string(index=False))
print(classification_report(y_test, y_pred))
print("ROC-AUC:", round(roc_auc_score(y_test, y_proba), 3))
print(confusion_matrix(y_test, y_pred))

if os.path.basename(os.getcwd()) == "src":
    os.chdir("..")
joblib.dump(model, "models/churn_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("Модель и scaler сохранены")
predictions = pd.DataFrame({
    "churn_actual": y_test.values,
    "churn_proba": y_proba,
    "monthlycharges": X_test["monthlycharges"].values,
    "tenure": X_test["tenure"].values
}, index=y_test.index)

predictions.to_csv("data/processed/predictions.csv", index=True)
print("Предсказания сохранены:", predictions.shape)
print(predictions.head())