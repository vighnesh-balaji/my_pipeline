from setuptools import setup, find_packages

setup(
    name='my_pipeline',  
    version='0.1.0',  
    author='Vighnesh',  
    author_email='vighneshsrinivasabalaji@gmail.com', 
    description='Test cases for pipeline function testing suite', 
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Set the README content type
    url='https://github.com/vighnesh-balaji/my_pipeline', 
    packages=find_packages(),
    install_requires=[
        'numpy', 
        'pandas',
        'scipy',
        'json',
        'pytest'
    ],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License', 
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',  
)
