import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# -----------------------------
# Configuration
# -----------------------------

NUM_USERS = 500
NUM_EVENTS = 50000

DEPARTMENTS = [
    "Finance",
    "HR",
    "IT",
    "Sales",
    "Operations"
]

ROLES = [
    "Analyst",
    "Manager",
    "Engineer",
    "Administrator"
]

COUNTRIES = [
    "India",
    "USA",
    "Germany",
    "Singapore",
    "UK"
]

DEVICE_TYPES = [
    "Laptop",
    "Desktop",
    "Mobile"
]

RESOURCES = [
    "Payroll System",
    "CRM",
    "Database",
    "Email",
    "Admin Portal"
]

# -----------------------------
# Create Employee Profiles
# -----------------------------

employees = {}

for i in range(1, NUM_USERS + 1):

    user_id = f"EMP_{i:04d}"

    employees[user_id] = {
        "Department": random.choice(DEPARTMENTS),
        "Role": random.choice(ROLES),
        "Home_Country": random.choice(COUNTRIES),
        "Primary_Device": random.choice(DEVICE_TYPES),
        "Work_Start": random.choice([8, 9, 10]),
        "Work_End": random.choice([17, 18, 19])
    }

# -----------------------------
# Generate Login Events
# -----------------------------

records = []

start_date = datetime(2025, 1, 1)

for event_id in range(1, NUM_EVENTS + 1):

    user = random.choice(list(employees.keys()))

    profile = employees[user]

    timestamp = start_date + timedelta(
        minutes=random.randint(0, 525600)
    )

    # 90% normal behavior
    if random.random() < 0.90:

        country = profile["Home_Country"]
        device = profile["Primary_Device"]

    else:

        country = random.choice(COUNTRIES)
        device = random.choice(DEVICE_TYPES)

    login_status = np.random.choice(
        ["Success", "Failed"],
        p=[0.92, 0.08]
    )

    failed_attempts = (
        random.randint(1, 10)
        if login_status == "Failed"
        else 0
    )

    record = {
        "Event_ID": event_id,
        "Timestamp": timestamp,
        "User_ID": user,
        "Department": profile["Department"],
        "Role": profile["Role"],
        "Country": country,
        "Device_Type": device,
        "Login_Status": login_status,
        "Failed_Attempts": failed_attempts,
        "Resource_Accessed": random.choice(RESOURCES),
        "Privileged_Access": random.choice(
            ["Yes", "No"]
        )
    }

    records.append(record)

# -----------------------------
# Save Dataset
# -----------------------------

df = pd.DataFrame(records)

df.to_csv(
    "data/raw_login_data.csv",
    index=False
)

print("Dataset Created Successfully!")
print(df.head())
print("\nShape:", df.shape)