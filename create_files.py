import os
import subprocess

GITIGNORE_CONTENT = """
# Node
node_modules/
package-lock.json

# Python
__pycache__/
*.pyc
*.pyo

# Environment
.env

# Logs and temp
*.log
bot_log.txt
buy_price*.txt
strategy_state.json
compound_data.json
portfolio_value.json
bot_runner_output.txt

# React build
/static
build/
dist/

# VSCode or OS files
.vscode/
.DS_Store
Thumbs.db
"""

def create_gitignore():
    path = ".gitignore"
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(GITIGNORE_CONTENT.strip())
        print("✅ Created .gitignore")
    else:
        print("ℹ️ .gitignore already exists")

def remove_ignored_files_from_git():
    files_to_untrack = [
        "node_modules",
        "__pycache__",
        "*.txt",
        "*.json",
        "*.log",
        ".env"
    ]

    for item in files_to_untrack:
        try:
            subprocess.run(["git", "rm", "-r", "--cached", item], check=True)
            print(f"🔥 Untracked {item}")
        except subprocess.CalledProcessError:
            print(f"⚠️ Could not untrack {item} (maybe not tracked)")

    subprocess.run(["git", "add", ".gitignore"])
    subprocess.run(["git", "commit", "-m", "🧹 Auto cleanup with create_files.py"])
    subprocess.run(["git", "push"])
    print("🚀 Cleanup pushed to GitHub.")

if __name__ == "__main__":
    create_gitignore()
    remove_ignored_files_from_git()
