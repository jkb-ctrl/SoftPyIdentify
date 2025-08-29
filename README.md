# SoftPyIdentify
SoftPyIdentify library with tools to identify the model of the actuators with flexible material.

This module provides a set of functions for the identification of the following transfer function:

v = f_nlr(u)

y = G<sub>slow</sub>(s)*G<sub>fast</sub>(s)*v

where:
- f<sub>nlr</sub>(u) - input nonlinearity as polynomial
- G<sub>slow</sub>(s) = $\frac{s+z_0}/{s+s_0}$
- G<sub>fast</sub>(s) = $\frac{k*(\alpha^2 + \omega^2)}{s^2 + 2*\alpha*s + \alpha^2 + \omega^2}$

The transfer functions holds G<sub>slow</sub>(0)*G<sub>fast</sub>(0) = 1, because the gain is specified in the f<sub>nlr</sub>(u).

The main functions are:
- split signal
- identify_static
- identify_fast
- identify_slow

The auxiliary functions for ploting are:
- get_slow_model_y
- get_fast_model_y

Install
-----
Directly from github:

pip install git+https://github.com/jkb-ctrl/SoftPyIdentify.git

Example
-----
See example.py (in https://github.com/jkb-ctrl/SoftPyIdentify-examples) to see how to use the package.

Notes
-----
The package is inspired by works:
1. Jakub Bernat, Paulina Superczyńska, Piotr Gajewski, Agnieszka Marcinkowska, Magnetorheological axisymmetric actuator with permanent magnet, Sensors and Actuators A: Physical, Volume 368, 1 April 2024, 115116, http://dx.doi.org/10.1016/j.sna.2024.115116
2. Jakub Bernat, Jakub Kolota, A PI Controller with a Robust Adaptive Law for a Dielectric Electroactive Polymer Actuator, Electronics 2021, 10(11), 1326, https://doi.org/10.3390/electronics10111326
