import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine, text

# -------------------------------
# 1. MySQL Connection
# -------------------------------
DB_USER = "root"
DB_PASS = "Sundar_46"   # <- replace with your MySQL password
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "cricket_matches"

# Connect to MySQL
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}")
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
    conn.execute(text(f"USE {DB_NAME}"))

# Reconnect directly to cricket_matches DB
engine = create_engine(f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# -------------------------------
# 2. Create DataFrames (with Winner column)
# -------------------------------
odi_data = [
    ("ODI1", "IND", "PAK", "2023-09-13", "Colombo", 356, 128, "IND"),
    ("ODI2", "IND", "WI", "2023-07-27", "Bridgetown", 181, 182, "WI")
]

t20_data = [
    ("T201", "IND", "PAK", "2024-06-09", "New York", 165, 159, "IND"),
    ("T202", "IND", "AUS", "2024-06-24", "Gros Islet", 205, 181, "IND")
]

test_data = [
    ("TEST1", "IND", "ENG", "2025-06-20", "Leeds", 390, 280, "IND"),
    ("TEST2", "IND", "ENG", "2025-07-02", "Birmingham", 412, 415, "ENG")
]

ipl_data = [
    ("IPL2023", "CSK", "GT", "2023-05-28", "Ahmedabad", 171, 178, "CSK"),
    ("IPL2024", "SRH", "KKR", "2024-05-26", "Chennai", 159, 161, "KKR")
]

odi_df = pd.DataFrame(odi_data, columns=["Match_Code", "Team1", "Team2", "Match_Date", "Venue", "Innings1_Score", "Innings2_Score", "Winner"])
t20_df = pd.DataFrame(t20_data, columns=["Match_Code", "Team1", "Team2", "Match_Date", "Venue", "Innings1_Score", "Innings2_Score", "Winner"])
test_df = pd.DataFrame(test_data, columns=["Match_Code", "Team1", "Team2", "Match_Date", "Venue", "Innings1_Score", "Innings2_Score", "Winner"])
ipl_df = pd.DataFrame(ipl_data, columns=["Match_Code", "Team1", "Team2", "Match_Date", "Venue", "Innings1_Score", "Innings2_Score", "Winner"])

# Insert into MySQL
odi_df.to_sql("odi_matches", engine, if_exists="replace", index=False)
t20_df.to_sql("t20_matches", engine, if_exists="replace", index=False)
test_df.to_sql("test_matches", engine, if_exists="replace", index=False)
ipl_df.to_sql("ipl_matches", engine, if_exists="replace", index=False)

print("✅ Inserted ODI, T20, Test, and IPL matches into MySQL with Winner column")

# -------------------------------
# 3. Queries for Analysis
# -------------------------------
queries = {
    "matches_per_format": """
        SELECT 'ODI' as Format, COUNT(*) as Matches FROM odi_matches
        UNION ALL
        SELECT 'T20', COUNT(*) FROM t20_matches
        UNION ALL
        SELECT 'TEST', COUNT(*) FROM test_matches
        UNION ALL
        SELECT 'IPL', COUNT(*) FROM ipl_matches;
    """,
    "matches_per_venue": """
        SELECT Venue, COUNT(*) as Matches FROM (
            SELECT Venue FROM odi_matches
            UNION ALL
            SELECT Venue FROM t20_matches
            UNION ALL
            SELECT Venue FROM test_matches
            UNION ALL
            SELECT Venue FROM ipl_matches
        ) x GROUP BY Venue ORDER BY Matches DESC;
    """,
    "matches_per_team": """
        SELECT Team, COUNT(*) as Matches FROM (
            SELECT Team1 as Team FROM odi_matches
            UNION ALL
            SELECT Team2 FROM odi_matches
            UNION ALL
            SELECT Team1 FROM t20_matches
            UNION ALL
            SELECT Team2 FROM t20_matches
            UNION ALL
            SELECT Team1 FROM test_matches
            UNION ALL
            SELECT Team2 FROM test_matches
            UNION ALL
            SELECT Team1 FROM ipl_matches
            UNION ALL
            SELECT Team2 FROM ipl_matches
        ) x GROUP BY Team ORDER BY Matches DESC;
    """,
    "matches_per_winner": """
        SELECT Winner, COUNT(*) as Wins FROM (
            SELECT Winner FROM odi_matches
            UNION ALL
            SELECT Winner FROM t20_matches
            UNION ALL
            SELECT Winner FROM test_matches
            UNION ALL
            SELECT Winner FROM ipl_matches
        ) x GROUP BY Winner ORDER BY Wins DESC;
    """
}

# -------------------------------
# 4. Run Queries and Export CSVs
# -------------------------------
for name, q in queries.items():
    with engine.connect() as conn:
        df_result = pd.read_sql(text(q), conn)
        df_result.to_csv(f"{name}.csv", index=False)
        print(f"✅ Saved {name}.csv")

# -------------------------------
# 5. Graphs
# -------------------------------
# Graph 1: Matches per Format
df1 = pd.read_csv("matches_per_format.csv")
plt.figure(figsize=(6,4))
sns.barplot(x="Format", y="Matches", data=df1)
plt.title("Matches per Format")
plt.savefig("matches_per_format.png")
plt.show()

# Graph 2: Matches per Venue
df2 = pd.read_csv("matches_per_venue.csv")
plt.figure(figsize=(7,4))
sns.barplot(x="Venue", y="Matches", data=df2)
plt.title("Matches per Venue")
plt.xticks(rotation=45)
plt.savefig("matches_per_venue.png")
plt.show()

# Graph 3: Matches per Team
df3 = pd.read_csv("matches_per_team.csv")
plt.figure(figsize=(7,4))
sns.barplot(x="Team", y="Matches", data=df3)
plt.title("Matches per Team")
plt.savefig("matches_per_team.png")
plt.show()

# Graph 4: Matches per Winner
df4 = pd.read_csv("matches_per_winner.csv")
plt.figure(figsize=(6,4))
sns.barplot(x="Winner", y="Wins", data=df4)
plt.title("Matches per Winner")
plt.savefig("matches_per_winner.png")
plt.show()

print("✅ Graphs saved (PNG files)")
