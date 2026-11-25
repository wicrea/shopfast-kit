"""CTP 2 - Exercise 1 STARTER: profile customers.csv with pandas.
Run from the 02_CTP2 folder:  python profile_customers_starter.py
Goal: measure at least 8 rules (2 per dimension) and copy the numbers into quality_scorecard_template.csv
"""
import pandas as pd

df = pd.read_csv("../shopfast-kit/data/customers.csv", dtype=str)   # dtype=str: keep the raw text (e.g. 01300)
n = len(df)
print("Rows:", n)
print(df.head())

# --- Completeness: how many empty values per column? ---
print("\nEmpty values per column:\n", df.isna().sum())

# --- Uniqueness: is customer_id unique? ---
print("\nDuplicated customer_id rows:", df["customer_id"].duplicated(keep=False).sum())
import pandas as pd

n = len(df)

# TODO 1 (Uniqueness): normalise email (strip + lower case) and count people registered twice
df["email"]=df["email"].str.lower()
df["email"]=df["email"].str.strip(" ")
email_dup_fail = df["email"].duplicated(keep=False)
print("\nDuplicated email rows:", email_dup_fail.sum())
df= df.drop_duplicates(subset=["email"])
print("\nDuplicated email rows:", df["email"].duplicated(keep=False).sum())

# TODO 2 (Validity): count emails that do not match the regex  ^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$   (hint: .str.match)
mask = df["email"].str.match(r'^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$').fillna(False)
email_fail = ~mask
print("email not match regex", (~mask).sum())
# TODO 3 (Consistency): list the distinct values of country with value_counts() - how many spellings for 4 countries?
print("country:",df["country"].value_counts())
# France: 5 , Germany: 4, Belgium:4, Spain:4
# TODO 4 (Consistency): count signup_date values that are NOT in the format YYYY-MM-DD
mask2=df["signup_date"].str.match(r'^\d{4}-\d{2}-\d{2}$').fillna(False)
signup_fail = ~mask2
print("signup_date not match regex", (~mask2).sum())
# TODO 5 (Validity): loyalty_tier values outside bronze / silver / gold / platinum
allowed = {'bronze', 'silver', 'gold', 'platinum'}
mask3=df["loyalty_tier"].astype(str).str.strip().str.lower().isin(allowed)
tier_fail = ~mask3
print("loyalty_tier not match regex", (~mask3).sum())
# TODO 6 (Accuracy): birth dates in the future or before 1906
birth_fail = (lambda b: b.isna() | (b > pd.Timestamp.today()) | (b < pd.Timestamp('1906-01-01')))(pd.to_datetime(df['birth_date'], errors='coerce'))
print(" not match regex",birth_fail.sum())
# TODO 7 (Validity): French postal codes that do not have 5 digits
mask4=df['postal_code'].astype(str).str.strip().str.match(r'^\d{5}$', na=False)
postal_fail = ~mask4
print("postal_code not match regex", (~mask4).sum())
# Bonus: compute score_pct = 100 * (1 - failing_rows / n) for each rule
rules = {
    "TODO 1 email uniqueness": email_dup_fail,
    "TODO 2 email regex":      email_fail,
    "TODO 4 signup_date":      signup_fail,
    "TODO 5 loyalty_tier":     tier_fail,
    "TODO 6 birth_date":       birth_fail,
    "TODO 7 postal_code":      postal_fail,
}
score_df = pd.DataFrame(
    {k: {"failing_rows": int(v.sum()), "total": len(v),
         "score_%": round(100 * (1 - v.sum()/len(v)), 2)}
     for k, v in rules.items()}
).T
print("\n", score_df)