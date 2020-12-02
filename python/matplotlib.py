"""Snippets for matplotlib."""

# Place legend under chart
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0), ncol=5)

# Increase pixel density in notebooks
%config InlineBackend.figure_format='retina'

# Remove vertial grid lines
ax.xaxis.grid(False)

# Start graph
fig, ax = plt.subplots(figsize=(20, 7))

# Zoomed insert
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset, zoomed_inset_axes
axins = zoomed_inset_axes(ax, zoom=7, loc="upper right")
axins = inset_axes(ax, width=5, height=3, loc="upper right")
axins.plot(x, y)
axins.xaxis.set_visible(False)
axins.yaxis.set_visible(False)
mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec=0.5)  # Adds lines that connect to their points to the original plot
