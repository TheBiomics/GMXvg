from setuptools import setup, find_packages
REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]
setup(
    name='GMXvg',
    version='0.4',
    packages=find_packages(),
    description='Plot GROMACS .xvg files',
    author='Vishal K Sahu',
    author_email='contact@thebiomics.com',
    url='https://www.vishalkumarsahu.in/gmxvg',
    install_requires=REQUIREMENTS,
    entry_points = {
        'console_scripts': ['gmxvg=gmxvg.GMXVGHelper:main'],
    }
)
