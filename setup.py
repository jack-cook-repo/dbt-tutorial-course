from setuptools import find_packages, setup

setup(
    name="lessons_dagster",
    packages=find_packages(exclude=["lessons_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-core==1.8.9",
        "dbt-bigquery==1.8.3",
    ],
    extras_require={
        "dev": [
            "dagster-webserver",
        ]
    },
)