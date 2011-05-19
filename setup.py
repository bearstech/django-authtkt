from setuptools import setup, find_packages
import sys, os

version = '0.3'

setup(name='django-authtkt',
      version=version,
      description="django-authtkt is used to share auth between more than one django site (a kind of SSO auth)",
      long_description=open('README.txt').read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          'Framework :: Django',
          'Intended Audience :: Developers',
      ],
      keywords='django auth cookie',
      author='Bearstech',
      author_email='py@beasrtech.com',
      url='https://github.com/bearstech/django-authtkt',
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
