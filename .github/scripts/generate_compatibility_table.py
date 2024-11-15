import os
import requests
from datetime import datetime

# GitHub repository information
GITHUB_REPO = os.getenv("GITHUB_REPOSITORY")  # e.g., "YourUsername/YourRepo"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Headers for authentication
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# URL for listing workflow runs
api_url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/ci.yml/runs"

# Function to get workflow runs for a specific Python version
def get_latest_run_status(python_version):
    params = {
        "event": "push",
        "branch": "main",
        "per_page": 10
    }
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()  # Raise error if the API call fails
    runs = response.json()["workflow_runs"]

    # Find the latest run with the specified Python version
    for run in runs:
        # Check if the Python version is in the run's matrix
        for job in run.get("jobs", []):
            if job.get("name") == f"build-and-test ({python_version})":
                conclusion = job.get("conclusion")
                if conclusion == "success":
                    return "✅ Supported"
                elif conclusion == "failure":
                    return "❌ Unsupported"
    return "⚠️ Not tested"  # If no relevant job is found

# Define Python versions to check
python_versions = ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]

# Generate the compatibility table
table_lines = ["| Python Version | Compatibility | Last Tested        |"]
table_lines.append("|----------------|---------------|--------------------|")

for version in python_versions:
    status = get_latest_run_status(version)
    last_tested = datetime.now().strftime("%B %Y")
    table_lines.append(f"| {version}            | {status}       | {last_tested}     |")

# Output to a file that the workflow will read
with open(".github/scripts/compatibility_table.md", "w") as f:
    f.write("\n".join(table_lines))

