from setuptools import setup
import schemar

requirements = [
    'pyparsing>=2.0.0',
]

setup(name='Schemar',
      version=schemar.__version__,
      description='CLI tool for quickly generating SQL Schemas',
      author='Ainsley Escorce-Jones',
      author_email='me@ains.co',
      url='https://www.github.com/Ainsleh/Schemar',
      packages=['schemar', 'schemar.generators'],
      entry_points={
          'console_scripts': [
              'schemar = schemar.__main__:main',
          ],
      },
)