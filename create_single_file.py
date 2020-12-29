import os
import json

INDENT = 2
OUTPUT_FILE = "indent.json"


files = [f for f in os.listdir() if f[:7] == "output_" and f[-5:] == ".json"]
customers = []


print("Loading")

for filename in files:
    with open(filename, "r", encoding="utf8") as f:
        data = json.load(f)
        customers.extend(data["customers"])

with open(OUTPUT_FILE, "w", encoding="utf8") as f:
    json.dump(customers, f, ensure_ascii=False, indent=INDENT)

print(f"Saved {len(customers)} customers to {OUTPUT_FILE} (indent = {INDENT})")
print(
    f"max customerNumber = {max([customer['customerNumber'] for customer in customers])}")  # @fix speedup
