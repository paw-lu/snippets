# Pandas snippets
import pandas as pd

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
