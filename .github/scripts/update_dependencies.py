import re
import ast

# Read install_requires from setup.py
with open("setup.py", "r") as f:
    setup_contents = f.read()

# Parse install_requires using AST (Abstract Syntax Tree)
tree = ast.parse(setup_contents)
install_requires = []
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and node.targets[0].id == "install_requires":
        install_requires = [elt.s for elt in node.value.elts]

# Generate dependencies as Markdown list
dependencies_list = "\n".join(f"- `{dep}`" for dep in install_requires)

# Insert dependencies into README
with open("README.md", "r") as f:
    readme_contents = f.read()

updated_readme = re.sub(
    r"<!--DEPENDENCIES_START-->(.*?)<!--DEPENDENCIES_END-->",
    f"<!--DEPENDENCIES_START-->\n{dependencies_list}\n<!--DEPENDENCIES_END-->",
    readme_contents,
    flags=re.DOTALL,
)

with open("README.md", "w") as f:
    f.write(updated_readme)
