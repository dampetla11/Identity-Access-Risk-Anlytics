import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

NUM_USERS = 500
NUM_EVENTS = 50000

departments = [
    "Finance",
    "HR",
    "IT",
    "Sales",
    "Operations"
]

roles = [
    "Analyst",
    "Manager",
    "Administrator",
    "Engineer"
]

countries = [
    "India",
    "USA",
    "Germany",
    "Singapore",
    "UK"
]

device_types = [
    "Laptop",
    "Desktop",
    "Mobile"
]

resources = [
    "Payroll System",
    "CRM",
    "Database",
    "Email",
    "Admin Portal"
]

users = [f"EMP_{i:04d}" for i in range(1, NUM_USERS + 1)]

records = []

start_date = datetime(2025, 1, 1)

for i in range(NUM_EVENTS):

    user = random.choice(users)

    timestamp = start_date + timedelta(
        minutes=random.randint(0, 525600)
    )

    login_status = np.random.choice(
        ["Success", "Failed"],
        p=[0.9, 0.1]
    )

    failed_attempts = (
        random.randint(1, 10)
        if login_status == "Failed"
        else 0
    )

    record = {
        "Event_ID": i + 1,
        "Timestamp": timestamp,
        "User_ID": user,
        "Department": random.choice(departments),
        "Role": random.choice(roles),
        "Country": random.choice(countries),
        "Device_Type": random.choice(device_types),
        "Login_Status": login_status,
        "Failed_Attempts": failed_attempts,
        "Resource_Accessed": random.choice(resources),
        "Privileged_Access": random.choice(
            ["Yes", "No"]
        )
    }

    records.append(record)

df = pd.DataFrame(records)

df.to_csv(
    "data/raw_login_data.csv",
    index=False
)

print("Dataset created successfully!")
print(df.head())