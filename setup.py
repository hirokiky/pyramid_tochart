import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_fanstatic',
    'js.highcharts',
    'zope.component',
    ]

setup(name='pyramid_tochart',
      version='0.0',
      description='sakila',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pyramid",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        ],
      author='Hiroki KIYOHARA',
      author_email='hirokiky@gmail.com',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      dependency_links=['git+git://github.com/HireIQ/highcharts-python.git@b626dbdf9084c71dbb1cec27a88058cd1a64a1be']
)
