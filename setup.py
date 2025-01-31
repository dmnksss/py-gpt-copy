from setuptools import setup, find_packages

setup(
    name='py-gpt-copy',
    version='1.0.0',
    author='Dmitry Gulak',
    author_email='dmitry.gulak.on@gmail.com',
    description='Copies all imported project files recursively and places them on the clipboard.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dmnksss/py-recursive-context-for-gpt',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyperclip>=1.8.2',
    ],
    entry_points={
        'console_scripts': [
            'copy-module=copy_module.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)