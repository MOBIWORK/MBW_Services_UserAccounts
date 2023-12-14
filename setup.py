from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in mbw_account_service/__init__.py
from mbw_account_service import __version__ as version

setup(
	name="mbw_account_service",
	version=version,
	description="api mbw account",
	author="MBW",
	author_email="dev@mbw.vn",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
