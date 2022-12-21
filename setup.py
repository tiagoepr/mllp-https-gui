### Added feature: HTTPS to MLLP
### By Tiago Rodrigues
### Sectra Iberia, Dec 2022

import setuptools

version = {}
with open("mllp_https_gui/version.py", "r") as f:
    exec(f.read(), version)

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    author="Tiago Rodrigues/SECTRA Iberia",
    author_email="Tiago.Rodrigues@sectra.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    description="GUI to install and configure mllp-https",
    entry_points={
        "console_scripts": [
            "mllp_https_gui=mllp_https_gui.main:gui",
        ]
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "mllp-https",
        "pysimplegui",
    ],
    name="mllp_https_gui",
    packages=setuptools.find_packages(),
    include_package_data=True,
    project_urls={
        "Issues": "https://github.com/tiagoepr/mllp-https/issues",
    },
    url="https://github.com/tiagoepr/mllp-https",
    version=version["__version__"],

)
