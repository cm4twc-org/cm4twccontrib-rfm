import numpy as np
import warnings

import unifhy


class OpenWaterComponent(unifhy.component.OpenWaterComponent):
    """River flow model (RFM) is a runoff routing model based on a discrete
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
    """
    _inwards = {
        'surface_runoff_flux_delivered_to_rivers',
        'net_groundwater_flux_to_rivers'
    }
    _outwards = {}
    _inputs_info = {
        'flow_accumulation': {
            'units': '1',
            'kind': 'static',
            'description': 'drainage area (specified in number of '
                           'cells) draining to a grid box'
        }
    }
    _parameters_info = {
        'c_land': {
            'units': 'm s-1',
            'description': 'kinematic wave speed for surface flow in '
                           'a land grid box on the river routing grid'
        },
        'cb_land': {
            'units': 'm s-1',
            'description': 'kinematic wave speed for subsurface flow in '
                           'a land grid box on the river routing grid'
        },
        'c_river': {
            'units': 'm s-1',
            'description': 'kinematic wave speed for surface flow in '
                           'a river grid box on the river routing grid'
        },
        'cb_river': {
            'units': 'm s-1',
            'description': 'kinematic wave speed for subsurface flow in '
                           'a river grid box on the river routing grid'
        },
        'ret_l': {
            'units': '1',
            'description': 'land return flow fraction '
                           '(resolution dependent)'
        },
        'ret_r': {
            'units': '1',
            'description': 'river return flow fraction '
                           '(resolution dependent)'
        },
        'routing_length': {
            'units': 'm',
            'description': 'length of the routing path'
        }
    }
    _states_info = {
        'flow_in': {
            'units': 'm3',
            'description': 'surface flow from neighbouring cells'
        },
        'b_flow_in': {
            'units': 'm3',
            'description': 'sub-surface flow from neighbouring cells'
        },
        'surf_store': {
            'units': 'm3',
            'description': 'surface water store'
        },
        'sub_store': {
            'units': 'm3',
            'description': 'sub-surface water store'
        }
    }
    _constants_info = {
        'a_thresh': {
            'units': '1',
            'description': 'threshold drainage area (specified in number of '
                           'cells) draining to a grid box, above which the '
                           'grid cell is considered to be a river point - '
                           'remaining points are treated as land (drainage '
                           'area = 0) or sea (drainage area < 0)',
            'default_value': 13
        },
        'rho_lw': {
            'description': 'specific mass of liquid water',
            'units': 'kg m-3',
            'default_value': 1e3
        }
    }
    _outputs_info = {
        'outgoing_water_volume_transport_along_river_channel': {
            'units': 'm3 s-1',
            'description': 'streamflow at outlet of grid element'
        }
    }
    _requires_flow_direction = True
    _requires_cell_area = True

    def initialise(
            self,
            # component inputs
            flow_accumulation,
            # component parameters
            c_land, cb_land, c_river, cb_river, ret_l, ret_r, routing_length,
            # component states
            flow_in, b_flow_in, surf_store, sub_store,
            # component constants
            a_thresh,
            **kwargs
    ):

        # /!\__RENAMING_CM4TWC__________________________________________
        dt = self.timedelta_in_seconds
        shape = self.spaceshape

        dx = routing_length
        i_area = flow_accumulation
        # ______________________________________________________________

        if not self.initialised_states:
            # set initialise conditions for component states
            flow_in.set_timestep(-1, 0.)
            b_flow_in.set_timestep(-1, 0.)
            surf_store.set_timestep(-1, 0.)
            sub_store.set_timestep(-1, 0.)

        # Set theta values
        r_theta = c_river * dt / dx
        if np.any(r_theta < 0) or np.any(r_theta > 1):
            warnings.warn(
                "theta river surface not within [0, 1]", RuntimeWarning
            )
        sub_r_theta = cb_river * dt / dx
        if np.any(sub_r_theta < 0) or np.any(sub_r_theta > 1):
            warnings.warn(
                "theta river subsurface not within [0, 1]", RuntimeWarning
            )
        l_theta = c_land * dt / dx
        if np.any(l_theta < 0) or np.any(l_theta > 1):
            warnings.warn(
                "theta land surface not within [0, 1]", RuntimeWarning
            )
        sub_l_theta = cb_land * dt / dx
        if np.any(sub_l_theta < 0) or np.any(sub_l_theta > 1):
            warnings.warn(
                "theta land subsurface not within [0, 1]", RuntimeWarning
            )

        # define sea/land/river points
        sea = np.where(i_area < 0)
        land = np.where((i_area < a_thresh) & (i_area >= 0))
        riv = np.where(i_area >= a_thresh)

        # initialise mapped variables
        theta = np.zeros(shape)
        s_theta = np.zeros(shape)
        ret_flow = np.zeros(shape)
        theta[land] = l_theta[land]
        theta[riv] = r_theta[riv]
        s_theta[land] = sub_l_theta[land]
        s_theta[riv] = sub_r_theta[riv]
        ret_flow[land] = ret_l[land]
        ret_flow[riv] = ret_r[riv]
        mask = np.ones(shape)
        mask[sea] = 0

        # store pre-processed information on shelf
        self.shelf.update(
            {
                'theta': theta,
                's_theta': s_theta,
                'ret_flow': ret_flow,
                'mask': mask
            }
        )

    def run(
            self,
            # from exchanger
            surface_runoff_flux_delivered_to_rivers,
            net_groundwater_flux_to_rivers,
            # component states
            flow_in, b_flow_in, surf_store, sub_store,
            # component constants
            rho_lw,
            **kwargs
    ):

        # /!\__RENAMING_CM4TWC__________________________________________
        dt = self.timedelta_in_seconds
        area = self.spacedomain.cell_area

        surf_in = surface_runoff_flux_delivered_to_rivers
        sub_in = net_groundwater_flux_to_rivers
        # ______________________________________________________________

        # shorten API for states by creating tuples of views
        flow_in = (flow_in.get_timestep(0), flow_in.get_timestep(-1))
        b_flow_in = (b_flow_in.get_timestep(0), b_flow_in.get_timestep(-1))
        surf_store = (surf_store.get_timestep(0), surf_store.get_timestep(-1))
        sub_store = (sub_store.get_timestep(0), sub_store.get_timestep(-1))

        # retrieve pre-processed information from shelf
        theta = self.shelf['theta']
        s_theta = self.shelf['s_theta']
        ret_flow = self.shelf['ret_flow']
        mask = self.shelf['mask']

        # convert units for input runoffs
        surf_runoff = mask * surf_in * dt * area / rho_lw
        sub_surf_runoff = mask * sub_in * dt * area / rho_lw

        # compute stores
        surf_store_n = (1.0 - theta) * surf_store[-1] + flow_in[-1] + surf_runoff
        sub_store_n = (1.0 - s_theta) * sub_store[-1] + b_flow_in[-1] + sub_surf_runoff

        # return flow between surface and subsurface
        return_flow = np.maximum(sub_store_n * ret_flow, 0.0)
        surf_store[0][:] = surf_store_n + return_flow
        sub_store[0][:] = sub_store_n - return_flow

        # move water between adjacent grid points
        flow_in[0][:], outed = self.spacedomain.route(theta * surf_store[-1])
        b_flow_in[0][:], b_outed = self.spacedomain.route(s_theta * sub_store[-1])

        # compute river flow output
        riv_flow = theta / dt * surf_store[-1]

        return (
            # to exchanger
            {},
            # component outputs
            {
                'outgoing_water_volume_transport_along_river_channel':
                    riv_flow
            }
        )

    def finalise(
            self,
            **kwargs
    ):
        pass
