# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

from setuptools import setup, Command
from shutil import rmtree
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))


class UploadCommand(Command):
    """
    Copied from https://github.com/kennethreitz/setup.py/blob/master/setup.py
    """

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            print('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        print('Building Source and Wheel (universal) distribution...')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        print('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='memorize.py',
    packages=['memorize'],
    version='1.2',
    description='Simple decorator for memoizing a function across multiple program executions.',
    author='Ben Scheiner',
    url='https://github.com/brmscheiner/memorize.py',
    keywords='memorize memoize pickle',
    cmdclass={
        'upload': UploadCommand,
    },
)
