from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pypermacc',
    version='0.1.1',
    description='Python wrapper around the perma.cc API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Te-k/pypermacc',
    author='Tek',
    author_email='tek@randhome.io',
    keywords='archive',
    install_requires=['requests'],
    license='MIT',
    python_requires='>=3.5',
    packages=['pypermacc'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)
