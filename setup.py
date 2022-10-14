import os
from setuptools import setup

# bigqueryorm
# A BigQuery ORM


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="bigqueryorm",
    version="0.0.1",
    description="A BigQuery ORM",
    author="__xor__",
    author_email="dunder.xor.dunder@gmail.com",
    license="GPLv3",
    keywords="bigquery orm",
    url="https://github.com/dunder-xor-dunder/bigqueryorm",
    packages=['bigqueryorm'],
    package_dir={'bigqueryorm': 'bigqueryorm'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'bigqueryorm=bigqueryorm:main',
        ],
    },
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    # package_data={
    #     'bigqueryorm': ['templates/*.html'],
    # },
    # include_package_data=True,
)
