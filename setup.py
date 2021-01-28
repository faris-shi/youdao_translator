from setuptools import setup, find_packages


try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open("README.md", "r") as fd:
        long_description = fd.read()

requirements = [
    'pyquery',
    'click',
    'rich',
    'requests',
]

name = 'youdao-trans-cli'

setup(
    name = name,
    version = '0.3',
    packages = find_packages(),
    description = 'simple approach to translate English to Chinese by youdao-translator-cli',
    long_description = long_description,
    long_description_content_type="text/markdown",
    author = 'Faris Shi',
    author_email = 'faris.shi84@gmail.com',
    url = 'https://github.com/faris-shi/youdao_translator',
    license = 'MIT',
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        'console_scripts':[
            'youdao-trans-cli=youdao_trans:cli' 
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Utilities',

        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)