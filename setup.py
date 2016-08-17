from setuptools import setup

setup(
    name="http_server",
    description="A Python implementation of a http server as an echo server",
    version=0.1,
    author="David Smith, Victor Benavente",
    author_email="dbsmith.dbs83@gmail.com, vbenavente@hotmail.com",
    license="MIT",
    py_modules=["server", "client"],
    package_dir={"": "src"},
    install_requires=[],
    extras_requires={"test": ["pytest", "pytest-watch", "pytest-cov", "tox"]},
    entry_points={
        "console_scripts": [
            "server = server:main", "client = client:main"
        ]
    }
)
