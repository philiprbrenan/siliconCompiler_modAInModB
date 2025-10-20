import sys, subprocess
from pathlib import Path

def script_to_rst(script_path, rst_path):
    """
    Convert a Python script to a Sphinx-friendly .rst file.
    - Lines starting with # -> reStructuredText (trimmed, except first-line shebang)
    - All other lines -> Python code blocks
    """
    script_path = Path(script_path)

    with script_path.open('r') as f:
        lines = f.readlines()
    lines.pop(0)                                                                # Remove shebang

    rst_lines = []
    code_block = []

    def flush_code():
        """Flush accumulated code lines as a code block."""
        if code_block:
            rst_lines.append(".. code-block:: python\n")
            for cl in code_block:
                rst_lines.append("    " + cl.rstrip())
            rst_lines.append("")  # blank line after code block
            code_block.clear()

    for i, line in enumerate(lines):
        stripped = line.lstrip()

        if stripped.startswith("#"):
            flush_code()
            rst_lines.append(stripped[2:].rstrip())
        elif stripped.strip() == "":
            # preserve blank lines inside code block
            code_block.append(line)
        else:
            code_block.append(line)

    flush_code()  # flush any remaining code at the end

    # write output rst
    with open(rst_path, 'w') as f:
        f.write("\n".join(rst_lines))

    print(f"Converted {script_path} â {rst_path}")

script_to_rst("top.py", "doc/source/modAInModB.rst")

result = subprocess.run(["make", "html"], cwd="doc", capture_output=True, text=True)

print(result.stdout)
print(result.stderr)
