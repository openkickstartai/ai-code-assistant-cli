import os
import subprocess
from pathlib import Path
from typing import Optional


def read_file(file_path: str) -> str:
    """Read file contents safely."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading file {file_path}: {e}")


def get_git_diff(staged_only: bool = False) -> str:
    """Get git diff for current repository."""
    try:
        if staged_only:
            result = subprocess.run(
                ["git", "diff", "--cached"],
                capture_output=True,
                text=True,
                check=True
            )
        else:
            result = subprocess.run(
                ["git", "diff", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
        return result.stdout
    except subprocess.CalledProcessError:
        return "No git repository or no changes detected."


def is_python_file(file_path: str) -> bool:
    """Check if file is a Python file."""
    return file_path.endswith(".py")


def get_function_name_from_line(code: str, line_number: int) -> Optional[str]:
    """Extract function name from a specific line of code."""
    lines = code.split("\n")
    if 0 <= line_number < len(lines):
        line = lines[line_number].strip()
        if line.startswith("def "):
            return line.split("def ")[1].split("(")[0].strip()
        elif line.startswith("class "):
            return line.split("class ")[1].split("(")[0].split(":")[0].strip()
    return None