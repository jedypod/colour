# -*- coding: utf-8 -*-
"""
CAM16-LCD, CAM16-SCD, and CAM16-UCS Colourspaces - Li et al. (2017)
===================================================================

Defines the *Li, Li, Wang, Zu, Luo, Cui, Melgosa, Brill and Pointer (2017)*
*CAM16-LCD*, *CAM16-SCD*, and *CAM16-UCS* colourspaces transformations:

-   :func:`colour.JMh_CAM16_to_CAM16LCD`
-   :func:`colour.CAM16LCD_to_JMh_CAM16`
-   :func:`colour.JMh_CAM16_to_CAM16SCD`
-   :func:`colour.CAM16SCD_to_JMh_CAM16`
-   :func:`colour.JMh_CAM16_to_CAM16UCS`
-   :func:`colour.CAM16UCS_to_JMh_CAM16`
-   :func:`colour.XYZ_to_CAM16LCD`
-   :func:`colour.CAM16LCD_to_XYZ`
-   :func:`colour.XYZ_to_CAM16SCD`
-   :func:`colour.CAM16SCD_to_XYZ`
-   :func:`colour.XYZ_to_CAM16UCS`
-   :func:`colour.CAM16UCS_to_XYZ`

References
----------
-   :cite:`Li2017` : Li, C., Li, Z., Wang, Z., Xu, Y., Luo, M. R., Cui, G.,
    Melgosa, M., Brill, M. H., & Pointer, M. (2017). Comprehensive color
    solutions: CAM16, CAT16, and CAM16-UCS. Color Research & Application,
    42(6), 703-718. doi:10.1002/col.22131
"""

import re
from functools import partial

from colour.models.cam02_ucs import (
    COEFFICIENTS_UCS_LUO2006, JMh_CIECAM02_to_UCS_Luo2006,
    UCS_Luo2006_to_JMh_CIECAM02, JMh_CIECAM02_to_CAM02LCD,
    CAM02LCD_to_JMh_CIECAM02, JMh_CIECAM02_to_CAM02SCD,
    CAM02SCD_to_JMh_CIECAM02, JMh_CIECAM02_to_CAM02UCS,
    CAM02UCS_to_JMh_CIECAM02, XYZ_to_CAM02LCD, CAM02LCD_to_XYZ,
    XYZ_to_CAM02SCD, CAM02SCD_to_XYZ, XYZ_to_CAM02UCS, CAM02UCS_to_XYZ)
from colour.utilities import (as_float_array, copy_definition,
                              domain_range_scale, tsplit)

__author__ = 'Colour Developers'
__copyright__ = 'Copyright (C) 2013-2021 - Colour Developers'
__license__ = 'New BSD License - https://opensource.org/licenses/BSD-3-Clause'
__maintainer__ = 'Colour Developers'
__email__ = 'colour-developers@colour-science.org'
__status__ = 'Production'

__all__ = [
    'JMh_CAM16_to_UCS_Li2017', 'UCS_Li2017_to_JMh_CAM16',
    'JMh_CAM16_to_CAM16LCD', 'CAM16LCD_to_JMh_CAM16', 'JMh_CAM16_to_CAM16SCD',
    'CAM16SCD_to_JMh_CAM16', 'JMh_CAM16_to_CAM16UCS', 'CAM16UCS_to_JMh_CAM16',
    'XYZ_to_UCS_Li2017', 'UCS_Li2017_to_XYZ', 'XYZ_to_CAM16LCD',
    'CAM16LCD_to_XYZ', 'XYZ_to_CAM16SCD', 'CAM16SCD_to_XYZ', 'XYZ_to_CAM16UCS',
    'CAM16UCS_to_XYZ'
]


def _UCS_Luo2006_callable_to_UCS_Li2017_docstring(callable_):
    """
    Converts given *Luo et al. (2006)* callable docstring to
    *Li et al. (2017)* docstring.

    Parameters
    ----------
    callable_ : callable
        Callable to use the docstring from.

    Returns
    -------
    unicode
        Docstring.
    """

    docstring = callable_.__doc__
    docstring = docstring.replace('Luo et al. (2006)', 'Li et al. (2017)')
    docstring = docstring.replace('CIECAM02', 'CAM16')
    docstring = docstring.replace('CAM02', 'CAM16')
    docstring = docstring.replace('Luo2006b', 'Li2017')

    docstring = re.match('(.*)Examples', docstring, re.DOTALL).group(1)

    return docstring


JMh_CAM16_to_UCS_Li2017 = copy_definition(JMh_CIECAM02_to_UCS_Luo2006,
                                          'JMh_CAM16_to_UCS_Li2017')
JMh_CAM16_to_UCS_Li2017.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(JMh_CIECAM02_to_UCS_Luo2006))

UCS_Li2017_to_JMh_CAM16 = copy_definition(UCS_Luo2006_to_JMh_CIECAM02,
                                          'UCS_Li2017_to_JMh_CAM16')
UCS_Li2017_to_JMh_CAM16.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(UCS_Luo2006_to_JMh_CIECAM02))

JMh_CAM16_to_CAM16LCD = partial(
    JMh_CAM16_to_UCS_Li2017,
    coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-LCD'])
JMh_CAM16_to_CAM16LCD.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(JMh_CIECAM02_to_CAM02LCD))

CAM16LCD_to_JMh_CAM16 = partial(
    UCS_Li2017_to_JMh_CAM16,
    coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-LCD'])
CAM16LCD_to_JMh_CAM16.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(CAM02LCD_to_JMh_CIECAM02))

JMh_CAM16_to_CAM16SCD = partial(
    JMh_CAM16_to_UCS_Li2017,
    coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-SCD'])
JMh_CAM16_to_CAM16SCD.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(JMh_CIECAM02_to_CAM02SCD))

CAM16SCD_to_JMh_CAM16 = partial(
    UCS_Li2017_to_JMh_CAM16,
    coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-SCD'])
CAM16SCD_to_JMh_CAM16.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(CAM02SCD_to_JMh_CIECAM02))

JMh_CAM16_to_CAM16UCS = partial(
    JMh_CAM16_to_UCS_Li2017,
    coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-UCS'])
JMh_CAM16_to_CAM16UCS.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(JMh_CIECAM02_to_CAM02UCS))

CAM16UCS_to_JMh_CAM16 = partial(
    UCS_Li2017_to_JMh_CAM16,
    coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-UCS'])
CAM16UCS_to_JMh_CAM16.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(CAM02UCS_to_JMh_CIECAM02))


@domain_range_scale('1')
def XYZ_to_UCS_Li2017(XYZ, coefficients, **kwargs):
    """
    Converts from *CIE XYZ* tristimulus values to one of the *Li et al. (2017)*
    *CAM16-LCD*, *CAM16-SCD*, or *CAM16-UCS* colourspaces :math:`J'a'b'` array.

    Parameters
    ----------
    XYZ : array_like
        *CIE XYZ* tristimulus values.
    coefficients : array_like
        Coefficients of one of the *Li et al. (2017)* *CAM16-LCD*, *CAM16-SCD*,
        or *CAM16-UCS* colourspaces.

    Other Parameters
    ----------------
    \\**kwargs : dict, optional
        {:func:`colour.XYZ_to_CAM16`},
        Please refer to the documentation of the previously listed definition.
        The default viewing conditions are that of *IEC 61966-2-1:1999*, i.e.
        *sRGB* 64 Lux ambiant illumination, 80 :math:`cd/m^2`, adapting field
        luminance about 20% of a white object in the scene.

    Returns
    -------
    ndarray
        *Li et al. (2017)* *CAM16-LCD*, *CAM16-SCD*, or *CAM16-UCS*
        colourspaces :math:`J'a'b'` array.

    Warnings
    --------
    The domain-range scale is **'1'** and cannot be changed.

    Notes
    -----

    +------------+------------------------+------------------+
    | **Domain** |  **Scale - Reference** | **Scale - 1**    |
    +============+========================+==================+
    | ``XYZ``    | [0, 1]                 | [0, 1]           |
    +------------+------------------------+------------------+

    +------------+------------------------+------------------+
    | **Range**  |  **Scale - Reference** | **Scale - 1**    |
    +============+========================+==================+
    | ``Jpapbp`` | ``Jp`` : [0, 1]        | ``Jp`` : [0, 1]  |
    |            |                        |                  |
    |            | ``ap`` : [-1, 1]       | ``ap`` : [-1, 1] |
    |            |                        |                  |
    |            | ``bp`` : [-1, 1]       | ``bp`` : [-1, 1] |
    +------------+------------------------+------------------+

    Examples
    --------
    >>> import numpy as np
    >>> XYZ = np.array([0.20654008, 0.12197225, 0.05136952])
    >>> XYZ_to_UCS_Li2017(XYZ, COEFFICIENTS_UCS_LUO2006['CAM02-LCD'])
    ... # doctest: +ELLIPSIS
    array([ 0.4606586...,  0.4107586...,  0.1451025...])
    """

    from colour.appearance import (CAM_KWARGS_CIECAM02_sRGB, XYZ_to_CAM16)

    settings = CAM_KWARGS_CIECAM02_sRGB.copy()
    settings.update(**kwargs)

    specification = XYZ_to_CAM16(XYZ, **settings)
    JMh = as_float_array([specification.J, specification.M, specification.h])

    return JMh_CAM16_to_UCS_Li2017(JMh, coefficients)


@domain_range_scale('1')
def UCS_Li2017_to_XYZ(Jpapbp, coefficients, **kwargs):
    """
    Converts from one of the *Li et al. (2017)* *CAM16-LCD*, *CAM16-SCD*, or
    *CAM16-UCS* colourspaces :math:`J'a'b'` array to *CIE XYZ* tristimulus
    values.

    Parameters
    ----------
    Jpapbp : array_like
        *Li et al. (2017)* *CAM16-LCD*, *CAM16-SCD*, or *CAM16-UCS*
        colourspaces :math:`J'a'b'` array.
    coefficients : array_like
        Coefficients of one of the *Li et al. (2017)* *CAM16-LCD*, *CAM16-SCD*,
        or *CAM16-UCS* colourspaces.

    Other Parameters
    ----------------
    \\**kwargs : dict, optional
        {:func:`colour.CAM16_to_XYZ`},
        Please refer to the documentation of the previously listed definition.
        The default viewing conditions are that of *IEC 61966-2-1:1999*, i.e.
        *sRGB* 64 Lux ambiant illumination, 80 :math:`cd/m^2`, adapting field
        luminance about 20% of a white object in the scene.

    Returns
    -------
    ndarray
        *CIE XYZ* tristimulus values.

    Warnings
    --------
    The domain-range scale is **'1'** and cannot be changed.

    Notes
    -----

    +------------+------------------------+------------------+
    | **Domain** |  **Scale - Reference** | **Scale - 1**    |
    +============+========================+==================+
    | ``Jpapbp`` | ``Jp`` : [0, 1]        | ``Jp`` : [0, 1]  |
    |            |                        |                  |
    |            | ``ap`` : [-1, 1]       | ``ap`` : [-1, 1] |
    |            |                        |                  |
    |            | ``bp`` : [-1, 1]       | ``bp`` : [-1, 1] |
    +------------+------------------------+------------------+

    +------------+------------------------+------------------+
    | **Range**  |  **Scale - Reference** | **Scale - 1**    |
    +============+========================+==================+
    | ``XYZ``    | [0, 1]                 | [0, 1]           |
    +------------+------------------------+------------------+

    Examples
    --------
    >>> import numpy as np
    >>> Jpapbp = np.array([0.4606586, 0.41075865, 0.14510258])
    >>> UCS_Li2017_to_XYZ(
    ...     Jpapbp, COEFFICIENTS_UCS_LUO2006['CAM02-LCD'])
    ... # doctest: +ELLIPSIS
    array([ 0.2065400...,  0.1219722...,  0.0513695...])
    """

    from colour.appearance import (CAM_KWARGS_CIECAM02_sRGB,
                                   CAM_Specification_CAM16, CAM16_to_XYZ)

    settings = CAM_KWARGS_CIECAM02_sRGB.copy()
    settings.update(**kwargs)

    J, M, h = tsplit(UCS_Li2017_to_JMh_CAM16(Jpapbp, coefficients))

    specification = CAM_Specification_CAM16(J=J, M=M, h=h)

    return CAM16_to_XYZ(specification, **settings)


XYZ_to_CAM16LCD = partial(
    XYZ_to_UCS_Li2017, coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-LCD'])
XYZ_to_CAM16LCD.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(XYZ_to_CAM02LCD))

CAM16LCD_to_XYZ = partial(
    XYZ_to_UCS_Li2017, coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-LCD'])
CAM16LCD_to_XYZ.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(CAM02LCD_to_XYZ))

XYZ_to_CAM16SCD = partial(
    XYZ_to_UCS_Li2017, coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-SCD'])
XYZ_to_CAM16SCD.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(XYZ_to_CAM02SCD))

CAM16SCD_to_XYZ = partial(
    XYZ_to_UCS_Li2017, coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-SCD'])
CAM16SCD_to_XYZ.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(CAM02SCD_to_XYZ))

XYZ_to_CAM16UCS = partial(
    XYZ_to_UCS_Li2017, coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-UCS'])
XYZ_to_CAM16UCS.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(XYZ_to_CAM02UCS))

CAM16UCS_to_XYZ = partial(
    XYZ_to_UCS_Li2017, coefficients=COEFFICIENTS_UCS_LUO2006['CAM02-UCS'])
CAM16UCS_to_XYZ.__doc__ = (
    _UCS_Luo2006_callable_to_UCS_Li2017_docstring(CAM02UCS_to_XYZ))
