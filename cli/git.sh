# Useful git snippets

# Git cheatsheet: https://ndpsoftware.com/git-cheatsheet.html#loc=local_repo;

# Push to last commit
git commit --amend

# Fix an old commit
git add <new files>
git commit --fixup=OLDSHA
git rebase --interactive --autosquash OLDSHA^

# Interactively look through hunks to commit
# https://nuclearsquid.com/writings/git-add/
git add --patch

# Interactively add files
# https://nuclearsquid.com/writings/git-add/
git add --interactive
