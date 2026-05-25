# setup.py
# Long Vy – Unit 10 Assignment
# Packages the Unit 9 security-enhanced GUI/database application using setuptools.
#
# References:
# Python Packaging Authority. (2023). Packaging Python projects.
#   https://packaging.python.org/en/latest/tutorials/packaging-projects/
# Python Software Foundation. (2024). setuptools documentation.
#   https://setuptools.pypa.io/en/latest/

from setuptools import setup, find_packages

setup(
    name="long_vy_unit9_app",
    version="1.0.0",
    author="Long Vy",
    description=(
        "Security-enhanced Tkinter/PostgreSQL login application "
        "with bcrypt hashing, parameterized queries, input validation, "
        "and account lockout (Unit 9 – IN450)."
    ),
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "psycopg2-binary>=2.9",   # PostgreSQL adapter
        "bcrypt>=4.0",            # Password hashing (Security Change 3)
    ],
    entry_points={
        "console_scripts": [
            # Allows running the app from the command line as: long-vy-unit9
            "long-vy-unit9=long_vy_unit9_app.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
