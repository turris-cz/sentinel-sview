#!/usr/bin/env python3

from setuptools import setup, find_packages

VERSION = "1.3.1"


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
        "Flask==2.2.2",
        "Flask-Babel==2.0.0",
        "Flask-Caching==2.0.1",
        "Flask-Mail==0.9.1",
        "Flask-Migrate==3.1.0",
        "Flask-Redis==0.4.0",
        "Flask-RQ2==18.3",
        "Flask-Breadcrumbs==0.5.1",
        "psycopg2-binary==2.9.3",
        "Flask-SQLAlchemy==2.5.1",
        "pycountry",
        "python-dotenv",
        "simplejson",
        "geoip2",
        "sn@git+https://gitlab.nic.cz/turris/sentinel/sn@v0.3.1#egg=sn",
        "websockets",
        "jsonschema",
        "SQLAlchemy==1.4.41"
    ],
    extras_require={
        "tests": ["pytest", "coverage", "pytest-cov", "flake8", "black"],
    },
    zip_safe=False,
    include_package_data=True,
)
