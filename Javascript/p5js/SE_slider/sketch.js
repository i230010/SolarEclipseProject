// Eclipse Date: 2 Aug 2027

// Canvas size constant
let canvasSize = 500;

// Function to convert radius to diameter
function convertRadiusToDiameter(radius) {
  return radius * 2;
}

// Function to convert hours, minutes, and seconds to decimal degrees
function convertHMSToDecimalHours(hours, minutes, seconds) {
  const minutesInAnHour = 60;
  const secondsInAnHour = 3600;
  return hours + (minutes / minutesInAnHour) + (seconds / secondsInAnHour);
}

// Astronomical data for sun and moon (in decimal degrees)
let sunAngularRadius = convertHMSToDecimalHours(0, 15, 45.5);
let moonAngularRadius = convertHMSToDecimalHours(0, 16, 43.1);
let gamma = 0.1421;  // Gamma value affecting moon's position

// Variables for canvas and astronomical calculations
let sunCanvasSize;
let moonCanvasSize;
let moonPositionX;
let moonPositionY;
let absoluteGamma;
let moonPositionSlider;
let isNorthernHemisphere;
let defaultMoonPosition = 0;
let sliderStep = 0.0001;

// Constants for gamma limits
const minGamma = 1.0266174;
const maxGamma = 1.56;

// Setup function for initial calculations and canvas setup
function setup() {
  // Create the canvas with defined size
  createCanvas(canvasSize, canvasSize);
  
  // Convert sun and moon angular radii to canvas sizes
  sunCanvasSize = convertRadiusToDiameter(sunAngularRadius) * canvasSize;
  moonCanvasSize = convertRadiusToDiameter(moonAngularRadius) * canvasSize;
  
  // Set stroke properties for drawing
  strokeWeight(1);  
  stroke(255);
  
  // Absolute value of gamma to calculate position
  absoluteGamma = Math.abs(gamma);
  
  // Determine if the gamma indicates a position in the northern hemisphere (gamma > 0) or southern hemisphere (gamma < 0)
  if (gamma > 0) {
    isNorthernHemisphere = true;
  } else {
    isNorthernHemisphere = false;
  }
  
  // Penumbral limit calculation based on sun and moon size
  let penumbralLimit = sunCanvasSize - ((sunCanvasSize - moonCanvasSize) / 2);
  
  // Position the moon based on the value of gamma
  if (absoluteGamma < minGamma) {
    moonPositionY = 0;  // If gamma is very small, keep the moon centered
  } else {
    let moonPositionOffset = 0;
    
    // Adjust moon's vertical position based on sun and moon size
    if (moonCanvasSize <= sunCanvasSize) {
      moonPositionOffset = (sunCanvasSize - moonCanvasSize) / 2;
    } else {
      moonPositionOffset = (sunCanvasSize - moonCanvasSize) / 2 * -1;
    }
    
    // Map the gamma value to determine the moon's position within the penumbral limit
    moonPositionY = map(absoluteGamma, minGamma, maxGamma, moonPositionOffset, penumbralLimit);
  }
  
  // Create a slider to control the moon's horizontal position
  moonPositionSlider = createSlider(penumbralLimit * -1, penumbralLimit, defaultMoonPosition, sliderStep);
  moonPositionSlider.position(0, canvasSize); 
  moonPositionSlider.size(canvasSize, 10);
}

// Draw function to render the sun and moon on the canvas
function draw() {
  // Set background color to avoid overlap between the sun and moon
  background(200);
  
  // Update the moon's horizontal position based on the slider value
  if (isNorthernHemisphere) {
    moonPositionX = moonPositionSlider.value();
  } else {
    moonPositionX = -moonPositionSlider.value();
  }
  
  // Draw the sun (yellow circle)
  fill(255, 170, 0);
  circle(canvasSize / 2, canvasSize / 2, sunCanvasSize);
  
  // Draw the moon (black circle with some transparency)
  fill(0, 0, 0, 180);
  circle(canvasSize / 2 - moonPositionX, canvasSize / 2 - moonPositionY, moonCanvasSize);
}
