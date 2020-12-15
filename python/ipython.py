"""Snippets and useful magic for Jupyter and iPython."""

# Increase pixel density in notebooks
%config InlineBackend.figure_format="retina"

# Reload imports
%load_ext autoreload
%autoreload 2

# Use variables in shell
name = "Steven"
!echo {name}
