"""
main.py
-------
Solar Eclipse Besselians (SEBesselians)

Adapted from: https://celestialprogramming.com/eclipsesGeneratingBesselianElements/generatingBesselianPolynomials.html

Compute Besselian elements for a solar eclipse and fit cubic polynomials
to the elements for interpolation. Outputs raw values, polynomial coefficients,
and a formatted table for inspection.
"""

from datetime import datetime, timedelta, timezone
from skyfield.api import load

import _besselians


def main():
	"""
	Main script to compute Besselian elements for a solar eclipse
	and fit cubic polynomials to the elements for interpolation.
	"""

	# -------------------------------------------------------------------------
	# Define datetime of maximum eclipse in UTC
	# -------------------------------------------------------------------------
	dt = datetime(2024, 4, 8, 18, 17, 21, tzinfo=timezone.utc)

	# Round down minutes and seconds to zero (hourly alignment)
	dt = dt - timedelta(minutes=dt.minute, seconds=dt.second)

	# Skyfield timescale object
	ts = load.timescale()
	t = ts.from_datetime(dt)  # Skyfield Time object

	# -------------------------------------------------------------------------
	# Compute Besselian elements at five times: -2h, -1h, 0h, +1h, +2h
	# Each function call returns a tuple of elements:
	# (x, y, d, l1, l2, u, tanf1, tanf2)
	# -------------------------------------------------------------------------
	TM2 = _besselians.besselian_find(dt - timedelta(hours=2))
	TM1 = _besselians.besselian_find(dt - timedelta(hours=1))
	T   = _besselians.besselian_find(dt)
	TP1 = _besselians.besselian_find(dt + timedelta(hours=1))
	TP2 = _besselians.besselian_find(dt + timedelta(hours=2))

	# Print raw Besselian elements for inspection
	print("Besselian elements at five sample times:")
	print(TM2)
	print(TM1)
	print(T)
	print(TP1)
	print(TP2)
	print("")

	# -------------------------------------------------------------------------
	# Fit cubic polynomials to each Besselian element for smooth interpolation
	# Each call returns four coefficients (c0, c1, c2, c3)
	# -------------------------------------------------------------------------
	Xarr  = _besselians.find_besselian_polynomial(TM2[0], TM1[0], T[0],  TP1[0], TP2[0])
	Yarr  = _besselians.find_besselian_polynomial(TM2[1], TM1[1], T[1],  TP1[1], TP2[1])
	Darr  = _besselians.find_besselian_polynomial(TM2[2], TM1[2], T[2],  TP1[2], TP2[2])
	L1arr = _besselians.find_besselian_polynomial(TM2[3], TM1[3], T[3],  TP1[3], TP2[3])
	L2arr = _besselians.find_besselian_polynomial(TM2[4], TM1[4], T[4],  TP1[4], TP2[4])
	Micro = _besselians.find_besselian_polynomial(TM2[5], TM1[5], T[5],  TP1[5], TP2[5])

	# -------------------------------------------------------------------------
	# Unpack polynomial coefficients for clarity
	# -------------------------------------------------------------------------
	X0, X1, X2, X3 = Xarr
	Y0, Y1, Y2, Y3 = Yarr
	D0, D1, D2, D3 = Darr
	L10, L11, L12, L13 = L1arr
	L20, L21, L22, L23 = L2arr
	Micro0, Micro1, Micro2, Micro3 = Micro

	# Tangents of shadow limits (from the central time)
	Tanf1, Tanf2 = T[6], T[7]

	# -------------------------------------------------------------------------
	# Print polynomial coefficients for inspection
	# -------------------------------------------------------------------------
	print("Polynomial coefficients for each Besselian element:")
	print("X:", Xarr)
	print("Y:", Yarr)
	print("D:", Darr)
	print("L1:", L1arr)
	print("L2:", L2arr)
	print("Micro:", Micro)
	print("")

	# -------------------------------------------------------------------------
	# Print a formatted table of polynomial coefficients
	# -------------------------------------------------------------------------
	print(f"{'n':<3} {'X':>12} {'Y':>14} {'D':>14} "
		  f"{'L1':>14} {'L2':>14} {'Micro':>14}")
	print(f"0 {X0:14.10f} {Y0:14.10f} {D0:14.10f} "
		  f"{L10:14.10f} {L20:14.10f} {Micro0:14.10f}")
	print(f"1 {X1:14.10f} {Y1:14.10f} {D1:14.10f} "
		  f"{L11:14.10f} {L21:14.10f} {Micro1:14.10f}")
	print(f"2 {X2:14.10f} {Y2:14.10f} {D2:14.10f} "
		  f"{L12:14.10f} {L22:14.10f} {Micro2:14.10f}")
	print(f"3 {X3:14.10f} {Y3:14.10f} {D3:14.10f} "
		  f"{L13:14.10f} {L23:14.10f} {Micro3:14.10f}")

	print(f"tan(f1) = {Tanf1:14.10f} tan(f2) = {Tanf2:14.10f}")
	print("")

	# -------------------------------------------------------------------------
	# Print basic timing information
	# -------------------------------------------------------------------------
	print(f"T0 (maximum eclipse hour) = {dt.hour}h UTC")
	print(f"Delta T (TT - UT1) = {t.delta_t} s")
	print("")


# -------------------------------------------------------------------------
# Entry point of script
# -------------------------------------------------------------------------
if __name__ == "__main__":
	main()