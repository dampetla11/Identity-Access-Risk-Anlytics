import pandas as pd

# Load dataset
df = pd.read_csv("data/raw_login_data.csv")

print("Dataset Loaded Successfully!")
print("Rows, Columns:", df.shape)

# ----------------------------
# Convert Timestamp
# ----------------------------
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Extract Hour
df["Hour"] = df["Timestamp"].dt.hour
# ==========================
# USER BASELINES
# ==========================

user_country = (
    df.groupby("User_ID")["Country"]
    .agg(lambda x: x.mode()[0])
)

user_device = (
    df.groupby("User_ID")["Device_Type"]
    .agg(lambda x: x.mode()[0])
)

df["Normal_Country"] = df["User_ID"].map(
    user_country
)

df["Normal_Device"] = df["User_ID"].map(
    user_device
)

# ----------------------------
# Initialize Risk Score
# ----------------------------
df["Risk_Score"] = 0
# ==========================
# COUNTRY ANOMALY
# ==========================

df.loc[
    df["Country"] != df["Normal_Country"],
    "Risk_Score"
] += 25

# ==========================
# DEVICE ANOMALY
# ==========================

df.loc[
    df["Device_Type"] != df["Normal_Device"],
    "Risk_Score"
] += 20

# ----------------------------
# Failed Login Risk
# ----------------------------
df["Risk_Score"] += df["Failed_Attempts"] * 5

# ----------------------------
# Privileged Access Risk
# ----------------------------
df.loc[
    df["Privileged_Access"] == "Yes",
    "Risk_Score"
] += 15

# ----------------------------
# After Hours Risk
# Working Hours = 9AM to 6PM
# ----------------------------
df.loc[
    (df["Hour"] < 9) |
    (df["Hour"] > 18),
    "Risk_Score"
] += 10

# ----------------------------
# Login Failure Bonus Risk
# ----------------------------
df.loc[
    df["Login_Status"] == "Failed",
    "Risk_Score"
] += 10

# ----------------------------
# Risk Classification
# ----------------------------
def classify_risk(score):

    if score >= 50:
        return "Critical"

    elif score >= 30:
        return "High"

    elif score >= 15:
        return "Medium"

    else:
        return "Low"


df["Risk_Level"] = df["Risk_Score"].apply(classify_risk)

# ----------------------------
# Risk Summary
# ----------------------------
print("\nRisk Distribution:")
print(df["Risk_Level"].value_counts())

# ----------------------------
# Top Risky Events
# ----------------------------
print("\nTop 10 Highest Risk Events:")

top_risk = df.sort_values(
    by="Risk_Score",
    ascending=False
).head(10)

print(
    top_risk[
        [
            "User_ID",
            "Country",
            "Login_Status",
            "Failed_Attempts",
            "Risk_Score",
            "Risk_Level"
        ]
    ]
)

# ----------------------------
# Save Output
# ----------------------------
df.to_csv(
    "data/risk_scored_data.csv",
    index=False
)

print("\nRisk Scored Dataset Saved Successfully!")
print("File: data/risk_scored_data.csv")
print("\nTop Users By Event Count:")

print(
    df["User_ID"]
    .value_counts()
    .head()
)
print("\nCountry Anomalies:")
print(
    (df["Country"] != df["Normal_Country"]).sum()
)

print("\nDevice Anomalies:")
print(
    (df["Device_Type"] != df["Normal_Device"]).sum()
)
# ==========================
# USER RISK PROFILES
# ==========================

user_risk = (
    df.groupby("User_ID")["Risk_Score"]
    .mean()
    .reset_index()
)

user_risk.columns = [
    "User_ID",
    "Average_Risk_Score"
]

def classify_user_risk(score):

    if score >= 25:
        return "Critical"

    elif score >= 20:
        return "High"

    elif score >= 15:
        return "Medium"

    else:
        return "Low"


user_risk["Risk_Category"] = (
    user_risk["Average_Risk_Score"]
    .apply(classify_user_risk)
)

user_risk.to_csv(
    "data/user_risk_profiles.csv",
    index=False
)

print("\nTop 10 Riskiest Users")

print(
    user_risk[
        [
            "User_ID",
            "Average_Risk_Score",
            "Risk_Category"
        ]
    ]
    .sort_values(
        by="Average_Risk_Score",
        ascending=False
    )
    .head(10)
)