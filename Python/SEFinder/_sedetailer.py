"""
_sedetailer.py
---------------
Finds the time of minimum angular separation between the Sun and Moon
(as seen from the Earth's geocenter) within a given time range.
Dont put the whole year because it will find the most lowest angle of seperation at that year.
This function is a bit slow.
"""

from datetime import timedelta
from skyfield.api import load
from skyfield.positionlib import ICRF
import math

import _constants
import _ephempath


def sedetail(starttime, endtime):
	"""
	Finds the time and angular distance of the closest Sun–Moon approach.

	Args:
		starttime (datetime): Start of search range (UTC)
		endtime (datetime): End of search range (UTC)

	Returns:
		tuple:
			date (datetime): Time of minimum separation
			min_sep_angle (float): Minimum angular separation (radians)
	"""
	separations = []
	timestamps = []

	# Load Skyfield ephemerides and timescale once
	planets = load(_ephempath.EPHEM_PATH)
	ts = load.timescale()

	earth, sun, moon = planets["earth"], planets["sun"], planets["moon"]

	curtime = starttime

	# Step through each second to find region of closest approach
	while curtime <= endtime:
		t = ts.from_datetime(curtime)

		# Apparent positions
		obs_sun = earth.at(t).observe(sun)
		obs_moon = earth.at(t).observe(moon)

		# Angular separation (radians)
		sep_angle = float(
			ICRF(obs_moon.apparent().position.au)
			.separation_from(ICRF(obs_sun.apparent().position.au))
			.radians
		)

		# Distances (km)
		_, _, sdist = obs_sun.radec()
		_, _, mdist = obs_moon.radec()
		sdist_km, mdist_km = sdist.km, mdist.km

		# Eclipse geometry threshold (radians)
		eclipse_threshold_angle = (
			math.asin((_constants.MOON_RADIUS_KM + _constants.EARTH_RADIUS_KM) / mdist_km)
			+ math.asin((_constants.SUN_RADIUS_KM - _constants.EARTH_RADIUS_KM) / sdist_km)
		)

		if eclipse_threshold_angle >= sep_angle:
			separations.append(sep_angle)
			timestamps.append(curtime)

		# Increment time by 1 second
		curtime += timedelta(seconds=1)

	min_sep_angle = min(separations)
	min_index = separations.index(min_sep_angle)
	date = timestamps[min_index]

	return date, min_sep_angle