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
      ],
      install_requires=[
          "Flask",
      ],
      extras_require={
          "tests": [
              "pytest",
              "coverage",
              "pytest-cov",
              "flake8",
          ],
          "dev": [
              "python-dotenv",
          ],
      }
      )
