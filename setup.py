from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='hexagons',
    version='0.0.1.0',
    license='MIT License',
    author='Diorge Brognara',
    author_email='diorge.bs@gmail.com',
    packages=['hexagons'],
    description='Hexagon grids for games',
    tests_require=['pytest'],
    install_requires=['pygame>=1.9.3'],
    cmdclass={'test': PyTest},
    test_suite='hexagons.test',
    extras_require={'testing': ['pytest']}
)
