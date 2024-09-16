
# Github 101

## Why Do We Use GitHub?

GitHub is a platform that helps you manage your code. It allows multiple people to work on the same project, track changes, and collaborate. It's used by developers worldwide to keep their projects organized, share code with others, and store code online securely.

GitHub is like a super-powered folder on your computer where you can:
- **Save different versions of your code** so you can go back to older versions if something breaks.
- **Collaborate** with friends or classmates by sharing code.
- **Backup your code online** so you don't lose it.


## Essential Git Commands (That Cover 80% of GitHub Use Cases)
Here are the core commands and what they do, explained in simple terms:

Here are the core commands and what they do, explained in simple terms:

| Command                            | What it Does                                             |
|------------------------------------|----------------------------------------------------------|
| `git clone [URL]`                  | **Downloads** a project from GitHub to your computer.    |
| `git status`                       | **Checks** the status of your files (changed, staged, etc.). |
| `git add [file-name]`              | **Adds** a file to the list of changes to be saved.      |
| `git commit -m "message"`          | **Saves** your changes with a description (message).     |
| `git push`                         | **Uploads** your changes from your computer to GitHub.   |
| `git pull`                         | **Downloads** the latest changes from GitHub to your local copy. |
| `git branch`                       | **Lists** all branches (different versions) of the project. |
| `git checkout [branch-name]`       | **Switches** to a different branch.                      |
| `git merge [branch-name]`          | **Combines** changes from one branch into another.       |
| `git log`                          | **Shows** the history of changes made to the project.    |


## Popular GitHub Commands

Here are the most common commands you'll use with GitHub, along with what they do:

### 1. `git init`
- **What it does**: Initializes a new Git repository in your project folder.
- **When to use it**: When starting a new project.
```
git init
```

### 2. `git clone [url]`
- **What it does**: Copies (or "clones") a project from GitHub to your computer.
- **When to use it**: When you want to download someone else’s project or continue working on your own project on another computer.
```
git clone https://github.com/username/repo-name.git
```

### 3. `git status`
- **What it does**: Shows the status of your files — which files have been changed, added, or are ready to be committed.
- **When to use it**: Anytime you want to see what's going on with your files.
```
git status
```

### 4. `git add [file-name]`
- **What it does**: Stages changes to be committed (saved) to Git. You can also add all files at once by using `git add .`.
- **When to use it**: After modifying a file and before committing it.
```
git add myfile.txt
# or to add all files:
git add .
```

### 5. `git commit -m "message"`
- **What it does**: Saves a snapshot of your project with a message explaining the changes.
- **When to use it**: After you've added your files with `git add` and you're ready to save your changes.
```
git commit -m "Added a new feature"
```

### 6. `git push`
- **What it does**: Uploads (pushes) your changes to GitHub so others can see or download them.
- **When to use it**: After you've committed changes and want to send them to the GitHub website.
```
git push
```

### 7. `git pull`
- **What it does**: Downloads (pulls) the latest changes from GitHub to your computer.
- **When to use it**: When someone else has made changes to the project and you want to update your local copy.
```
git pull
```

### 8. `git branch`
- **What it does**: Lists all the branches in your project and highlights the current one.
- **When to use it**: To see or create different branches for working on new features.
```
git branch
```

### 9. `git checkout -b [branch-name]`
- **What it does**: Creates a new branch and switches to it.
- **When to use it**: When you want to start working on a new feature without affecting the main project.
```
git checkout -b new-feature
```

### 10. `git merge [branch-name]`
- **What it does**: Merges the changes from one branch into another.
- **When to use it**: When you're ready to combine your changes (from a feature branch) back into the main project.
```
git merge new-feature
```

## Summary

- `git init`: Start a new Git project.
- `git clone`: Copy a project from GitHub.
- `git status`: Check the status of your files.
- `git add`: Stage files for a commit.
- `git commit -m`: Save your changes with a message.
- `git push`: Upload changes to GitHub.
- `git pull`: Download changes from GitHub.
- `git branch`: Manage project branches.
- `git checkout -b`: Create and switch to a new branch.
- `git merge`: Combine changes from one branch into another.

## Final Note:
GitHub makes working on code easier, even with large teams, by keeping everything organized and allowing everyone to contribute to the same project.
