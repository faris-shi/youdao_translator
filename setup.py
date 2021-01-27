from setuptools import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

requirements = [
    'pyquery >= 1.4.3',
    'click >= 4.1',
    'prettytable >= 2.0.0',
    'requests >= 2.4'
]

setup(
    name = "youdao-translator-cli",
    version = '0.1',
    packages = find_packages(),
    description = 'simple approach to translate English to Chinese by youdao-translator-cli',
    author = 'Faris Shi',
    author_email = 'faris.shi84@gmail.com',
    url = 'https://github.com/faris-shi/youdao_translator',
    license = 'MIT',
    include_package_data=True,
    install_requires=requirements,
)