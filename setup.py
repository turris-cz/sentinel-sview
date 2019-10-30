#!/usr/bin/env python3

from setuptools import setup

setup(name="sview",
      version="0.0",
      description="Turris:Sentinel - visualization app for Sentinel data",
      author="CZ.NIC, z.s.p.o.",
      author_email="admin@turris.cz",
      url="https://gitlab.labs.nic.cz/turris/sentinel/sview",
      packages=[
          "sview",
          "sview.queries",
          "sview.queries.sql",
      ],
      install_requires=[
          "Flask",
          "Flask-Babel",
          "Flask-Caching",
          "Flask-Mail",
          "Flask-Migrate",
          "Flask-SQLAlchemy",
          "Flask-Redis",
          "Flask-RQ2",
          "psycopg2-binary",
          "pycountry",
          "python-dotenv",
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
