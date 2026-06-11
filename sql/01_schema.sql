DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customerID        VARCHAR(10) PRIMARY KEY,
    gender            VARCHAR(10),
    SeniorCitizen     SMALLINT,
    Partner           VARCHAR(3),
    Dependents        VARCHAR(3),
    tenure            SMALLINT,
    PhoneService      VARCHAR(3),
    MultipleLines     VARCHAR(20),
    InternetService   VARCHAR(20),
    OnlineSecurity    VARCHAR(20),
    OnlineBackup      VARCHAR(20),
    DeviceProtection  VARCHAR(20),
    TechSupport       VARCHAR(20),
    StreamingTV       VARCHAR(20),
    StreamingMovies   VARCHAR(20),
    Contract          VARCHAR(20),
    PaperlessBilling  VARCHAR(3),
    PaymentMethod     VARCHAR(30),
    MonthlyCharges    NUMERIC(10, 2),
    TotalCharges      NUMERIC(10, 2),
    Churn             SMALLINT
);