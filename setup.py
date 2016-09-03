from setuptools import setup, find_packages

from django_learnit import __version__


requires = [
    'Django>=1.7'
]

setup(
    name='django-learnit',
    version=__version__,
    author='Florian PAQUET',
    license='MIT',
    packages=find_packages(),
    install_requires=requires,
    tests_require=requires + ['factory_boy'],
    test_suite='runtests.runtests'
)
