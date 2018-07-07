let canvas;
let particles = [];

let pNum;

function setup() {
  canvas = createCanvas(windowWidth, windowHeight);
  //canvas.position(0, 0);
  canvas.parent("Background");

  pNum = (windowWidth + windowHeight)/20;

  for(let i = 0; i < pNum; i++) {
    particles.push(new Particle(random(0, canvas.width), random(0, canvas.height), random(-0.1, 0.1), random(-0.1, 0.1), random(10, 30), int(random(0, 2)), canvas.width, canvas.height));
  }
  //console.log(mouseX);
}

function draw() {
  background(228, 237, 219);

  for(let i = 0; i < particles.length; i++) {
    particles[i].update();
    particles[i].show();

    forceX = (particles[i].x - mouseX) * -0.4;
    forceY = (particles[i].y - mouseY) * -0.4;

    distance = sqrt(pow(particles[i].x - mouseX, 2) + pow(particles[i].y - mouseY, 2));

    if(distance < 50) {
      forceX *= 1.0/(distance * 30);
      forceY *= 1.0/(distance * 30);

      particles[i].applyForce(forceX, forceY);
    } else {

      if(particles[i].vx > 1 || particles[i].vx < -1) {
        particles[i].vx *= 0.99;
      }

      if(particles[i].vy > 1 || particles[i].vy < -1) {
        particles[i].vy *= 0.99;
      }
    }
  }
  //console.log(mouseX);
}

class Particle {

  constructor(x, y, vx, vy, r, c, w, h){
    this.x = x;
    this.y = y;

    this.vx = vx;
    this.vy = vy;

    this.ax = 0;
    this.ay = 0;

    this.r = r;

    if(c < 1) {
      this.c1 = [48, 118, 114];
      this.c2 = [20, 77, 83];
    } else {
      this.c1 = [20, 77, 83];
      this.c2 = [48, 118, 114];
    }

    this.w = w;
    this.h = h;
  }

  show() {
    fill(this.c1[0], this.c1[1], this.c1[2]);
    stroke(this.c2[0], this.c2[1], this.c2[2]);
    strokeWeight(3);

    ellipse(this.x, this.y, this.r, this.r);
  }

  update() {
    this.vx += this.ax;
    this.vy += this.ay;

    this.constrainVel(2);

    this.x  += this.vx;
    this.y  += this.vy;

    this.wrap();

    this.ax = 0;
    this.ay = 0;
  }

  applyForce(fx, fy) {
    this.ax = fx;
    this.ay = fy;
  }

  wrap() {
    if(this.x > this.w + this.r) {
      this.x = -this.r;
    } else if(this.x < -this.r) {
      this.x = this.w + this.r;
    }

    if(this.y > this.w + this.r) {
      this.y = -this.r;
    } else if(this.y < -this.r) {
      this.y = this.w + this.r;
    }
  }

  constrainVel(v) {
    if(this.vx > v) {
      this.vx = v;
    } else if(this.vx < -v) {
      this.vx = -v
    }

    if(this.vy > v) {
      this.vy = v;
    } else if(this.vx < -v) {
      this.vy = -v
    }
  }
}
