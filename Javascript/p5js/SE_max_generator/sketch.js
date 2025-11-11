// =============================================
//  ECLIPSE VISUALIZATION (p5.js)
//  Eclipse Date: 29 Apr 2014
// =============================================

// -------------------------------------------------------------
// CONFIG
// -------------------------------------------------------------

// Canvas size in pixels (the drawing area will be 500x500)
let canvasSize = 500;

// -------------------------------------------------------------
// HELPER FUNCTIONS
// -------------------------------------------------------------

/**
 * Converts a radius value to diameter.
 * 
 * @param {number} radius - The radius.
 * @returns {number} The diameter (2 * radius).
 */
function radiusToDiameter(radius) {
  return radius * 2;
}

/**
 * Converts hours, minutes, and seconds to decimal hours.
 * 
 * This is used because celestial measurements (like Sun or Moon
 * apparent sizes) are often given in time-based angular units.
 * 
 * @param {number} hours - Hours.
 * @param {number} minutes - Minutes.
 * @param {number} seconds - Seconds.
 * @returns {number} The decimal representation in hours.
 */
function hmsToDecimal(hours, minutes, seconds) {
  const minutesInHour = 60;
  const secondsInHour = 3600;

  return hours + (minutes / minutesInHour) + (seconds / secondsInHour);
}

// -------------------------------------------------------------
// DATA (Astronomical Parameters for April 29, 2014 Eclipse)
// -------------------------------------------------------------

// Angular sizes of the Sun and Moon (in decimal hours)
let sunAngularSize = hmsToDecimal(0, 15, 52.9);
let moonAngularSize = hmsToDecimal(0, 15, 38.4);

// Gamma (?) parameter — describes the alignment of the eclipse.
// Negative gamma means the Moon passes below the Sun’s center.
let gamma = -0.99996;

// -------------------------------------------------------------
// VARIABLES (Canvas Calculations)
// -------------------------------------------------------------

// Computed canvas versions of the Sun/Moon sizes
let sunSizeInPixels;
let moonSizeInPixels;

// Vertical position of the Moon relative to the Sun
let moonOffsetY;

// Canvas-adjusted gamma value
let adjustedGamma;

// -------------------------------------------------------------
// GAMMA RANGE CONSTANTS
// -------------------------------------------------------------

// These define when the Moon begins/ends its partial path across the Sun.
const minGamma = 1.0266174; // Near-central eclipse limit
const maxGamma = 1.56;      // Far limit (no visible overlap)

// -------------------------------------------------------------
// SETUP FUNCTION (runs once at start)
// -------------------------------------------------------------

function setup() {
  // 1. Create the drawing canvas
  createCanvas(canvasSize, canvasSize);

  // 2. Convert angular sizes to pixel sizes for display
  //    The multiplication by canvas size is arbitrary — it scales for visibility.
  sunSizeInPixels = radiusToDiameter(sunAngularSize) * canvasSize;
  moonSizeInPixels = radiusToDiameter(moonAngularSize) * canvasSize;

  // 3. Set background and drawing styles
  background(200);   // Light gray sky
  strokeWeight(1);    // Thin border for circles
  stroke(255);        // White outline for contrast

  // 4. Convert gamma to an absolute value for position calculations
  adjustedGamma = abs(gamma);

  // 5. Determine the Moon's offset position relative to the Sun
  if (adjustedGamma < minGamma) {
    // If gamma is small (central eclipse), the Moon covers the Sun centrally
    moonOffsetY = 0;
  } else {
    // Otherwise, we calculate how far the Moon’s disk should be from the Sun’s center

    // "Penumbral limit" — maximum offset where disks still interact
    let maxMoonOffsetY = sunSizeInPixels - ((sunSizeInPixels - moonSizeInPixels) / 2);
    let minMoonOffsetY;

    // Adjust starting offset depending on which disk is larger
    if (moonSizeInPixels <= sunSizeInPixels) {
      // Typical case — Moon smaller than Sun
      minMoonOffsetY = ((sunSizeInPixels - moonSizeInPixels) / 2);
    } else {
      // Rare case — Moon larger than Sun (total eclipse)
      minMoonOffsetY = ((sunSizeInPixels - moonSizeInPixels) / 2) * -1;
    }

    // Map the gamma range (min to max) into a positional range (minMoonOffsetY to maxMoonOffsetY)
    moonOffsetY = map(adjustedGamma, minGamma, maxGamma, minMoonOffsetY, maxMoonOffsetY);
  }

  // 6. Draw the Sun and Moon circles
  // ---------------------------------------------------------
  // SUN: orange-yellow circle centered on the canvas
  fill(255, 170, 0); // warm orange
  circle(canvasSize / 2, canvasSize / 2, sunSizeInPixels);

  // MOON: dark translucent circle offset vertically by 'moonOffsetY'
  fill(0, 0, 0, 180); // semi-transparent black
  circle(canvasSize / 2, (canvasSize / 2) - moonOffsetY, moonSizeInPixels);
}

// -------------------------------------------------------------
// DRAW FUNCTION (runs continuously, but unused here)
// -------------------------------------------------------------

function draw() {
  // No continuous drawing needed — static visualization
}