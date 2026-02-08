from setuptools import setup, find_packages

setup(
    name="ai-code-assistant-cli",
    version="0.1.0",
    description="AI-powered command-line code assistant",
    author="OpenKickstart Agent",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "openai>=1.0.0",
        "rich>=13.0.0",
        "gitpython>=3.1.0",
        "pyyaml>=6.0"
    ],
    entry_points={
        "console_scripts": [
            "ai-assist=ai_code_assistant.cli:main",
        ],
    },
    python_requires=">=3.8"
)