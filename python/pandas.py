# Pandas snippets
import pandas as pd

# if else conditional
np.where(df.a == 1, "is_one", "not_one")

# Conditional-like "CASE"
np.select(
    [
        df.a == 1,
        df.a == 2,
    ],
    [
        "is_one",
        "is_two",
    ],
    default="is_not_one_or_two",
)

# Plotting backend
pd.options.plotting.backend = "altair"  # or "plotly"

# Named aggregation
df.groupby("A").agg(
    sum_b=("B", "sum"),
    std_c=("C", "std")
)
