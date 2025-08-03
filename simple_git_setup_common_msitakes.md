Here's a practical guide for setting up Git and handling common issues:

## Initial Git Setup

**Install Git** (if not already installed):

- Windows: Download from git-scm.com or use `winget install Git.Git`
- Mac: `brew install git` or install Xcode Command Line Tools
- Linux: `sudo apt install git` (Ubuntu/Debian) or `sudo yum install git` (RHEL/CentOS)

**Configure your identity** (required for commits):

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Optional but recommended settings**:

```bash
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.autocrlf true  # Windows only
git config --global core.autocrlf input # Mac/Linux
```

## Basic Workflow Setup

**Initialize a repository**:

```bash
git init
# or clone existing repo
git clone https://github.com/username/repo.git
```

**Check repository status**:

```bash
git status
git log --oneline
```

## Most Common Mistakes and Fixes

**1. Forgot to configure user info**

```bash
# Error: "Please tell me who you are"
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**2. Added wrong files to staging**

```bash
# Remove from staging (keeps file changes)
git reset HEAD filename
# or remove all staged files
git reset HEAD .
```

**3. Made a commit with wrong message**

```bash
# Fix the last commit message
git commit --amend -m "Correct message"
```

**4. Want to undo last commit but keep changes**

```bash
git reset --soft HEAD~1
```

**5. Accidentally committed sensitive files**

```bash
# Remove from tracking but keep local file
git rm --cached filename
# Add to .gitignore to prevent future commits
echo "filename" >> .gitignore
```

**6. Branch conflicts during merge/pull**

```bash
# See which files have conflicts
git status
# Edit files to resolve conflicts, then
git add .
git commit -m "Resolve merge conflicts"
```

**7. Pushed to wrong branch**

```bash
# Create new branch from current state
git checkout -b correct-branch-name
# Switch back and reset the wrong branch
git checkout wrong-branch
git reset --hard HEAD~1
```

## Essential Daily Commands

```bash
# Check what's changed
git status
git diff

# Stage and commit changes
git add .
git commit -m "Descriptive message"

# Push to remote
git push origin branch-name

# Pull latest changes
git pull origin branch-name

# Create and switch to new branch
git checkout -b new-feature-branch
```

## Quick Health Checks

**Verify your setup**:

```bash
git config --list
git remote -v
git branch -a
```

**Clean up if things get messy**:

```bash
# Discard all local changes
git restore .
# or the old way
git checkout .

# Remove untracked files
git clean -fd
```

The key to avoiding most Git problems is checking `git status` frequently and making small, focused commits with clear
messages. When in doubt, create a backup branch before trying fixes!

>> **The golden rule: **when in doubt, backup first!** It takes 5 seconds and can save hours of work recovery.**
Here are several ways to create backup branches before attempting fixes:

## Quick Backup Methods

**1. Simple backup of current branch**
```bash
# Creates backup-YYYY-MM-DD branch from current state
git checkout -b backup-$(date +%Y-%m-%d)
# Then switch back to original branch
git checkout main  # or whatever branch you were on
```

**2. Backup with descriptive name**
```bash
# Create backup with specific name
git checkout -b backup-before-merge-fix
git checkout main  # switch back to working branch
```

**3. Backup without switching branches**
```bash
# Create backup branch but stay on current branch
git branch backup-current-work
# Verify it was created
git branch
```

## Before Specific Risky Operations

**Before attempting a rebase**:
```bash
git checkout -b backup-before-rebase
git checkout feature-branch
git rebase main  # now safe to try
```

**Before merge conflict resolution**:
```bash
git branch backup-before-merge
# Continue with merge...
```

**Before hard reset or other destructive commands**:
```bash
git branch backup-$(date +%H%M)  # timestamp backup
git reset --hard HEAD~3  # now safe to reset
```

## Advanced Backup Strategies

**1. Tag important states**
```bash
# Create a tag for easy reference
git tag backup-v1.0-before-refactor
# Tags persist even if branches are deleted
```

**2. Create backup with commit message**
```bash
git checkout -b backup-login-feature
git checkout main
# Add a commit describing what you're about to try
git commit --allow-empty -m "About to attempt risky merge"
```

**3. Multiple backup points**
```bash
# Before starting risky work
git branch backup-start-point

# After partial progress
git branch backup-partial-fix

# Before final dangerous step
git branch backup-before-final-step
```

## Restoring from Backups

**If something goes wrong**:
```bash
# See all your backup branches
git branch | grep backup

# Switch to backup
git checkout backup-before-merge-fix

# Create new working branch from backup
git checkout -b attempt-2

# Or merge backup into current branch
git checkout main
git merge backup-before-merge-fix
```

**Clean up old backups**:
```bash
# List backup branches
git branch | grep backup

# Delete backup branch you no longer need
git branch -d backup-2024-01-15

# Force delete if it has unmerged changes
git branch -D backup-before-failed-rebase
```

## Pro Tips

**Automated backup function** (add to your shell profile):
```bash
# Add to ~/.bashrc or ~/.zshrc
gitbackup() {
    local branch_name="backup-$(date +%Y%m%d-%H%M%S)"
    git branch "$branch_name"
    echo "Created backup branch: $branch_name"
}

# Usage: just type 'gitbackup' before risky operations
```

**Quick verification**:
```bash
# Make sure backup was created correctly
git log --oneline backup-branch-name

# Compare current branch to backup
git diff backup-branch-name
```

**Emergency "oh no" recovery**:
```bash
# If you realize you need a backup AFTER messing up
# Git keeps commits for ~30 days in reflog
git reflog
# Find the commit hash before your mistake
git checkout -b emergency-recovery abc1234
```

