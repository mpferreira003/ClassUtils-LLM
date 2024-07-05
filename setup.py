from setuptools import setup, find_packages

setup(
    name="RCL",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # Lista de dependências, por exemplo:
        "numpy>=1.13.3",
        "torch>=0.4.0",
        "openai==0.28",
        "sentence-transformers"
        "tensorflow",
        "scikit-learn"
    ],
    author="Seu Nome",
    author_email="seuemail@exemplo.com",
    description="Uma biblioteca de exemplo",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/seuusuario/minha_biblioteca",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
