import setuptools

with open("README.MD", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="api_commons",  # Replace with your own username
    version="0.0.1",
    author="Till Schulte",
    author_email="till@s.chulte.de",
    description="Gathered Api Commons",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tooxo/api_commons",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
