from setuptools import setup, find_packages

setup(
    name='hemerton',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hemerton=cli.hemerton:hemerton
    ''',
)