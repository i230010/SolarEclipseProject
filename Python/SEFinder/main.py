"""
main.py
-------
Solar Eclipse Finder (SEFinder)

Finds solar eclipses within a given timespan using Skyfield.
Scans for times when the Sun–Moon angular separation indicates
a potential eclipse near the geocenter.
"""

from datetime import datetime, timedelta, timezone
from skyfield.api import load
from skyfield.positionlib import ICRF
import math

import _sedetailer
import _constants
import _ephempath


def main():
	"""Main function to search for solar eclipses within a given timeframe."""
	# Time window for eclipse search
	start_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
	end_time = datetime(2025, 1, 1, tzinfo=timezone.utc)

	# Load Skyfield ephemerides and timescale once
	planets = load(_ephempath.EPHEM_PATH)
	ts = load.timescale()

	earth, sun, moon = planets['earth'], planets['sun'], planets['moon']

	current = start_time

	while current <= end_time:
		t = ts.from_datetime(current)

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
			math.asin((_constants.MOON_RADIUS_KM + _constants.EARTH_RADIUS_KM)
				/ mdist_km)
			+ math.asin((_constants.SUN_RADIUS_KM - _constants.EARTH_RADIUS_KM)
				/ sdist_km)
		)

		# Possible eclipse detected
		if eclipse_threshold_angle >= sep_angle:
			date, min_sep = _sedetailer.sedetail(
				current - timedelta(hours=2),
				current + timedelta(hours=4)
			)

			if date:
				print(date.strftime("%Y-%m-%dT%H:%M:%SZ"))
				# Optional: print also min separation in radians
				# print(date.strftime("%Y-%m-%dT%H:%M:%SZ"), f"{min_sep} rad")

			# Skip ahead roughly one synodic month (~27 days) (skips scanning between the eclipse month)
			current += timedelta(days=27)

		# Advance by 2 hours
		current += timedelta(hours=2)


# -------------------------------------------------------------------------
# Entry point of script
# -------------------------------------------------------------------------
if __name__ == "__main__":
	main()