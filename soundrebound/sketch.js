/*
CodingTrain Sketch 
*/
var ball = {
  x: 300,
  y: 200,
  xspeed: 4,
  yspeed: -3
}

// A sound file object
let soundfile;

window.onload = function() {
var context = new AudioContext();
}

function preload(){
  // Load the sound file.
  getAudioContext();
  soundFormats('mp3');
  soundfile = loadSound('http://localhost:8000/assets/metal_hit.mp3');
}

function setup() {
  createCanvas(600, 400);
}

function draw() {
  background(0);
  move();
  bounce();
  display();
}

function move(){
  ball.x = ball.x + ball.xspeed;
  ball.y = ball.y + ball.yspeed;
}

function bounce(){
  if (ball.x > width || ball.x < 0){
    ball.xspeed = -ball.xspeed;
    soundfile.play();

  }
  if (ball.y > height || ball.y < 0){
    ball.yspeed = -ball.yspeed;
    soundfile.play();

  }

}

function display(){
  stroke(255);
  strokeWeight(4);
  fill(255,0,200);

    ellipse(ball.x, ball.y, 24, 24);
}
