import setuptools

setuptools.setup(
    name='Nexa_Deep_Research_Agent',
    version='0.1.0',
    packages=setuptools.find_packages(include=['api', 'cli', 'core', 'schemas', 'services']),
    install_requires=[
        # your requirements here
    ],
)