import os
from setuptools import setup, find_packages


setup(
    name="inbox-sync",
    version="1.0",  # Release Feb 11, 2021
    packages=find_packages(),

    install_requires=[],

    include_package_data=False,


    # See:
    # https://pythonhosted.org/setuptools/setuptools.html#dynamic-discovery-of-services-and-plugins
    # https://pythonhosted.org/setuptools/pkg_resources.html#entry-points
    zip_safe=False,
    author="Tristan",
    author_email="tristanlp.alfred@gmail.com",
    description="On test la livraison Debian",
    keywords="debian",
)
