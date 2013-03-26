from setuptools import setup

setup(
    name='tx_elevators',
    version='0.1.0-dev',
    author='The Texas Tribune',
    author_email='tech@texastribune.org',
    url='https://github.com/texastribune/tx_elevators',
    packages=['tx_elevators'],
    include_package_data=True,  # automatically include things from MANIFEST.in
    license='Apache License, Version 2.0',
    description='',
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
    ],
)
