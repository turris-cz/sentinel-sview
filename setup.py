#!/usr/bin/env python3

from setuptools import setup, find_packages

VERSION = "1.0.0"


setup(
    name="sview",
    version=VERSION,
    description="Turris:Sentinel - visualization app for Sentinel data",
    author="CZ.NIC, z.s.p.o.",
    author_email="packaging@turris.cz",
    url="https://gitlab.nic.cz/turris/sentinel/sview",
    packages=find_packages(),
    entry_points={"console_scripts": ["dynfw-backend=dynfw_backend.__main__:main"]},
    install_requires=[
        "Flask",
        "Flask-Babel",
        "Flask-Caching",
        "Flask-Mail",
        "Flask-Migrate",
        "Flask-Redis",
        "Flask-RQ2",
        "Flask-Breadcrumbs",
        "psycopg2-binary",
        "pycountry",
        "python-dotenv",
        "simplejson",
        "geoip2",
        "websockets",
    ],
    extras_require={
        "tests": [
            "pytest",
            "coverage",
            "pytest-cov",
            "flake8",
        ],
    },
    zip_safe=False,
    include_package_data=True,
)
