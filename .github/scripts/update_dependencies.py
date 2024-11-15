import re

# Function to directly extract `install_requires` by regex
# Function to directly extract `install_requires` by regex
def get_install_requires():
    with open("setup.py", "r") as f:
        setup_contents = f.read()

    # Regex to match the entire install_requires list as one block
    match = re.search(r"install_requires=\[(.*?)\]", setup_contents, re.DOTALL)
    if not match:
        print("Warning: Could not find install_requires in setup.py")
        return []

    # Split dependencies while keeping versions together
    deps = match.group(1)
    dependencies = re.findall(r"['\"]([^'\"]+)['\"]", deps)  # Extract items between quotes
    return dependencies

# Generate dependencies as a Markdown list
dependencies = get_install_requires()
dependencies_md = "\n".join(f"- `{dep}`" for dep in dependencies)

# Insert dependencies into README
with open("README.md", "r") as f:
    readme_contents = f.read()
print("Original README contents:\n", readme_contents)  # Debug statement

# Replace the dependencies section in README
updated_readme = re.sub(
    r"<!--DEPENDENCIES_START-->(.*?)<!--DEPENDENCIES_END-->",
    f"<!--DEPENDENCIES_START-->\n{dependencies_md}\n<!--DEPENDENCIES_END-->",
    readme_contents,
    flags=re.DOTALL,
)

print("Updated README contents:\n", updated_readme)  # Debug statement

# Write the updated content to README.md
with open("README.md", "w") as f:
    f.write(updated_readme)

print("Dependencies updated in README.md")
