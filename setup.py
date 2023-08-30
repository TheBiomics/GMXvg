from setuptools import setup, find_packages
from gmxvg import __package__, __version__, __subversion__, __author__

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
LONG_DESCRIPTION = "".join(open("README.md").readlines())

setup(
    name=__package__,
    version=f"{__version__}.{__subversion__}",
    packages=find_packages(),
    description='Plots GROMACS .xvg files.',
    author=__author__,
    author_email='mail@vishalkumarsahu.in',
    url='https://github.com/thebiomics/GMXvg',
    install_requires=REQUIREMENTS,
    entry_points = {
        'console_scripts': ['gmxvg=gmxvg.GMXVGHelper:main'],
    },
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
)
