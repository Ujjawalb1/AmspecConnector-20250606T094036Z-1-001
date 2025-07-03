from setuptools import setup,find_packages

setup(
    name="amspec_einvoice_package",
    version="0.1.2",
    author="Moksh Baweja",
    author_email="mokshb@engineosol.com",
    description = "package for einvoices",
    packages = find_packages(where="src"),
    package_dir={"": "src"},  # Maps package location
    install_requires=[  # Dependencies from `requirements.txt`
        line.strip() for line in open("requirements.txt") if line.strip() and not line.startswith("#")
    ],
    python_requires=">=3.12",
)