from setuptools import find_packages, setup

setup(
    name="lessons_dagster",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "lessons_dagster": [
            "dbt-project/**/*",
        ],
    },
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-bigquery<1.9",
        "dbt-bigquery<1.9",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)