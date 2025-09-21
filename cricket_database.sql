-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS cricket_matches;
USE cricket_matches;

-- Step 2: Create ODI Table
DROP TABLE IF EXISTS odi_matches;
CREATE TABLE odi_matches (
    Match_Code VARCHAR(20) PRIMARY KEY,
    Team1 VARCHAR(50),
    Team2 VARCHAR(50),
    Match_Date DATE,
    Venue VARCHAR(100)
);

-- Step 3: Create T20 Table
DROP TABLE IF EXISTS t20_matches;
CREATE TABLE t20_matches (
    Match_Code VARCHAR(20) PRIMARY KEY,
    Team1 VARCHAR(50),
    Team2 VARCHAR(50),
    Match_Date DATE,
    Venue VARCHAR(100)
);

-- Step 4: Create Test Table
DROP TABLE IF EXISTS test_matches;
CREATE TABLE test_matches (
    Match_Code VARCHAR(20) PRIMARY KEY,
    Team1 VARCHAR(50),
    Team2 VARCHAR(50),
    Match_Dates TEXT,   -- multiple days stored as text
    Venue VARCHAR(100)
);

-- Step 5: Create IPL Table
DROP TABLE IF EXISTS ipl_matches;
CREATE TABLE ipl_matches (
    Match_Code VARCHAR(20) PRIMARY KEY,
    Team1 VARCHAR(50),
    Team2 VARCHAR(50),
    Match_Date DATE,
    Venue VARCHAR(100)
);

-- Step 6: Insert ODI Matches
INSERT INTO odi_matches (Match_Code, Team1, Team2, Match_Date, Venue) VALUES
('ODI1','IND','PAK','2023-09-13','Colombo'),
('ODI2','IND','WI','2023-07-27','Bridgetown');

-- Step 7: Insert T20 Matches
INSERT INTO t20_matches (Match_Code, Team1, Team2, Match_Date, Venue) VALUES
('T201','IND','PAK','2024-06-09','New York'),
('T202','IND','AUS','2024-06-24','Gros Islet');

-- Step 8: Insert Test Matches
INSERT INTO test_matches (Match_Code, Team1, Team2, Match_Dates, Venue) VALUES
('TEST1','IND','ENG','2025-06-20,2025-06-21,2025-06-22,2025-06-23,2025-06-24','Leeds'),
('TEST2','IND','ENG','2025-07-02,2025-07-03,2025-07-04,2025-07-05,2025-07-06','Birmingham');

-- Step 9: Insert IPL Matches
INSERT INTO ipl_matches (Match_Code, Team1, Team2, Match_Date, Venue) VALUES
('IPL1','CSK','GT','2023-03-31','Ahmedabad'),
('IPL2','CSK','LSG','2023-04-03','Chennai');

-- ✅ Data inserted successfully ✅


-- Step 10: Queries for Analysis

-- 1. Matches per format
SELECT 'ODI' AS Format, COUNT(*) AS Matches FROM odi_matches
UNION ALL
SELECT 'T20', COUNT(*) FROM t20_matches
UNION ALL
SELECT 'TEST', COUNT(*) FROM test_matches
UNION ALL
SELECT 'IPL', COUNT(*) FROM ipl_matches;

-- 2. Matches per venue
SELECT Venue, COUNT(*) AS Matches FROM (
    SELECT Venue FROM odi_matches
    UNION ALL
    SELECT Venue FROM t20_matches
    UNION ALL
    SELECT Venue FROM test_matches
    UNION ALL
    SELECT Venue FROM ipl_matches
) x GROUP BY Venue ORDER BY Matches DESC;

-- 3. Matches per team
SELECT Team, COUNT(*) AS Matches FROM (
    SELECT Team1 AS Team FROM odi_matches
    UNION ALL SELECT Team2 FROM odi_matches
    UNION ALL SELECT Team1 FROM t20_matches
    UNION ALL SELECT Team2 FROM t20_matches
    UNION ALL SELECT Team1 FROM test_matches
    UNION ALL SELECT Team2 FROM test_matches
    UNION ALL SELECT Team1 FROM ipl_matches
    UNION ALL SELECT Team2 FROM ipl_matches
) x GROUP BY Team ORDER BY Matches DESC;

-- 4. List ODI Matches
SELECT * FROM odi_matches;

-- 5. List T20 Matches
SELECT * FROM t20_matches;

-- 6. List Test Matches
SELECT * FROM test_matches;

-- 7. List IPL Matches
SELECT * FROM ipl_matches;

-- 8. Matches in 2023
SELECT Match_Code, Team1, Team2, Match_Date, Venue 
FROM odi_matches WHERE YEAR(Match_Date)=2023
UNION ALL
SELECT Match_Code, Team1, Team2, Match_Date, Venue 
FROM t20_matches WHERE YEAR(Match_Date)=2023
UNION ALL
SELECT Match_Code, Team1, Team2, Match_Date, Venue 
FROM ipl_matches WHERE YEAR(Match_Date)=2023;

-- 9. Matches in 2024
SELECT Match_Code, Team1, Team2, Match_Date, Venue 
FROM t20_matches WHERE YEAR(Match_Date)=2024;

-- 10. Matches in 2025 (Test Matches only)
SELECT * FROM test_matches;

-- 11. Matches grouped by country (Teams)
SELECT Country, COUNT(*) AS Matches FROM (
    SELECT Team1 AS Country FROM odi_matches
    UNION ALL SELECT Team2 FROM odi_matches
    UNION ALL SELECT Team1 FROM t20_matches
    UNION ALL SELECT Team2 FROM t20_matches
    UNION ALL SELECT Team1 FROM test_matches
    UNION ALL SELECT Team2 FROM test_matches
    UNION ALL SELECT Team1 FROM ipl_matches
    UNION ALL SELECT Team2 FROM ipl_matches
) x GROUP BY Country ORDER BY Matches DESC;
