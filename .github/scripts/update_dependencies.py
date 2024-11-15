import re
import ast

# Read and parse the dependencies from setup.py
def get_install_requires():
    with open("setup.py", "r") as f:
        setup_contents = f.read()

    # Parse setup.py to extract install_requires
    tree = ast.parse(setup_contents)
    install_requires = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and node.targets[0].id == "install_requires":
            install_requires = [elt.s for elt in node.value.elts]
    return install_requires

# Generate dependencies as a Markdown list
dependencies = get_install_requires()
dependencies_md = "\n".join(f"- `{dep}`" for dep in dependencies)

# Insert dependencies into README
with open("README.md", "r") as f:
    readme_contents = f.read()

# Replace the dependencies section in README
updated_readme = re.sub(
    r"<!--DEPENDENCIES_START-->(.*?)<!--DEPENDENCIES_END-->",
    f"<!--DEPENDENCIES_START-->\n{dependencies_md}\n<!--DEPENDENCIES_END-->",
    readme_contents,
    flags=re.DOTALL,
)

with open("README.md", "w") as f:
    f.write(updated_readme)

print("Dependencies updated in README.md")
