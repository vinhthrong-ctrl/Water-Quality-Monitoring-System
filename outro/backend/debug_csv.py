import csv

file_path = "../data/water_potability.csv"

EXPECTED_COLS = 12

broken_rows = []
extra_cols = 0
missing_cols = 0
ok_rows = 0

with open(file_path, "r", encoding="latin1") as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader):

        col_count = len(row)

        # skip header safely
        if i == 0:
            continue

        if col_count == EXPECTED_COLS:
            ok_rows += 1

        elif col_count > EXPECTED_COLS:
            extra_cols += 1
            broken_rows.append({
                "row": i,
                "issue": "EXTRA COLUMNS",
                "count": col_count,
                "preview": row[:6]
            })

        elif col_count < EXPECTED_COLS:
            missing_cols += 1
            broken_rows.append({
                "row": i,
                "issue": "MISSING COLUMNS",
                "count": col_count,
                "preview": row
            })

# ----------------------------
# RESULTS SUMMARY
# ----------------------------
print("\n===== DATASET REPORT =====")
print("Valid rows:", ok_rows)
print("Extra column rows:", extra_cols)
print("Missing column rows:", missing_cols)
print("Total broken rows:", len(broken_rows))

# ----------------------------
# SHOW SAMPLE ISSUES
# ----------------------------
print("\n===== SAMPLE BROKEN ROWS =====\n")

for r in broken_rows[:15]:
    print(f"Row {r['row']}")
    print("Issue:", r["issue"])
    print("Columns:", r["count"])
    print("Preview:", r["preview"])
    print("-" * 40)

# ----------------------------
# SAVE BROKEN ROWS TO FILE
# ----------------------------
import json

with open("broken_rows.json", "w") as f:
    json.dump(broken_rows, f, indent=2)

print("\nBroken rows saved to broken_rows.json ✅")