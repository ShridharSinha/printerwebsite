			var container, stats;

			var camera, cameraTarget, scene, renderer;

      $(document).ready(function() {
        init();
			  animate();
      });



			function init() {

				//container = document.createElement( 'div' );
        container = document.getElementById("Model");

        let width  = container.width
        let height = container.height
				//document.body.appendChild( container );
        console.log(container);

				camera = new THREE.PerspectiveCamera( 35, container.width / container.height, 1, 100 );
				camera.position.set( 3, 0.15, 3 );

				cameraTarget = new THREE.Vector3( 0, - 0.25, 0 );

				scene = new THREE.Scene();
				scene.background = new THREE.Color( 0x000000 );
				//scene.fog = new THREE.Fog( 0x72645b, 2, 15 );


				// Ground

				/*var plane = new THREE.Mesh(
					new THREE.PlaneBufferGeometry( 40, 40 ),
					new THREE.MeshPhongMaterial( { color: 0x999999, specular: 0x101010 } )
				);
				plane.rotation.x = - Math.PI / 2;
				plane.position.y = - 0.5;
				//scene.add( plane );

				plane.receiveShadow = true;*/


				// ASCII file
        //let box;
        console.log(container);

				var loader = new THREE.STLLoader();
				loader.load( '../static/JS/3DModels/Dragon.stl', function ( geometry ) {

					var material = new THREE.MeshPhongMaterial( { color: 0x1a3c40, specular: 0xaaaaaa, shininess: 1000 } );
					var mesh = new THREE.Mesh( geometry, material );

          console.log(mesh);

          let geom = mesh.geometry;
          geom.computeBoundingBox();
          console.log(geom);

          let cuboid = geom.boundingBox;
          console.log(cuboid);

          let vectors = [cuboid.max, cuboid.min];
          console.log(vectors);

          let max_min = [[vectors[0].x, vectors[0].y, vectors[0].z],
                         [vectors[1].x, vectors[1].y, vectors[1].z]];
          console.log(max_min);

          let offset = [];

          for(let i = 0; i < 3; i = i + 1) {
            offset[i] = -1 * (max_min[0][i] + max_min[1][i])/2.0;
          }
          console.log(offset);

          mesh.position.set(0, -0.29, 0);
					//mesh.position.set( 0, - 0.25, 0.6 );
          //mesh.position.set(offset[0], offset[1], offset[2]);
					mesh.rotation.set( - Math.PI / 2, 0, 0 );
					mesh.scale.set(0.01, 0.01, 0.01);

					mesh.castShadow = true;
					mesh.receiveShadow = true;

					scene.add( mesh );


          //vectors = [cuboid.min, cuboid.max];
          //console.log('Vectors :');
          //console.log(vectors);

          //var edges = new THREE.EdgesGeometry(mesh);
          //console.log('The Edges are ' + edges);

				} );

        //let centre = box.getCenter();
        //console.log(centre);


				// Binary files
        console.log(container);

				var material = new THREE.MeshPhongMaterial( { color: 0xAAAAAA, specular: 0x111111, shininess: 200 } );

				/*loader.load( './models/stl/binary/pr2_head_pan.stl', function ( geometry ) {

					var mesh = new THREE.Mesh( geometry, material );

					mesh.position.set( 0, - 0.37, - 0.6 );
					mesh.rotation.set( - Math.PI / 2, 0, 0 );
					mesh.scale.set( 2, 2, 2 );

					mesh.castShadow = true;
					mesh.receiveShadow = true;

					scene.add( mesh );

				} );

				loader.load( './models/stl/binary/pr2_head_tilt.stl', function ( geometry ) {

					var mesh = new THREE.Mesh( geometry, material );

					mesh.position.set( 0.136, - 0.37, - 0.6 );
					mesh.rotation.set( - Math.PI / 2, 0.3, 0 );
					mesh.scale.set( 2, 2, 2 );

					mesh.castShadow = true;
					mesh.receiveShadow = true;

					scene.add( mesh );

				} );

				// Colored binary STL
				loader.load( './models/stl/binary/colored.stl', function ( geometry ) {

					var meshMaterial = material;
					if ( geometry.hasColors ) {

						meshMaterial = new THREE.MeshPhongMaterial( { opacity: geometry.alpha, vertexColors: THREE.VertexColors } );

					}

					var mesh = new THREE.Mesh( geometry, meshMaterial );

					mesh.position.set( 0.5, 0.2, 0 );
					mesh.rotation.set( - Math.PI / 2, Math.PI / 2, 0 );
					mesh.scale.set( 0.3, 0.3, 0.3 );

					mesh.castShadow = true;
					mesh.receiveShadow = true;

					scene.add( mesh );

				} );*/


				// Lights

				//scene.add( new THREE.HemisphereLight( 0x443333, 0x111122 ) );

        console.log(container);
				addShadowedLight( 1, 1, 1, 0xe4eddb, 0.5 );
				addShadowedLight( 0.5, 1, - 1, 0xe4eddb, 0.5 );
				// renderer

        console.log(container);
        renderer = new THREE.WebGLRenderer( { antialias: true } );
				renderer.setPixelRatio( window.devicePixelRatio );
				renderer.setSize( window.innerWidth, window.innerHeight );

				renderer.gammaInput = true;
				renderer.gammaOutput = true;

				renderer.shadowMap.enabled = true;

        console.log(container);
				container.appendChild( renderer.domElement );
        console.log('done');

				// stats

				//stats = new Stats();
				//container.appendChild( stats.dom );

				//

				window.addEventListener( 'resize', onWindowResize, false );

			}

			function addShadowedLight( x, y, z, color, intensity ) {

				var directionalLight = new THREE.DirectionalLight( color, intensity );
				directionalLight.position.set( x, y, z );
				scene.add( directionalLight );

				directionalLight.castShadow = true;

				var d = 1;
				directionalLight.shadow.camera.left = - d;
				directionalLight.shadow.camera.right = d;
				directionalLight.shadow.camera.top = d;
				directionalLight.shadow.camera.bottom = - d;

				directionalLight.shadow.camera.near = 1;
				directionalLight.shadow.camera.far = 4;

				directionalLight.shadow.mapSize.width = 1024;
				directionalLight.shadow.mapSize.height = 1024;

				directionalLight.shadow.bias = - 0.002;

			}

			function onWindowResize() {

				camera.aspect = window.innerWidth / window.innerHeight;
				camera.updateProjectionMatrix();

				renderer.setSize( window.innerWidth, window.innerHeight );

			}

			function animate() {

				requestAnimationFrame( animate );

				render();
				//stats.update();

			}

			function render() {

				var timer = Date.now() * 0.0005;

				camera.position.x = Math.cos( timer ) * 3;
				camera.position.z = Math.sin( timer ) * 3;

				camera.lookAt( cameraTarget );

				renderer.render( scene, camera );

			}
