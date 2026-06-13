create database IdentityAccessRiskAnalytics;
use IdentityAccessRiskAnalytics;
select DB_NAME() as CurrentDatabase;
CREATE TABLE security_events
(
    Event_ID INT,
    Timestamp DATETIME,
    User_ID VARCHAR(20),
    Department VARCHAR(50),
    Role VARCHAR(50),
    Country VARCHAR(50),
    Device_Type VARCHAR(50),
    Login_Status VARCHAR(20),
    Failed_Attempts INT,
    Resource_Accessed VARCHAR(100),
    Privileged_Access VARCHAR(10),
    Hour INT,
    Normal_Country VARCHAR(50),
    Normal_Device VARCHAR(50),
    Risk_Score INT,
    Risk_Level VARCHAR(20)
);
CREATE TABLE user_risk_profiles
(
    User_ID VARCHAR(20),
    Average_Risk_Score FLOAT,
    Risk_Category VARCHAR(20)
);
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES;


SELECT COUNT(*) AS TotalRows
FROM risk_scored_data;

DROP TABLE user_risk_profiles;

SELECT COUNT(*) AS TotalRows
FROM user_risk_profiles;

SELECT TOP 10
    User_ID,
    Average_Risk_Score,
    Risk_Category
FROM user_risk_profiles
ORDER BY Average_Risk_Score DESC;


SELECT
    Risk_Category,
    COUNT(*) AS User_Count
FROM user_risk_profiles
GROUP BY Risk_Category
ORDER BY User_Count DESC;

SELECT
    Department,
    AVG(Risk_Score) AS Avg_Risk
FROM risk_scored_data
GROUP BY Department
ORDER BY Avg_Risk DESC;


SELECT
    Department,
    COUNT(*) AS Critical_Events
FROM risk_scored_data
WHERE Risk_Level = 'Critical'
GROUP BY Department
ORDER BY Critical_Events DESC;

SELECT
    Country,
    COUNT(*) AS Anomaly_Count
FROM risk_scored_data
WHERE Country <> Normal_Country
GROUP BY Country
ORDER BY Anomaly_Count DESC;

SELECT TOP 5 *
FROM risk_scored_data;


