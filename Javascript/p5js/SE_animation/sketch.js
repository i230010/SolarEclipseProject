// Eclipse Date: 16 Jul 2186
// Solar Eclipse Animation without Slider but using timer

// Canvas size constant
let canvasSize = 750;

// Function to convert radius to diameter
function convertRadiusToDiameter(radius) {
  return radius * 2;
}

// Function to convert hours, minutes, and seconds to decimal hours
function convertHMSToDecimalHours(hours, minutes, seconds) {
  const minutesInAnHour = 60;
  const secondsInAnHour = 3600;
  return hours + (minutes / minutesInAnHour) + (seconds / secondsInAnHour);
}

// Astronomical data for sun and moon (in decimal degrees)
let sunAngularRadius = convertHMSToDecimalHours(0, 15, 44.1);
let moonAngularRadius = convertHMSToDecimalHours(0, 16, 43.2);
let gamma = -0.23964;  // Gamma value affecting moon's position

// Variables for canvas and astronomical calculations
let sunCanvasSize;
let moonCanvasSize;
let moonPositionX;
let moonPositionY;
let absoluteGamma;
let direction;
let xPosition;
let isTotalEclipse;

// Constants for gamma limits
const minGamma = 1.0266174;
const maxGamma = 1.56;

// Convert angular sizes of the sun and moon to canvas sizes
sunCanvasSize = convertRadiusToDiameter(sunAngularRadius) * canvasSize;
moonCanvasSize = convertRadiusToDiameter(moonAngularRadius) * canvasSize;

// Non-central eclipse limit
let nonCentralEclipseLimit;
let totalEclipseIndicator;

// Check for total or non-central eclipse
if (moonCanvasSize <= sunCanvasSize) {
  nonCentralEclipseLimit = (sunCanvasSize - moonCanvasSize) / 2;
  totalEclipseIndicator = 0;
} else {
  nonCentralEclipseLimit = (sunCanvasSize - moonCanvasSize) / 2 * -1;
  totalEclipseIndicator = 1;
}

// Penumbral limit for the moon's position
let penumbralLimit = sunCanvasSize - (sunCanvasSize - moonCanvasSize) / 2;

// Setup function to initialize canvas and calculate moon's position
function setup() {
  // Create canvas
  createCanvas(canvasSize, canvasSize);
  
  // Set stroke properties
  noStroke();
  
  // Absolute value of gamma to calculate the moon's vertical position
  absoluteGamma = Math.abs(gamma);
  
  // Determine if the eclipse is in the northern hemisphere (gamma > 0) or southern hemisphere (gamma < 0)
  if (gamma > 0) {
    direction = 1;  // North (right to left)
  } else {
    direction = 0;  // South (left to right)
  }
  
  // If gamma is less than the non-central limit, keep the moon centered
  if (absoluteGamma < minGamma) {
    moonPositionY = 0;
  } else {
    // Otherwise, map the gamma value to determine the moon's vertical position
    moonPositionY = map(absoluteGamma, minGamma, maxGamma, nonCentralEclipseLimit, penumbralLimit);
  }
  
  // Initial x position of the moon for animation
  xPosition = penumbralLimit * -1;
}

// Draw function to render the sun and moon on the canvas
function draw() {
  // Define colors for the moon and sky
  let moonColor = color("#000000");
  let skyColor = color("#1439FF");
  
  // Ensure the x position is within the penumbral limit
  if (xPosition >= penumbralLimit) {
    xPosition = penumbralLimit * -1;
  }
  
  // Animation logic for the moon's horizontal position
  if (xPosition >= -20 && xPosition <= 20) {
    xPosition += 0.1;
  } else {
    xPosition += 1;
  }
  
  // Update the moon's position based on the hemisphere direction
  if (direction === 1) {
    moonPositionX = xPosition;
  } else {
    moonPositionX = -xPosition;
  }
  
  // Check if it's a total eclipse or a non-central eclipse
  if ((xPosition <= nonCentralEclipseLimit && xPosition >= -nonCentralEclipseLimit) && totalEclipseIndicator) {
    // Set background to black during total eclipse
    background(0);
    
    // Draw the corona with a gradient effect
    fill(color("#EC8C00"));
    circle(canvasSize / 2, canvasSize / 2, sunCanvasSize + (canvasSize / 4) - 50);
  } else {
    // Set background to sky color during partial eclipse
    background(skyColor);
    moonColor = skyColor;
  }
  
  // Draw the sun (yellow circle)
  fill(color("rgb(255, 170, 0)"));
  circle(canvasSize / 2, canvasSize / 2, sunCanvasSize);
  
  // Draw the moon (black circle with transparency during the eclipse)
  fill(moonColor);
  circle(canvasSize / 2 - moonPositionX, canvasSize / 2 - moonPositionY, moonCanvasSize);
}