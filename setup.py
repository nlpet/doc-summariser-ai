from setuptools import setup, find_packages

setup(
    name="api",
    version="0.1.0",
    description="API for summarising text documents",
    author="Nora Petrova",
    packages=find_packages(where="api"),
    package_dir={"": "api"},
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0.post1",
        "python-multipart>=0.0.6",
        "python-dotenv>=1.0.1",
        "langchain>=0.1.4",
        "langchain-openai>=0.0.5",
        "tiktoken>=0.5.2",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
)
