from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django-authtkt',
      version=version,
      description="django-authtkt project",
      long_description="""\
""",
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Framework :: Django',
          'Intended Audience :: Developers',
      ],
      keywords='django',
      author='',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'test_project']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Paste',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [django.pluggable_app]
      authtkt = authtkt:pluggableapp
      """,
      )
