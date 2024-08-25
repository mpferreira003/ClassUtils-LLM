from setuptools import setup, find_packages

setup(
    name="ClassUtilsLLM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "openai",
        "sentence-transformers",
        "tensorflow",
        "matplotlib",
        "scikit-learn"
    ],
    author="Miguel Prates",
    author_email="miguelprates.ferreira@gmail.com",
    description="Library for analysis with Large Language Models",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/mpferreira003/ClassUtilsLLM",
    license='LICENSE.txt',
)
