"""
==============================================================================================
SoftPyIdentify library with tools to identify the model of the actuators with flexible material.
==============================================================================================

This module provides a set of functions for the identification of the following transfer function:
v = f_nlr(u)
y = Gslow(s)*Gfast(s)*v
where:
f_nlr(u) - input nonlinearity
Gslow(s) - (s+z0)/(s+s0)
Gfast(s) - k*(alpha^2 + omega^2)/(s^2 + 2*alpha*s + alpha^2 + omega^2)

The transfer functions holds Gslow(0)*Gfast(0) = 1, because the gain is specified in the f_nlr(u).

The main functions are:
- split signal
- identify_static
- identify_fast
- identify_slow

The auxiliary functions for ploting are:
- get_slow_model_y
- get_fast_model_y

Notes
-----
The package is inspired by works:
[1] Jakub Bernat, Paulina Superczyńska, Piotr Gajewski, Agnieszka Marcinkowska, Magnetorheological axisymmetric actuator with permanent magnet, Sensors and Actuators A: Physical, Volume 368, 1 April 2024, 115116, http://dx.doi.org/10.1016/j.sna.2024.115116
[2] Jakub Bernat, Jakub Kolota, A PI Controller with a Robust Adaptive Law for a Dielectric Electroactive Polymer Actuator, Electronics 2021, 10(11), 1326, https://doi.org/10.3390/electronics10111326

"""

# functions for identification:
from .__split_signal import split_signal
from .__identify_static import identify_static
from .__identify_fast import identify_fast
from .__identify_slow import identify_slow

# tools for ploting:
from .__identify_slow import get_slow_model_y
from .__identify_fast import get_fast_model_y
