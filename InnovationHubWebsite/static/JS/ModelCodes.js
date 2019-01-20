let WIDTH  = 300;
let HEIGHT = 240;

const VIEW_ANGLE = 45;
const ASPECT = WIDTH/HEIGHT;
const NEAR = 0.1;
const FAR = 1000;

const MATERIAL = [new THREE.MeshPhongMaterial({color: 0x1a3c40, shininess: 50, specular: 0x1a3c40}), new THREE.MeshStandardMaterial({color: 0x1a3c40, roughness: 0.4, metalness: 0.2})];

let init = function() {
  let num = document.getElementById("modelNum").value;
  models = [];

  let isHomePage = document.getElementById('isHomePage').value;

  for(let i = 1; i <= num; i++) {

    if(isHomePage == 'true' && i <= 4) {
      WIDTH  = 400;
      HEIGHT = 320;
    } else {
      WIDTH  = 300;
      HEIGHT = 240;
    };

    let tick = 0;
    let file_path = document.getElementById('modelName' + i).value;
    let container = document.getElementById(file_path);
    //let container = document.createElement('canvas');
    container.width  = WIDTH;
    container.height = HEIGHT;

    //parentDiv.appendChild(container);
    //console.log(parentDiv);

    let renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setSize(WIDTH, HEIGHT);

    container.appendChild(renderer.domElement);

    let camera = new THREE.PerspectiveCamera(VIEW_ANGLE, ASPECT, NEAR, FAR);
    camera.position.set(0, 0, 30);

    let scene = new THREE.Scene();
    scene.background = new THREE.Color(0xe4eddb);
    scene.add(camera);

    //let sphere = new THREE.Mesh(new THREE.SphereGeometry(50, 16, 16), MATERIAL);
    //sphere.position.z = -200;
    //scene.add(sphere);

    let geometryT = new THREE.BoxGeometry(10, 10, 10);
    let cube = new THREE.Mesh(geometryT, MATERIAL[0]);
    //scene.add(cube);
    //console.log(cube);


    //loading file
    let Mesh;
    let loader = new THREE.STLLoader();
    loader.load('../static/JS/3DModels/test_cube.stl', function(geometry){
      let mesh = new THREE.Mesh(geometry, MATERIAL[1]);
      //mesh.position.set(0, -1, 0);
      //mesh.rotation.set( - Math.PI / 2, 0, 0 );
      //mesh.scale.set(0.01, 0.01, 0.01);
      //mesh.position.set(-0.1101531982421875, -29.559922218322754, -16.02468403801322);
      //mesh.position.set(1, -0.5, -2);
      mesh.rotation.set( - Math.PI / 2, 0, 0 );
      //mesh.scale.set(0.2, 0.2, 0.2);
      mesh.geometry.computeBoundingBox();
      scene.add(mesh);

      //Translating:
      mesh.geometry.center();

      //let box = mesh.geometry.boundingBox;
      //let Cx = (box.min.x + box.max.x) /2.0;
      //let Cy = (box.min.y + box.max.y) /2.0;
      //let Cz = (box.min.z + box.max.z) /2.0;

      //mesh.geometry.center();

      //mesh.position.set(-1 * Cx, -1 * Cy, -1 * Cz);

      //Scaling:
      let box = mesh.geometry.boundingBox;
      let max = box.max;
      let min = box.min;

      let dimensions = [max.x - min.x, max.y - min.y, max.z - min.z];
      for(let j = 0; j < dimensions.length; j += 1) {
        dimensions[j] = Math.abs(dimensions[j]);
      };
      console.log(dimensions);

      let length_ratio = (WIDTH)/dimensions[0];
      let width_ratio  = (WIDTH)/dimensions[1];
      let height_ratio = (HEIGHT)/dimensions[2];

      //mesh.scale.set(length_ratio/14, width_ratio/14, height_ratio/14);

      if(length_ratio < width_ratio && length_ratio < height_ratio) {
        mesh.scale.set(length_ratio/14, length_ratio/14, length_ratio/14);
      } else if(width_ratio < height_ratio) {
        mesh.scale.set(width_ratio/14, width_ratio/14, width_ratio/14);
      } else {
        mesh.scale.set(height_ratio/14, height_ratio/14, height_ratio/14);
      };

      Mesh = mesh



      console.log(mesh);
    });

    //let axesHelper = new THREE.AxesHelper(100);
    //scene.add(axesHelper);


    let light = new THREE.AmbientLight(0x307672);
    scene.add(light);

    let spot_light = new THREE.PointLight(0x144d53, 1);
    spot_light.position.set(10, 10, 10);
    scene.add(spot_light);
    spot_light = new THREE.PointLight(0x144d53, 1);
    spot_light.position.set(10, 9, 5);
    scene.add(spot_light);
    spot_light = new THREE.PointLight(0x144d53, 1);
    spot_light.position.set(Math.sin(60) * 10, Math.sin(60) * 10, Math.sin(60) * 10);
    scene.add(spot_light);
    spot_light = new THREE.PointLight(0x144d53, 1);
    spot_light.position.set(0, Math.sin(60) * 10, Math.sin(60) * 10);
    scene.add(spot_light);
    spot_light = new THREE.PointLight(0x144d53, 1);
    spot_light.position.set(-10, -10, -10);
    scene.add(spot_light);

    let hem_light = new THREE.HemisphereLight(0xe4eddb, 0xe4eddb, 0.7);
    scene.add(hem_light);

    //let loader = new THREE.STLLoader();
    //loader.load();

    let update = function() {
      cube.rotation.z += 0.01;
      cube.rotation.y += 0.01;
      cube.rotation.x += 0.01;

      if(Mesh) {
        //camera.position.set(Mesh.position.x, Mesh.position.y, Mesh.position.z + 10);
        Mesh.rotation.z += 0.01;
        //Mesh.rotation.y += 0.01;
        //Mesh.rotation.x += 0.01;
      }

      //camera.position.set(Math.sin(tick) * 4, 0, Math.cos(tick) * 4);
      //control.update();
      //camera.rotation.set(0, Math.tan(tick), 0);
    };

    let render = function() {
      renderer.render(scene, camera);
    };

     let animate = function() {
       requestAnimationFrame(animate);
       tick += 0.001;

       update();
       render();
     };

     animate();

  };
};

$(document).ready(function() {
  init();
});
