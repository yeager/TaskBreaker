from setuptools import setup, find_packages

setup(
    name="taskbreaker",
    version="1.0.0",
    description="Bryt ner uppgifter till mikrosteg - ADHD-anpassat verktyg",
    author="TaskBreaker",
    license="MIT",
    packages=find_packages(),
        package_data={
        "": ["locale/*/LC_MESSAGES/*.mo"],
    },
    entry_points={
        "console_scripts": [
            "taskbreaker=taskbreaker.app:main",
        ],
    },
    python_requires=">=3.10",
    install_requires=[
        "PyGObject>=3.42",
    ],
)
