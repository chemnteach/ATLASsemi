"""
ATLASsemi setup script.
"""

from setuptools import setup, find_packages

setup(
    name="atlassemi",
    version="0.1.0",
    description="Semiconductor fab problem-solving assistant with 8D methodology",
    author="Your Name",
    author_email="your.email@company.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "python-dateutil>=2.8.2",
        "pyyaml>=6.0",
        "dataclasses-json>=0.6.0",
        "anthropic>=0.18.0",
        "openai>=1.12.0",
        "google-generativeai>=0.3.0",
        "neo4j>=5.14.0",
        "sentence-transformers>=2.2.0",
        "chromadb>=0.4.0",
        "langchain>=0.1.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "tenacity>=8.2.0",
        "structlog>=23.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "atlassemi=cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Manufacturing",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
