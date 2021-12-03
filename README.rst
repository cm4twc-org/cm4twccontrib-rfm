A unifhy-compliant version of the River Flow Model (RFM)
--------------------------------------------------------

River Flow Model (RFM) is a runoff routing model based on a discrete
approximation of the one-directional kinematic wave with lateral
inflow (`Bell et al., 2007 <https://doi.org/10.5194/hess-11-532-2007>`_,
`Dadson et al., 2011 <https://doi.org/10.1016/j.jhydrol.2011.10.002>`_).

The wave equation is parametrised differently for surface and
sub-surface pathways, themselves split into a land domain, and a
river domain. Return flow is also possible between surface and
sub-surface pathways in each domain.

This Python implementation of RFM is based on the work by Huw Lewis.

:contributors: Huw Lewis [1]
:affiliations:
    1. UK Met Office
:licence: UK Open Government
:copyright: 2020, UK Met Office
