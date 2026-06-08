import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

const foodDatabase = {
  apple: { name: 'Apple', calories: 95, protein: '0.5g', carbs: '25g', fat: '0.3g', fiber: '4g', color: '#ff3333' },
  banana: { name: 'Banana', calories: 105, protein: '1.3g', carbs: '27g', fat: '0.4g', fiber: '3g', color: '#ffeb3b' },
  orange: { name: 'Orange', calories: 62, protein: '1.2g', carbs: '15g', fat: '0.2g', fiber: '3g', color: '#ff9800' },
  burger: { name: 'Burger', calories: 540, protein: '25g', carbs: '45g', fat: '25g', fiber: '2g', color: '#8b4513' },
  pizza: { name: 'Pizza Slice', calories: 285, protein: '12g', carbs: '36g', fat: '10g', fiber: '2g', color: '#ffd700' },
  salad: { name: 'Salad Bowl', calories: 150, protein: '8g', carbs: '12g', fat: '8g', fiber: '5g', color: '#4caf50' }
};

export default function ScanMyBhojan() {
  const mountRef = useRef(null);
  const [selectedFood, setSelectedFood] = useState(null);
  const [showNutrition, setShowNutrition] = useState(false);

  useEffect(() => {
    if (!mountRef.current) return;

    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0xffffff, 10, 50);
    scene.background = new THREE.Color(0xfafafa);

    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 8, 12);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    mountRef.current.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 7);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    const pointLight = new THREE.PointLight(0xffffff, 0.5);
    pointLight.position.set(-5, 5, 5);
    scene.add(pointLight);

    // Plate
    const plateGeometry = new THREE.CylinderGeometry(3, 3, 0.3, 64);
    const plateMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xffffff, 
      roughness: 0.2, 
      metalness: 0.1 
    });
    const plate = new THREE.Mesh(plateGeometry, plateMaterial);
    plate.position.y = 0;
    plate.castShadow = true;
    plate.receiveShadow = true;
    scene.add(plate);

    // Plate rim
    const rimGeometry = new THREE.TorusGeometry(3, 0.15, 32, 100);
    const rimMaterial = new THREE.MeshStandardMaterial({ color: 0xe0e0e0, roughness: 0.3 });
    const rim = new THREE.Mesh(rimGeometry, rimMaterial);
    rim.position.y = 0.15;
    rim.rotation.x = Math.PI / 2;
    scene.add(rim);

    // Ground plane for shadows
    const groundGeometry = new THREE.PlaneGeometry(50, 50);
    const groundMaterial = new THREE.ShadowMaterial({ opacity: 0.1 });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.5;
    ground.receiveShadow = true;
    scene.add(ground);

    const foodItems = [];
    const foodPhysics = [];

    // Create Apple
    const appleGroup = new THREE.Group();
    const appleGeometry = new THREE.SphereGeometry(0.6, 64, 64);
    const appleMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xff3333, 
      roughness: 0.4, 
      metalness: 0.1 
    });
    const apple = new THREE.Mesh(appleGeometry, appleMaterial);
    apple.castShadow = true;
    
    const stemGeometry = new THREE.CylinderGeometry(0.03, 0.03, 0.4, 16);
    const stemMaterial = new THREE.MeshStandardMaterial({ color: 0x4a2511 });
    const stem = new THREE.Mesh(stemGeometry, stemMaterial);
    stem.position.y = 0.8;
    
    const leafGeometry = new THREE.SphereGeometry(0.15, 16, 16);
    leafGeometry.scale(1.5, 0.5, 0.8);
    const leafMaterial = new THREE.MeshStandardMaterial({ color: 0x228b22 });
    const leaf = new THREE.Mesh(leafGeometry, leafMaterial);
    leaf.position.set(0.1, 0.9, 0);
    leaf.rotation.z = Math.PI / 6;
    
    appleGroup.add(apple);
    appleGroup.add(stem);
    appleGroup.add(leaf);
    appleGroup.position.set(-4, 3, 2);
    appleGroup.userData.foodType = 'apple';
    scene.add(appleGroup);
    foodItems.push(appleGroup);
    foodPhysics.push({ velocity: new THREE.Vector3(0, 0, 0), mass: 1, dragging: false });

    // Create Banana
    const bananaGroup = new THREE.Group();
    const bananaCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(0.3, -0.1, 0),
      new THREE.Vector3(0.6, -0.15, 0),
      new THREE.Vector3(0.9, -0.1, 0),
      new THREE.Vector3(1.2, 0, 0)
    ]);
    const bananaGeometry = new THREE.TubeGeometry(bananaCurve, 64, 0.25, 32, false);
    const bananaMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xffeb3b, 
      roughness: 0.5 
    });
    const banana = new THREE.Mesh(bananaGeometry, bananaMaterial);
    banana.castShadow = true;
    bananaGroup.add(banana);
    bananaGroup.position.set(4, 4, -1);
    bananaGroup.rotation.z = Math.PI / 4;
    bananaGroup.userData.foodType = 'banana';
    scene.add(bananaGroup);
    foodItems.push(bananaGroup);
    foodPhysics.push({ velocity: new THREE.Vector3(0, 0, 0), mass: 1, dragging: false });

    // Create Orange
    const orangeGroup = new THREE.Group();
    const orangeGeometry = new THREE.SphereGeometry(0.65, 64, 64);
    const orangeMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xff9800, 
      roughness: 0.8,
      bumpScale: 0.05
    });
    const orange = new THREE.Mesh(orangeGeometry, orangeMaterial);
    orange.castShadow = true;
    orangeGroup.add(orange);
    orangeGroup.position.set(-2, 5, -3);
    orangeGroup.userData.foodType = 'orange';
    scene.add(orangeGroup);
    foodItems.push(orangeGroup);
    foodPhysics.push({ velocity: new THREE.Vector3(0, 0, 0), mass: 1, dragging: false });

    // Create Burger
    const burgerGroup = new THREE.Group();
    const bunTopGeometry = new THREE.SphereGeometry(0.8, 32, 32, 0, Math.PI * 2, 0, Math.PI / 2);
    const bunMaterial = new THREE.MeshStandardMaterial({ color: 0xdaa520, roughness: 0.6 });
    const bunTop = new THREE.Mesh(bunTopGeometry, bunMaterial);
    bunTop.position.y = 0.5;
    bunTop.castShadow = true;
    
    const pattyGeometry = new THREE.CylinderGeometry(0.75, 0.75, 0.2, 32);
    const pattyMaterial = new THREE.MeshStandardMaterial({ color: 0x4a2511, roughness: 0.7 });
    const patty = new THREE.Mesh(pattyGeometry, pattyMaterial);
    patty.position.y = 0.15;
    patty.castShadow = true;
    
    const cheeseGeometry = new THREE.CylinderGeometry(0.8, 0.8, 0.05, 32);
    const cheeseMaterial = new THREE.MeshStandardMaterial({ color: 0xffd700, roughness: 0.4 });
    const cheese = new THREE.Mesh(cheeseGeometry, cheeseMaterial);
    cheese.position.y = 0.3;
    
    const bunBottomGeometry = new THREE.CylinderGeometry(0.8, 0.8, 0.2, 32);
    const bunBottom = new THREE.Mesh(bunBottomGeometry, bunMaterial);
    bunBottom.position.y = 0;
    bunBottom.castShadow = true;
    
    burgerGroup.add(bunTop, patty, cheese, bunBottom);
    burgerGroup.position.set(2, 4, 3);
    burgerGroup.userData.foodType = 'burger';
    scene.add(burgerGroup);
    foodItems.push(burgerGroup);
    foodPhysics.push({ velocity: new THREE.Vector3(0, 0, 0), mass: 1.5, dragging: false });

    // Create Pizza Slice
    const pizzaGroup = new THREE.Group();
    const pizzaShape = new THREE.Shape();
    pizzaShape.moveTo(0, 0);
    pizzaShape.lineTo(1.5, 0);
    pizzaShape.arc(-1.5, 0, 1.5, 0, Math.PI / 3, false);
    pizzaShape.lineTo(0, 0);
    
    const pizzaGeometry = new THREE.ExtrudeGeometry(pizzaShape, { depth: 0.15, bevelEnabled: false });
    const pizzaMaterial = new THREE.MeshStandardMaterial({ color: 0xffd700, roughness: 0.6 });
    const pizza = new THREE.Mesh(pizzaGeometry, pizzaMaterial);
    pizza.castShadow = true;
    pizza.rotation.x = -Math.PI / 2;
    
    const pepperoniGeometry = new THREE.CylinderGeometry(0.15, 0.15, 0.05, 32);
    const pepperoniMaterial = new THREE.MeshStandardMaterial({ color: 0xff4500 });
    for (let i = 0; i < 3; i++) {
      const pepperoni = new THREE.Mesh(pepperoniGeometry, pepperoniMaterial);
      pepperoni.position.set(0.5 + i * 0.3, 0.2, 0.3);
      pepperoni.rotation.x = Math.PI / 2;
      pizzaGroup.add(pepperoni);
    }
    
    pizzaGroup.add(pizza);
    pizzaGroup.position.set(0, 5, 4);
    pizzaGroup.userData.foodType = 'pizza';
    scene.add(pizzaGroup);
    foodItems.push(pizzaGroup);
    foodPhysics.push({ velocity: new THREE.Vector3(0, 0, 0), mass: 1.2, dragging: false });

    // Create Salad Bowl
    const saladGroup = new THREE.Group();
    const bowlGeometry = new THREE.SphereGeometry(0.7, 32, 32, 0, Math.PI * 2, 0, Math.PI / 1.5);
    const bowlMaterial = new THREE.MeshStandardMaterial({ 
      color: 0xffffff, 
      roughness: 0.2, 
      side: THREE.DoubleSide 
    });
    const bowl = new THREE.Mesh(bowlGeometry, bowlMaterial);
    bowl.castShadow = true;
    
    const lettuceGeometry = new THREE.SphereGeometry(0.3, 16, 16);
    const lettuceMaterial = new THREE.MeshStandardMaterial({ color: 0x4caf50, roughness: 0.8 });
    for (let i = 0; i < 5; i++) {
      const lettuce = new THREE.Mesh(lettuceGeometry, lettuceMaterial);
      const angle = (i / 5) * Math.PI * 2;
      lettuce.position.set(Math.cos(angle) * 0.3, 0.4, Math.sin(angle) * 0.3);
      lettuce.scale.set(0.8 + Math.random() * 0.4, 0.6, 0.8 + Math.random() * 0.4);
      saladGroup.add(lettuce);
    }
    
    saladGroup.add(bowl);
    saladGroup.position.set(-4, 4, -2);
    saladGroup.userData.foodType = 'salad';
    scene.add(saladGroup);
    foodItems.push(saladGroup);
    foodPhysics.push({ velocity: new THREE.Vector3(0, 0, 0), mass: 1, dragging: false });

    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let draggedObject = null;
    let dragPlane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
    let dragOffset = new THREE.Vector3();

    function onMouseDown(event) {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(foodItems, true);

      if (intersects.length > 0) {
        let obj = intersects[0].object;
        while (obj.parent && !foodItems.includes(obj)) {
          obj = obj.parent;
        }
        if (foodItems.includes(obj)) {
          draggedObject = obj;
          const idx = foodItems.indexOf(draggedObject);
          foodPhysics[idx].dragging = true;
          foodPhysics[idx].velocity.set(0, 0, 0);
          
          const planeNormal = new THREE.Vector3(0, 0, 1);
          planeNormal.applyQuaternion(camera.quaternion);
          dragPlane.setFromNormalAndCoplanarPoint(planeNormal, draggedObject.position);
          
          const intersection = new THREE.Vector3();
          raycaster.ray.intersectPlane(dragPlane, intersection);
          dragOffset.copy(draggedObject.position).sub(intersection);
        }
      }
    }

    function onMouseMove(event) {
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

      if (draggedObject) {
        raycaster.setFromCamera(mouse, camera);
        const intersection = new THREE.Vector3();
        raycaster.ray.intersectPlane(dragPlane, intersection);
        draggedObject.position.copy(intersection.add(dragOffset));
      }
    }

    function onMouseUp() {
      if (draggedObject) {
        const idx = foodItems.indexOf(draggedObject);
        foodPhysics[idx].dragging = false;
        
        const distToPlate = draggedObject.position.distanceTo(new THREE.Vector3(0, 0, 0));
        if (distToPlate < 3 && draggedObject.position.y < 2) {
          const foodType = draggedObject.userData.foodType;
          setSelectedFood(foodDatabase[foodType]);
          setShowNutrition(true);
          
          draggedObject.position.y = 0.5;
          draggedObject.position.x = Math.max(-2, Math.min(2, draggedObject.position.x));
          draggedObject.position.z = Math.max(-2, Math.min(2, draggedObject.position.z));
        }
        
        draggedObject = null;
      }
    }

    window.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);

    function animate() {
      requestAnimationFrame(animate);

      foodItems.forEach((food, idx) => {
        const physics = foodPhysics[idx];
        
        if (!physics.dragging) {
          physics.velocity.y -= 0.015 * physics.mass;
          food.position.add(physics.velocity);
          
          if (food.position.y < 0.5) {
            food.position.y = 0.5;
            physics.velocity.y *= -0.4;
            physics.velocity.x *= 0.8;
            physics.velocity.z *= 0.8;
            
            if (Math.abs(physics.velocity.y) < 0.01) {
              physics.velocity.y = 0;
            }
          }
          
          if (food.position.y > 0.5) {
            food.rotation.x += physics.velocity.length() * 0.1;
            food.rotation.z += physics.velocity.length() * 0.05;
          }
        }
      });

      renderer.render(scene, camera);
    }

    animate();

    function handleResize() {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      mountRef.current?.removeChild(renderer.domElement);
    };
  }, []);

  return (
    <div className="relative w-full h-screen overflow-hidden">
      <div ref={mountRef} className="w-full h-full" />
      
      <div className="absolute top-8 left-1/2 transform -translate-x-1/2 z-10">
        <h1 className="text-6xl font-bold text-black tracking-wider" style={{ 
          fontFamily: 'system-ui, -apple-system, sans-serif',
          textShadow: '2px 2px 4px rgba(0,0,0,0.1)'
        }}>
          ScanMyBhojan
        </h1>
      </div>

      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10 text-center">
        <p className="text-black text-lg font-medium opacity-70">
          Drag food items onto the plate to scan nutrition
        </p>
      </div>

      {showNutrition && selectedFood && (
        <div className="fixed inset-0 flex items-center justify-center z-50 p-8" onClick={() => setShowNutrition(false)}>
          <div 
            className="relative p-8 rounded-3xl shadow-2xl max-w-md w-full"
            style={{
              background: 'rgba(255, 255, 255, 0.15)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.3)',
              boxShadow: '0 8px 32px 0 rgba(0, 0, 0, 0.2)'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <button 
              onClick={() => setShowNutrition(false)}
              className="absolute top-4 right-4 text-black text-2xl font-bold hover:text-gray-600 transition-colors"
            >
              ×
            </button>
            
            <div className="text-center mb-6">
              <h2 className="text-4xl font-bold text-black mb-2">{selectedFood.name}</h2>
              <div className="w-20 h-1 bg-black mx-auto rounded-full opacity-30"></div>
            </div>

            <div className="space-y-4">
              <div 
                className="p-6 rounded-2xl text-center"
                style={{
                  background: 'rgba(255, 255, 255, 0.2)',
                  border: '1px solid rgba(255, 255, 255, 0.4)'
                }}
              >
                <div className="text-6xl font-black text-black mb-2">{selectedFood.calories}</div>
                <div className="text-xl font-semibold text-black opacity-70">CALORIES</div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                {[
                  { label: 'Protein', value: selectedFood.protein },
                  { label: 'Carbs', value: selectedFood.carbs },
                  { label: 'Fat', value: selectedFood.fat },
                  { label: 'Fiber', value: selectedFood.fiber }
                ].map((item, idx) => (
                  <div 
                    key={idx}
                    className="p-4 rounded-xl text-center"
                    style={{
                      background: 'rgba(255, 255, 255, 0.15)',
                      border: '1px solid rgba(255, 255, 255, 0.3)'
                    }}
                  >
                    <div className="text-2xl font-bold text-black mb-1">{item.value}</div>
                    <div className="text-sm font-medium text-black opacity-70">{item.label}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-6 text-center">
              <p className="text-sm text-black opacity-50">Click anywhere to close</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}