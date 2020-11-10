"""Snippets for matplotlib."""

# Place legend under chart
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0), ncol=5)

# Increase pixel density in notebooks
%config InlineBackend.figure_format='retina'

# Remove vertial grid lines
ax.xaxis.grid(False)

# Start graph
fig, ax = plt.subplots(figsize=(20, 7))
