import setuptools


setuptools.setup(
    name="nanoloop_mobile_sample_tools",
    version="1.0.0",
    description="Nanoloop mobile sample tools",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gesceap",
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    install_requires=open("requirements.txt").read(),
    entry_points={'console_scripts': [
        'nmst=nanoloop_mobile_sample_tools.nmst:main'
    ]}
)
