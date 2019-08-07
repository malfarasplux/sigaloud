/*
RapidMix Getting started
https://www.doc.gold.ac.uk/eavi/rapidmixapi.com/index.php/getting-started/
*/

// Websockets
var launchWS = true;
console.log('ws state: ', launchWS);
if (launchWS){
  var ws = new WebSocket("ws://localhost:9001/");
ws.onopen = function() {
}} else{var ws =''};


// Detect when the page is unloaded or close
window.onbeforeunload = function() {
    ws.onclose = function () {};
    ws.close()
};

// Create server sent event connection to receive riot sensor data.
ws.onmessage = function(e) {
  // Update riot sensor values.
  data = JSON.parse(e.data)
  orientation_labels = ["Q1", "Q2", "Q3", "Q4"]
  var test_data_stream = ""
  for (var i = 0; i < orientation_labels.length; i += 1){
    ch = orientation_labels[i]
    test_data_stream += ch + ": " + data[ch] + "<br />"
  }
  updateSensorData(data);
};
ws.onopen = function(e) {
  };

ws.onerror = function(e) {
};

/////////////////////////////////////////////////////////////////////////////////////////////

// Global state.
var imuData = null;

var mouseX;
var mouseY;

//Mouse
onmousemove = function(e){
  mouseX = e.clientX; 
  mouseY = e.clientY;
  if (!launchWS){
  imuData = [mouseX, mouseY];
  }
  var newSpeed;
  if (ball.xspeed != 0){
    newSpeed = Math.sign(ball.xspeed) * mouseX
    ball.xspeed = map(newSpeed, 0, width, 0, 20);
  }else{
    newSpeed = mouseX
    ball.xspeed = map(newSpeed, 0, width, 0, 20);
  }
}

// Function called when a new sensor reading is received.
    function updateSensorData(data) {
    // Save the reading then update the UI.
    // labels = ["ACC_X", "ACC_Y", "ACC_Z", "GYRO_X", "GYRO_Y", "GYRO_Z", "MAG_X", "MAG_Y", "MAG_Z",
    // "TEMP", "IO", "A1", "A2", "C", "Q1", "Q2", "Q3", "Q4", "PITCH", "YAW", "ROLL", "HEAD"]
   
    if (launchWS){
    imuData = [data.ACC_X, data.ACC_Y];
    }
  }

// p5
var ball = {
  x: 300,
  y: 200,
  xspeed: -4,
  yspeed: -3
}

var colorBall;
let osc;
let fft;

function preload(){
  //p5 oscillator
  osc = new p5.SinOsc(); // 
  osc.amp(0.2);

  fft = new p5.FFT();
  osc.start();
  osc.freq(40);


  colorBall = [color(255,100,200), color(0,0,0), color(255,0,0)];
}

function setup() {
  createCanvas(600, 400);  
  }

 function draw() {
   background(10);
   move();
   bounce();
   display();

   //Change synth freq according to ball speed
   // let freq = map(Math.sign(ball.xspeed)*ball.xspeed, 0, 20, 40, 880);
   // osc.freq(freq);

  // Launch RapidMIX Train / Classify
  if (runState){
  rapidInput = imuData;
  runClassification(rapidInput);
  var fval = parseFloat(classificationOutput[0]);
  let freq = map(fval, 0, 3, 220, 880);
  console.log(freq);
  osc.freq(freq);
  }

    if (recordState){
    rapidInput = imuData;
    var rapidOutput =  [myOutput];
    myTrainingSet.push({
      input: rapidInput,
      output: rapidOutput
    });
   }
 }

function setup() {
  createCanvas(600, 400);
}


function move(){
  ball.x = ball.x + ball.xspeed;
  ball.y = ball.y + ball.yspeed;
}

function bounce(){
  if (ball.x > width || ball.x < 0){
    ball.xspeed = -ball.xspeed;
  }
  if (ball.y > height || ball.y < 0){
    ball.yspeed = -ball.yspeed;
  }
}

function display(){
  stroke(255);
  strokeWeight(4);
  defaultC = color(255,100,200);
  fill(defaultC);

  if (typeof classificationOutput === 'undefined'){
    fill(defaultC);  
    } else{
    fill(colorBall[classificationOutput]);  
  }
  ellipse(ball.x, ball.y, 24, 24);
}

////////////////////////////////////////////////////////////////////////////////////////////


// RapidMIX
  var rapidLib = window.RapidLib();
  var myClassification = new rapidLib.Classification();
  var myTrainingSet = [];
  var myOutput = '';
  var recordState;
  var runState;
  var rapidInput;

  // Get current state classification
  var classificationOutput;
  function runClassification(input){
  classificationOutput = myClassification.run(input);
  }

  //Train the model when called
  var trained = false;
  function trainMe(){
    console.log('this was trained: ', myClassification.train(myTrainingSet));
    trained = true;
  }

 //Launch training and classifying + assign label
 window.addEventListener('keydown', this.startRecord, false);
 function startRecord(e){
  if (e.keyCode > 47 && e.keyCode < 58){
    myOutput = e.keyCode - 48; 
    recordState = true;
    console.warn("recording");
  }
 }
  window.addEventListener('keyup', this.stopRecord, false);
 function stopRecord(e){
  if (e.keyCode > 47 && e.keyCode < 58){
    myOutput = e.keyCode - 48; 
    recordState = false;
    console.warn("stopped recording");

    // Train the Model
    trainMe();
    runState = true;
  }
 }