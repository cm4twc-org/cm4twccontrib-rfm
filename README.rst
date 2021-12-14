A unifhy-compliant version of the River Flow Model (RFM)
--------------------------------------------------------

.. image:: https://img.shields.io/pypi/v/unifhycontrib-rfm?style=flat-square&color=00b0f0
   :target: https://pypi.python.org/pypi/unifhycontrib-rfm
   :alt: PyPI Version
.. image:: https://img.shields.io/badge/dynamic/json?url=https://zenodo.org/api/records/5780053&label=doi&query=doi&style=flat-square&color=00b0f0
   :target: https://zenodo.org/badge/latestdoi/365264235
   :alt: DOI

River Flow Model (RFM) is a runoff routing model based on a discrete
approximation of the one-directional kinematic wave with lateral
inflow (`Bell et al., 2007 <https://doi.org/10.5194/hess-11-532-2007>`_,
`Dadson et al., 2011 <https://doi.org/10.1016/j.jhydrol.2011.10.002>`_).

The wave equation is parametrised differently for surface and
sub-surface pathways, themselves split into a land domain, and a
river domain. Return flow is also possible between surface and
sub-surface pathways in each domain.

This Python implementation of RFM is based on the work by Huw Lewis.

:contributors: Huw Lewis [1], Thibault Hallouin [2]
:affiliations:
    1. UK Met Office
    2. Department of Meteorology, University of Reading
:licence: UK Open Government
:copyright: 2020, UK Met Office
