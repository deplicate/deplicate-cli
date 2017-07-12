# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='deplicate-cli',
    version=open('VERSION').read().strip(),
    description='Command Line Interface for deplicate.',
    long_description=open('README.rst').read(),
    keywords='duplicates dups',
    url='https://github.com/vuolter/deplicate-cli',
    download_url='https://github.com/vuolter/deplicate-cli/releases',
    author='Walter Purcaro',
    author_email='vuolter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: System',
        'Topic :: System :: Filesystems',
        'Topic :: Utilities'],
    platforms=['any'],
    py_modules=['deplicate_cli'],
    include_package_data=True,
    install_requires=['click>=4.0', 'deplicate>=0.6.2'],
    python_requires='>=2.6,!=3.0,!=3.1,!=3.2',
    zip_safe=True,
    entry_points={
        'console_scripts': ['deplicate=deplicate_cli:cli']})
