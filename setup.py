from setuptools import setup, find_namespace_packages


pkg_name = 'RFM'

with open("README.rst", 'r') as fh:
    long_desc = fh.read()

with open("cm4twccontrib/{}/version.py".format(pkg_name.lower()), 'r') as fv:
    exec(fv.read())


setup(
    name='cm4twccontrib-{}'.format(pkg_name.lower()),

    version=__version__,

    description='cm4twc components for the {} model'.format(pkg_name),
    long_description=long_desc,
    long_description_content_type="text/x-rst",

    author='Thibault Hallouin',

    project_urls={
        'Source Code':
            'https://github.com/cm4twc-org/cm4twccontrib-{}'.format(pkg_name.lower())
    },

    license='UK Open Government',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering :: Hydrology',
    ],

    packages=find_namespace_packages(include=['cm4twccontrib.*']),

    namespace_packages=['cm4twccontrib'],

    install_requires=[
        'cm4twc'
    ],

    zip_safe=False
)
