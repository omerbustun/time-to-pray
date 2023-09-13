from setuptools import setup, find_packages

setup(
    name='time-to-pray',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'PyQt6==6.5.2',
        'PyQt6_sip==13.5.2',
        'Requests==2.31.0'
    ],
    entry_points={
        'console_scripts': [
            'time-to-pray=src.main:main',
        ],
    },
    author='Ömer Üstün',
    author_email='omerbustun@gmail.com',
    description='A desktop utility for Islamic prayer times',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/omerbustun/time-to-pray',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
