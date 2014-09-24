#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Colour Rendering Index
======================

Defines *colour rendering index* computation objects:

-   :func:`CRI_Specification`
-   :func:`colour_rendering_index`

See Also
--------
`Colour Rendering Index IPython Notebook
<http://nbviewer.ipython.org/github/colour-science/colour-ipython/blob/master/notebooks/quality/cri.ipynb>`_  # noqa

References
----------
.. [1]  http://cie2.nist.gov/TC1-69/NIST%20CQS%20simulation%207.4.xls
        (Last accessed 10 June 2014)
"""

from __future__ import division, unicode_literals

import numpy as np
from collections import namedtuple

from colour.colorimetry import STANDARD_OBSERVERS_CMFS
from colour.colorimetry import (
    D_illuminant_relative_spd,
    blackbody_spd,
    spectral_to_XYZ)
from colour.quality.dataset.tcs import TCS_SPDS, TCS_INDEXES_TO_NAMES
from colour.models import UCS_to_uv, XYZ_to_UCS, XYZ_to_xyY
from colour.temperature import CCT_to_xy_illuminant_D, uv_to_CCT_robertson1968

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013 - 2014 - Colour Developers'
__license__ = 'New BSD License - http://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-science@googlegroups.com'
__status__ = 'Production'

__all__ = ['TCS_ColorimetryData',
           'colour_rendering_index']


class TCS_ColorimetryData(namedtuple('TCS_ColorimetryData',
                                     ('name', 'XYZ', 'uv', 'UVW'))):
    """
    Defines the the class holding *test colour samples* colorimetry data.
    """


class CRI_Specification(
    namedtuple(
        'CRI_Specification',
        ('Q_a', 'Q_as', 'colorimetry_data'))):
    """
    Defines the *colour rendering index* colour quality specification.

    Parameters
    ----------
    Q_a : numeric
        *Colour rendering index* :math:`Q_a`.
    Q_as : dict
        Individual *colour rendering indexes* data for each sample.
    colorimetry_data : tuple
        Colorimetry data for the test and reference computations.
    """


def colour_rendering_index(spd_test, additional_data=False):
    """
    Returns the *colour rendering index* :math:`Q_a` of given spectral power
    distribution.

    Parameters
    ----------
    spd_test : SpectralPowerDistribution
        Test spectral power distribution.
    additional_data : bool, optional
        Output additional data.

    Returns
    -------
    numeric or CRI_Specification
        Colour rendering index.

    Examples
    --------
    >>> from colour import ILLUMINANTS_RELATIVE_SPDS
    >>> spd = ILLUMINANTS_RELATIVE_SPDS.get('F2')
    >>> colour_rendering_index(spd)  # doctest: +ELLIPSIS
    64.1507331...
    """

    cmfs = STANDARD_OBSERVERS_CMFS.get('CIE 1931 2 Degree Standard Observer')

    shape = cmfs.shape
    spd_test = spd_test.clone().align(shape)

    tcs_spds = {}
    for index, tcs_spd in TCS_SPDS.items():
        tcs_spds[index] = tcs_spd.clone().align(shape)

    XYZ = spectral_to_XYZ(spd_test, cmfs)
    uv = UCS_to_uv(XYZ_to_UCS(XYZ))
    CCT, Duv = uv_to_CCT_robertson1968(uv)

    if CCT < 5000:
        spd_reference = blackbody_spd(CCT, shape)
    else:
        xy = CCT_to_xy_illuminant_D(CCT)
        spd_reference = D_illuminant_relative_spd(xy)
        spd_reference.align(shape)

    test_tcs_colorimetry_data = _tcs_colorimetry_data(
        spd_test,
        spd_reference,
        tcs_spds,
        cmfs,
        chromatic_adaptation=True)

    reference_tcs_colorimetry_data = _tcs_colorimetry_data(
        spd_reference,
        spd_reference,
        tcs_spds,
        cmfs)

    Q_as = _colour_rendering_indexes(
        test_tcs_colorimetry_data, reference_tcs_colorimetry_data)

    Q_a = np.average(
        [v for k, v in Q_as.items()
         if k in (1, 2, 3, 4, 5, 6, 7, 8)])

    if additional_data:
        return CRI_Specification(Q_a,
                                 Q_as,
                                 (test_tcs_colorimetry_data,
                                  reference_tcs_colorimetry_data))
    else:
        return Q_a


def _tcs_colorimetry_data(spd_t,
                          spd_r,
                          spds_tcs,
                          cmfs,
                          chromatic_adaptation=False):
    """
    Returns the *test colour samples* colorimetry data.

    Parameters
    ----------
    spd_t : SpectralPowerDistribution
        Test spectral power distribution.
    spd_r : SpectralPowerDistribution
        Reference spectral power distribution.
    spds_tcs : dict
        *Test colour samples* spectral power distributions.
    cmfs : XYZ_ColourMatchingFunctions
        Standard observer colour matching functions.
    chromatic_adaptation : bool, optional
        Perform chromatic adaptation.

    Returns
    -------
    list
        *Test colour samples* colorimetry data.
    """

    XYZ_t = spectral_to_XYZ(spd_t, cmfs)
    uv_t = np.ravel(UCS_to_uv(XYZ_to_UCS(XYZ_t)))
    u_t, v_t = uv_t[0], uv_t[1]

    XYZ_r = spectral_to_XYZ(spd_r, cmfs)
    uv_r = np.ravel(UCS_to_uv(XYZ_to_UCS(XYZ_r)))
    u_r, v_r = uv_r[0], uv_r[1]

    tcs_data = []
    for key, value in sorted(TCS_INDEXES_TO_NAMES.items()):
        spd_tcs = spds_tcs.get(value)
        XYZ_tcs = spectral_to_XYZ(spd_tcs, cmfs, spd_t)
        xyY_tcs = np.ravel(XYZ_to_xyY(XYZ_tcs))
        uv_tcs = np.ravel(UCS_to_uv(XYZ_to_UCS(XYZ_tcs)))
        u_tcs, v_tcs = uv_tcs[0], uv_tcs[1]

        if chromatic_adaptation:
            c = lambda x, y: (4 - x - 10 * y) / y
            d = lambda x, y: (1.708 * y + 0.404 - 1.481 * x) / y

            c_t, d_t = c(u_t, v_t), d(u_t, v_t)
            c_r, d_r = (c(u_r, v_r),
                        d(u_r, v_r))
            tcs_c, tcs_d = c(u_tcs, v_tcs), d(u_tcs, v_tcs)
            u_tcs = ((10.872 + 0.404 * c_r / c_t * tcs_c - 4 *
                      d_r / d_t * tcs_d) /
                     (16.518 + 1.481 * c_r / c_t * tcs_c -
                      d_r / d_t * tcs_d))
            v_tcs = (5.52 / (16.518 + 1.481 * c_r / c_t * tcs_c -
                             d_r / d_t * tcs_d))

        W_tcs = 25 * xyY_tcs[-1] ** (1 / 3) - 17
        U_tcs = 13 * W_tcs * (u_tcs - u_r)
        V_tcs = 13 * W_tcs * (v_tcs - v_r)

        tcs_data.append(
            TCS_ColorimetryData(spd_tcs.name,
                                XYZ_tcs,
                                uv_tcs,
                                np.array([U_tcs, V_tcs, W_tcs])))

    return tcs_data


def _colour_rendering_indexes(test_data, reference_data):
    """
    Returns the *test colour samples* rendering indexes :math:`Q_a`.

    Parameters
    ----------
    test_data : list
        Test data.
    reference_data : list
        Reference data.

    Returns
    -------
    dict
        *Test colour samples* colour rendering indexes.
    """

    Q_as = {}
    for i, _ in enumerate(test_data):
        Q_as[i + 1] = 100 - 4.6 * np.linalg.norm(
            reference_data[i].UVW - test_data[i].UVW)
    return Q_as
