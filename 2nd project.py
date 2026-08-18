import pandas as pd
import pyodbc


# =====================================================
# 1. EXTRACT
# =====================================================

print("========== EXTRACT ==========")

# Read School CSV
school = pd.read_csv("school_different_data.csv")

# Read College CSV
college = pd.read_csv("college_different_data.csv")

print("\nSchool Data:")
print(school.head())

print("\nCollege Data:")
print(college.head())


# =====================================================
# 2. TRANSFORMATION
# =====================================================

print("\n========== TRANSFORMATION ==========")


# ---------- Clean column names ----------

school.columns = school.columns.str.strip().str.lower()
college.columns = college.columns.str.strip().str.lower()


# ---------- Remove duplicate records ----------

school = school.drop_duplicates()
college = college.drop_duplicates()


# ---------- Clean text columns ----------

school["student_name"] = (
    school["student_name"]
    .astype(str)
    .str.strip()
)

school["school_name"] = (
    school["school_name"]
    .astype(str)
    .str.strip()
)

school["city"] = (
    school["city"]
    .astype(str)
    .str.strip()
    .str.title()
)


college["college_name"] = (
    college["college_name"]
    .astype(str)
    .str.strip()
)

college["department"] = (
    college["department"]
    .astype(str)
    .str.strip()
)

college["city"] = (
    college["city"]
    .astype(str)
    .str.strip()
    .str.title()
)


# ---------- Convert numeric columns ----------

school["student_id"] = pd.to_numeric(
    school["student_id"],
    errors="coerce"
)

school["class"] = pd.to_numeric(
    school["class"],
    errors="coerce"
)

college["college_id"] = pd.to_numeric(
    college["college_id"],
    errors="coerce"
)

college["students"] = pd.to_numeric(
    college["students"],
    errors="coerce"
)


# ---------- Handle NULL values ----------

school = school.dropna(
    subset=[
        "student_id",
        "student_name",
        "city"
    ]
)

college = college.dropna(
    subset=[
        "college_id",
        "college_name",
        "city"
    ]
)


# ---------- Convert ID to integer ----------

school["student_id"] = school["student_id"].astype(int)
college["college_id"] = college["college_id"].astype(int)


print("\nClean School Data:")
print(school)

print("\nClean College Data:")
print(college)


# =====================================================
# 3. JOIN
# =====================================================

print("\n========== JOIN ==========")

# Join School and College using city

final_df = school.merge(
    college,
    on="city",
    how="inner"
)

print("\nJoined Data:")
print(final_df)


# =====================================================
# 4. WINDOW FUNCTION
# =====================================================

print("\n========== WINDOW FUNCTION ==========")


# Rank colleges according to number of students
# within each city

final_df["college_rank"] = (
    final_df
    .groupby("city")["students"]
    .rank(
        method="dense",
        ascending=False
    )
)


# Calculate average college students in each city

final_df["city_average_students"] = (
    final_df
    .groupby("city")["students"]
    .transform("mean")
)


# Calculate difference from city average

final_df["difference_from_average"] = (
    final_df["students"]
    - final_df["city_average_students"]
)


print("\nWindow Function Result:")
print(final_df)


# =====================================================
# 5. CREATE FINAL DATASET
# =====================================================

print("\n========== FINAL DATA ==========")

print(final_df)

print("\nColumns:")
print(final_df.columns.tolist())


# =====================================================
# 6. LOAD INTO SQL SERVER
# =====================================================

print("\n========== LOAD ==========")


# SQL Server connection
conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost\SQLEXPRESS;"
    r"DATABASE=connection_python;"
    r"Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("SQL Server connected!")


# =====================================================
# 7. CREATE TABLE
# =====================================================

create_table = """
IF OBJECT_ID('dbo.school_college_etl', 'U') IS NULL

CREATE TABLE dbo.school_college_etl
(
    id INT IDENTITY(1,1) PRIMARY KEY,

    student_id INT NOT NULL,

    student_name VARCHAR(100),

    school_name VARCHAR(100),

    class INT,

    city VARCHAR(100),

    college_id INT,

    college_name VARCHAR(100),

    department VARCHAR(100),

    students INT,

    college_rank INT,

    city_average_students DECIMAL(10,2),

    difference_from_average DECIMAL(10,2)
)
"""

cursor.execute(create_table)

conn.commit()

print("Table created!")


# =====================================================
# 8. INSERT DATA
# =====================================================

insert_query = """
INSERT INTO dbo.school_college_etl
(
    student_id,
    student_name,
    school_name,
    class,
    city,
    college_id,
    college_name,
    department,
    students,
    college_rank,
    city_average_students,
    difference_from_average
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


for row in final_df.itertuples(index=False, name=None):

    cursor.execute(
        insert_query,
        row
    )


# =====================================================
# 9. COMMIT
# =====================================================

conn.commit()

print("Data loaded successfully!")


# =====================================================
# 10. CLOSE CONNECTION
# =====================================================

cursor.close()
conn.close()

print("SQL Server connection closed.")

print("\n========== ETL COMPLETED ==========")


final_df["college_rank"] = (
    final_df.groupby("city")["students"]
    .rank(method="dense", ascending=False)
)


final_df["city_average_students"] = (
    final_df.groupby("city")["students"]
    .transform("mean")
)


final_df["difference_from_average"] = (
    final_df["students"]
    - final_df["city_average_students"]
)


import pandas as pd
import pyodbc


# =====================================================
# 1. EXTRACT - CSV FILES
# =====================================================

print("========== EXTRACT ==========")

school = pd.read_csv("school_different_data.csv")
college = pd.read_csv("college_different_data.csv")

print("School:")
print(school.head())

print("\nCollege:")
print(college.head())


# =====================================================
# 2. TRANSFORMATION
# =====================================================

print("\n========== TRANSFORMATION ==========")

# Clean column names
school.columns = school.columns.str.strip().str.lower()
college.columns = college.columns.str.strip().str.lower()

# Remove duplicates
school = school.drop_duplicates()
college = college.drop_duplicates()

# Clean text
school["student_name"] = school["student_name"].str.strip()
school["school_name"] = school["school_name"].str.strip()
school["city"] = school["city"].str.strip().str.title()

college["college_name"] = college["college_name"].str.strip()
college["department"] = college["department"].str.strip()
college["city"] = college["city"].str.strip().str.title()

# Convert numeric columns
school["student_id"] = pd.to_numeric(
    school["student_id"],
    errors="coerce"
)

school["class"] = pd.to_numeric(
    school["class"],
    errors="coerce"
)

college["college_id"] = pd.to_numeric(
    college["college_id"],
    errors="coerce"
)

college["students"] = pd.to_numeric(
    college["students"],
    errors="coerce"
)

# Remove NULL values
school = school.dropna(
    subset=["student_id", "student_name", "city"]
)

college = college.dropna(
    subset=["college_id", "college_name", "city"]
)

# Convert IDs
school["student_id"] = school["student_id"].astype(int)
school["class"] = school["class"].astype(int)

college["college_id"] = college["college_id"].astype(int)
college["students"] = college["students"].astype(int)


print("\nTransformation completed!")


# =====================================================
# 3. CONNECT PYTHON TO SQL SERVER
# =====================================================

print("\n========== SQL CONNECTION ==========")

conn = pyodbc.connect(
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=localhost\SQLEXPRESS;"
    r"DATABASE=connection_python;"
    r"Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("SQL Server connected successfully!")


# =====================================================
# 4. CREATE SCHOOL TABLE
# =====================================================

cursor.execute("""
IF OBJECT_ID('dbo.school_raw', 'U') IS NULL
BEGIN

    CREATE TABLE dbo.school_raw
    (
        student_id INT PRIMARY KEY,
        student_name VARCHAR(100) NOT NULL,
        school_name VARCHAR(100),
        class INT,
        city VARCHAR(100)
    )

END
""")

conn.commit()

print("School table ready!")


# =====================================================
# 5. CREATE COLLEGE TABLE
# =====================================================

cursor.execute("""
IF OBJECT_ID('dbo.college_raw', 'U') IS NULL
BEGIN

    CREATE TABLE dbo.college_raw
    (
        college_id INT PRIMARY KEY,
        college_name VARCHAR(100) NOT NULL,
        department VARCHAR(100),
        city VARCHAR(100),
        students INT
    )

END
""")

conn.commit()

print("College table ready!")


# =====================================================
# 6. LOAD SCHOOL CSV INTO SQL SERVER
# =====================================================

school_insert = """
INSERT INTO dbo.school_raw
(
    student_id,
    student_name,
    school_name,
    class,
    city
)
VALUES (?, ?, ?, ?, ?)
"""

for row in school.itertuples(index=False, name=None):

    cursor.execute(
        school_insert,
        row
    )

conn.commit()

print("School data loaded!")


# =====================================================
# 7. LOAD COLLEGE CSV INTO SQL SERVER
# =====================================================

college_insert = """
INSERT INTO dbo.college_raw
(
    college_id,
    college_name,
    department,
    city,
    students
)
VALUES (?, ?, ?, ?, ?)
"""

for row in college.itertuples(index=False, name=None):

    cursor.execute(
        college_insert,
        row
    )

conn.commit()

print("College data loaded!")


# =====================================================
# 8. SQL JOIN + WINDOW FUNCTION
# =====================================================

print("\n========== JOIN + WINDOW FUNCTION ==========")

cursor.execute("""

IF OBJECT_ID('dbo.school_college_final', 'U') IS NOT NULL
    DROP TABLE dbo.school_college_final;


SELECT

    s.student_id,
    s.student_name,
    s.school_name,
    s.class,
    s.city,

    c.college_id,
    c.college_name,
    c.department,
    c.students,

    -- WINDOW FUNCTION
    DENSE_RANK() OVER (
        PARTITION BY c.city
        ORDER BY c.students DESC
    ) AS college_rank,

    -- WINDOW FUNCTION
    AVG(c.students) OVER (
        PARTITION BY c.city
    ) AS city_average_students

INTO dbo.school_college_final

FROM dbo.school_raw AS s

INNER JOIN dbo.college_raw AS c
    ON s.city = c.city;

""")


conn.commit()

print("JOIN + Window Function completed!")


# =====================================================
# 9. SHOW FINAL DATA
# =====================================================

cursor.execute("""
SELECT *
FROM dbo.school_college_final
""")

rows = cursor.fetchall()

print("\n========== FINAL DATA ==========")

for row in rows:
    print(row)


# =====================================================
# 10. CLOSE CONNECTION
# =====================================================

cursor.close()
conn.close()

print("\nSQL Server connection closed!")
print("\n========== ETL COMPLETED ==========")