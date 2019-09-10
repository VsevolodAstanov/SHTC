from setuptools import setup

setup(
    name='tagcounter',
    version='1.0',
    url='https://github.com/VsevolodAstanov/SHTC.git',
    author='Vsevolod Astanov',
    packages=['tagcounter'],
    description='Simple HTML Tag Counter provide an ability to count HTML Tags by specified URL',
    package_data={'': ['*.yml']},
    entry_points={
        'console_scripts': ['tagcounter = tagcounter.__main__:main']
    },
    install_requires=['PyYAML', 'tabulate']
)