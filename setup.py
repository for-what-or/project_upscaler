from setuptools import setup, find_packages

setup(
    name="project_upscaler",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)