//let models;
//let angles = 0;
//for(let i = 0; i < document.getElementById("modelNum").value; i++) {
//console.log(document.getElementById("modelName1").value);
let init = function() {
  //console.log(document.getElementById("modelNum"));
  let num = document.getElementById("modelNum").value;
  let model = [];
  for(let i = 1; i <= num; i++) {

    let sketch = function(m) {

      m.setup = function() {
        //console.log("setup()");
        //console.log(document.getElementById("modelNum").value);

        m.canvas = m.createCanvas(300, 240, m.WEBGL);
        //m.canvas.parent("Zeus");

        m.models = m.loadModel("/static/JS/3DModels/" + m.getModelName("modelName" + i));
        //console.log("/static/JS/3DModels/" + m.getModelName("modelNames"));
        m.angle = 0;
      };

      m.getModelName = function(value) {
        //console.log("getModelName()");
        return (document.getElementById(value).value + ".obj");
      };

      m.draw = function() {
      //console.log("draw()");

        m.background(228, 237, 219);
        //m.background(0);

        //console.log(getModelName());

        m.ambientLight(255);
        m.ambientMaterial(20, 77, 83);//#144D53

        m.stroke(13 * 1.5, 30* 1.5, 32* 1.5);//#1A3C40
        m.strokeWeight(1);

        //pushMatrix();

        m.translate(0, 0, 0);
        m.rotateY(m.radians(m.angle));
        m.rotateX(m.PI);
        m.scale(m.getScale());

        m.model(m.models);

        //popMatrix();
        m.resetMatrix();
        if(60/m.frameRate() < 10) {
          //console.log(60/m.frameRate());
          m.angle += 0.2 * 60/m.frameRate();
        } else {
          m.angle += 0.2;
        }
      };

      m.getScale = function() {
        if(i < 3) {
          return(20);
        } else if(i == 3){
          return(50);
        } else {
          return(4);
        }
      };
    };

    model.push(new p5(sketch, document.getElementById("modelName" + i).value));
  }

};
init();
