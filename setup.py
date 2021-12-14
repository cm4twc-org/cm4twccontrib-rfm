from setuptools import setup, find_namespace_packages
import json


pkg_name = 'RFM'

with open("README.rst", 'r') as fh:
    long_desc = fh.read()

with open("unifhycontrib/{}/version.py".format(pkg_name.lower()), 'r') as fv:
    exec(fv.read())


def read_authors(filename):
    authors = []
    with open(filename, 'r') as fz:
        meta = json.load(fz)
        for author in meta['creators']:
            name = author['name'].strip()
            authors.append(name)

    return ', '.join(authors)


setup(
    name='unifhycontrib-{}'.format(pkg_name.lower()),

    version=__version__,

    description='unifhy components for the {} model'.format(pkg_name),
    long_description=long_desc,
    long_description_content_type="text/x-rst",

    author=read_authors('.zenodo.json'),

    project_urls={
        'Source Code':
            'https://github.com/unifhy-org/unifhycontrib-{}'.format(pkg_name.lower())
    },

    license='UK Open Government',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Hydrology',
    ],

    packages=find_namespace_packages(include=['unifhycontrib.*']),

    namespace_packages=['unifhycontrib'],

    install_requires=[
        'unifhy==0.1.0'
    ],

    zip_safe=False
)
