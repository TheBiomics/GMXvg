from setuptools import setup, find_packages

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='GMXvg',
    version='0.4.4',
    packages=find_packages(),
    description='Plots GROMACS .xvg files.',
    author='Vishal K Sahu',
    author_email='mail@vishalkumarsahu.in',
    url='https://github.com/thebiomics/GMXvg',
    install_requires=REQUIREMENTS,
    entry_points = {
        'console_scripts': ['gmxvg=gmxvg.GMXVGHelper:main'],
    }
)
