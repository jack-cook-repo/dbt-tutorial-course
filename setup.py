from setuptools import find_packages, setup

setup(
    name="lessons_dagster",
    version="0.0.1",
    packages=find_packages(where="lessons_dagster"),
    package_data={
        "lessons_dagster": [
            "dbt-project/**/*",
        ],
    },
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