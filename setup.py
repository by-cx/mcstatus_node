from setuptools import setup, find_packages

setup(
    name = "mcstatus_node",
    version = "1.0",
    author = "Adam Strauch",
    author_email = "cx@initd.cz",
    description = ("Node webapp for mcstatus"),
    license = "BSD",
    keywords = "minecraft",
    url = "https://github.com/creckx/mcstatus_node",
    long_description="Node webapp for mcstatus",
    packages = find_packages(exclude=['ez_setup', 'examples', 'tests']),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
        ],
    entry_points="""
    [console_scripts]
    mcstatus_node = mcstatus_node.infoweb:main
    mcstatus_node_install = mcstatus_node.install:main
    """
)
