let models;
let angles = 0;
let canvas;

function setup() {
  canvas = createCanvas(220, 220, WEBGL);
  canvas.parent("Zeus");

  models = loadModel("/static/JS/3DModels/" + getModelName());
}

function getModelName() {
  return document.getElementById("modelNames").value;
}

function draw() {
  background(228, 237, 219);
  //console.log(getModelName());
  ambientLight(228, 237, 219);
  pointLight(228, 237, 219, -30, -30, -30);
  ambientMaterial(20, 77, 83);//#144D53


  //pushMatrix();

  translate(0, 35, 0);
  rotateY(radians(angles));
  rotateX(PI);
  scale(0.4);

  model(models);

  //popMatrix();
  resetMatrix();

  angles += 0.1;
}
