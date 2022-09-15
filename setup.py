from setuptools import setup, find_packages
from codecs import open
from os import path
HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cprofile-middleware",
    version="0.1.5",
    description="Profile library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jijun/fastapi-cprofile",
    author="Gabriel Melo",
    author_email="gabriel.melo@bureauworks.com",
    license="MIT",
    classifiers=["cprofile", "fastapi", "middleware"],
    packages=["cProfileMiddleware"],
    include_package_data=True,
    install_requires=["fastapi"]
)