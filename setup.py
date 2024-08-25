from setuptools import setup, find_packages
from pkg_resources import parse_requirements

# Parse requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = list(parse_requirements(f))

# Extraindo as strings de dependências
install_requires = [str(req) for req in requirements]


setup(
    name="ClassUtils-LLM",
    version="0.1.0",
    packages=find_packages(),
    install_requires=install_requires,
    author="Miguel Prates",
    author_email="miguelprates.ferreira@gmail.com",
    description="Biblioteca para análise de risco usando LLM",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/mpferreira003/RCL",
    license='LICENSE.txt',
)
