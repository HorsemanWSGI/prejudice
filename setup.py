import os
from setuptools import setup, Extension, find_packages

version = "0.1"

install_requires = [
]

test_requires = [
    'pytest',
]


setup(
    name='prejudice',
    version=version,
    author='Souheil CHELFOUH',
    author_email='trollfot@gmail.com',
    url='https://github.com/HorsemanWSGI/prejudice',
    download_url='http://pypi.python.org/pypi/prejudice',
    description='Python/Cython predicate/guard/validation system.',
    long_description=(open("README.rst").read() + "\n" +
                      open(os.path.join("docs", "HISTORY.rst")).read()),
    license='ZPL',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    ext_modules=[
        Extension(
            "prejudice.errors",
            ["src/prejudice/errors.c"],
            extra_compile_args=["-O3"],  # Max optimization when compiling.
        ),
        Extension(
            "prejudice.utils",
            ["src/prejudice/utils.c"],
            extra_compile_args=["-O3"],  # Max optimization when compiling.
        ),
    ],
    install_requires=install_requires,
    extras_require={
        'test': test_requires,
    },
)
