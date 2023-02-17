import setuptools
from nanoloop_mobile_sample_tools import version


setuptools.setup(
    name="nanoloop_mobile_sample_tools",
    version=version.__version__,
    description="Nanoloop Mobile Sample Tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gesceap",
    author_email="gesceapmusic@gmail.com",
    url="https://github.com/gesceap/nanoloop-mobile-sample-tools",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    install_requires=open("requirements.txt").read(),
    entry_points={'console_scripts': [
        'nmst=nanoloop_mobile_sample_tools.nmst:main'
    ]}
)
