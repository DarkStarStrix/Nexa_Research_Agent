from setuptools import setup, find_packages

setup(
    name="Nexa_Research_Agent",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "redis",
        "psycopg2-binary",
        "sentence-transformers",
        "requests",
        # ...other dependencies...
    ],
    entry_points={
        "console_scripts": [
            "nexa-run=api.routes:main"  # if a main function exists
        ]
    }
)

