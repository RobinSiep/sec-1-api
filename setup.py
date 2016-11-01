import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'bcrypt',
    'bleach',
    'packaging',
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'pyramid_redis_sessions',
    'pyramid_tm',
    'psycopg2',
    'redis',
    'requests',
    'SQLAlchemy',
    'sqlalchemy_utils',
    'zope.sqlalchemy',
    'transaction',
    'marshmallow',
    'waitress',
    'sendgrid',
    'webtest'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
]

setup(name='sec-1-api',
      version='0.0',
      description='sec-1-api',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='sec_1_api',
      test_requires=tests_require,
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = sec_1_api:main
      [console_scripts]
      initialize_sec-1-api_db = sec_1_api.scripts.initializedb:main
      """,
      )
