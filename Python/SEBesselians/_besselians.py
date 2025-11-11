"""
_besselians.py
---------------
Computes Besselian elements for a given datetime and fits
polynomials to these elements for smooth interpolation.
"""

import math
import numpy as np
from skyfield.api import load
from skyfield.units import Angle
import vector

import _constants
import _ephempath


# -----------------------------------------------------------------------------
# Convert distance from km to Earth radii
# -----------------------------------------------------------------------------
def kmtoearthradii(x):
	"""Convert a distance from km to Earth radii using _constants.EARTH_RADIUS_KM."""
	return x / _constants.EARTH_RADIUS_KM


# -----------------------------------------------------------------------------
# Core Besselian element calculation
# -----------------------------------------------------------------------------
def besselian_find(dt):
	"""
	Compute Besselian elements for a given datetime.

	Parameters
	----------
	dt : datetime.datetime
		UTC datetime of the desired eclipse instant.

	Returns
	-------
	x, y : float
		Coordinates of the Moon's shadow in Earth radii.
	d : float
		Declination of shadow axis (degrees).
	l1, l2 : float
		Distances to the northern/southern limits of the eclipse (Earth radii).
	u : float
		Hour angle of the Sun minus the shadow axis angle (degrees).
	tanf1, tanf2 : float
		Tangents used in shadow limit calculations.
	"""
	# Load planetary ephemerides
	planets = load(_ephempath.EPHEM_PATH)
	earth, sun, moon = planets["earth"], planets["sun"], planets["moon"]

	# Create timescale and convert datetime
	ts = load.timescale()
	t = ts.from_datetime(dt)

	# Apparent positions
	obs_sun = earth.at(t).observe(sun)
	obs_moon = earth.at(t).observe(moon)

	# Geocentric RA, Dec, distances
	sra, sdec, sdist = obs_sun.radec()
	mra, mdec, mdist = obs_moon.radec()

	# Convert distances to Earth radii
	rp = sdist.km / _constants.EARTH_RADIUS_KM
	r = mdist.km / _constants.EARTH_RADIUS_KM

	# RA and Dec in radians
	alp = sra.radians
	dlp = sdec.radians
	al = mra.radians
	dl = mdec.radians

	# Rectangular coordinates of Sun and Moon in Earth radii
	xs = rp * math.cos(dlp) * math.cos(alp)
	ys = rp * math.cos(dlp) * math.sin(alp)
	zs = rp * math.sin(dlp)

	xm = r * math.cos(dl) * math.cos(al)
	ym = r * math.cos(dl) * math.sin(al)
	zm = r * math.sin(dl)

	# Vectors
	Sar = vector.obj(x=xs, y=ys, z=zs)
	Mar = vector.obj(x=xm, y=ym, z=zm)

	# Vector from Moon to Sun
	Gar = Sar - Mar
	G = abs(Gar)

	# Shadow axis angle in XY-plane
	tana = (Gar.y / G) / (Gar.x / G)
	a = math.atan(tana)

	# Sine of shadow declination
	sind = Gar.z / G

	# Hour angle of Sun minus shadow axis angle
	u = Angle(degrees=(t.gast * 15)).radians - a

	# Shadow axis declination
	d = math.asin(sind)

	# Transform Moon coordinates relative to shadow axis
	x = r * (math.cos(dl) * math.sin(al - a))
	y = r * ((math.sin(dl) * math.cos(d)) - (math.cos(dl) * math.sin(d) * math.cos(al - a)))
	z = r * ((math.sin(dl) * math.sin(d)) + (math.cos(dl) * math.cos(d) * math.cos(al - a)))

	# Sun and Moon radii in Earth radii
	ds = _constants.SUN_RADIUS_KM / _constants.EARTH_RADIUS_KM
	k = _constants.MOON_RADIUS_KM / _constants.EARTH_RADIUS_KM

	# Compute sine of angles for shadow limits
	sinf1 = (ds + k) / G
	sinf2 = (ds - k) / G

	# Z-coordinates for shadow limits
	c1 = z + (k / sinf1)
	c2 = z - (k / sinf2)

	# Tangents for shadow limits
	tanf1 = math.tan(math.asin(sinf1))
	tanf2 = math.tan(math.asin(sinf2))

	# Distances along shadow axis to northern and southern limits
	l1 = c1 * tanf1
	l2 = c2 * tanf2

	return x, y, Angle(radians=d).degrees, l1, l2, Angle(radians=u).degrees, tanf1, tanf2


# -----------------------------------------------------------------------------
# Fit polynomial to Besselian elements
# -----------------------------------------------------------------------------
def find_besselian_polynomial(tm2, tm1, t, tp1, tp2):
	"""
	Fit a cubic polynomial to five samples of a Besselian element.

	Parameters
	----------
	tm2, tm1, t, tp1, tp2 : float
		Values at times -2h, -1h, 0h, +1h, +2h.

	Returns
	-------
	coeffs : ndarray
		Array of 4 polynomial coefficients.
	"""
	# Vandermonde-like matrix for polynomial fit
	A = np.array([
		[1, -2, 4, 8],
		[1, -1, 1, -1],
		[1, 0, 0, 0],
		[1, 1, 1, 1],
		[1, 2, 4, 8]
	], dtype=float)

	b = np.array([tm2, tm1, t, tp1, tp2], dtype=float)

	# Solve least-squares for polynomial coefficients
	coeffs, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)

	return coeffs