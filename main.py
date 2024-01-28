from ursina import * 
from ursina.prefabs.first_person_controller import FirstPersonController
from random import randint
from random import uniform
import subprocess
subprocess.call("key.mp3", shell=True)

app = Ursina()
Sky()
ground = Entity(
	model = "plane",
	texture = "assets/esss.jfif",
	collider = "mesh",
	scale = (100,1,100))

player = FirstPersonController(position = (0,2,-5))

wall1 = Entity(
	model = "cube",
	texture = "assets/esss.jfif",
	collider = "cube",
	scale = (100,10,5),
	position = (0,5,50))

wall2 = duplicate(wall1, z=-50)
wall3 = duplicate(wall1, rotation_y=90, x=-50, z=0)
wall4 = duplicate(wall3, x=50)
wall5 = Entity(
	model = "cube",
	texture = "assets/esss.jfif",
	collider = "cube",
	scale = (20,5,0.5),
	position = (0,2,0))

weapon = Entity(
	model = "sphere",
	parent = camera.ui,
	scale = 0.5,
	color=color.gold,
	#texture="white_cube",
	texture="assets/akk47.png",
	position=(1000, 10),
	rotation=(-10,-20,-10))

enemies = []
objects = []
for i in range(10):
	enemy = Entity(
		model = "cube",
		texture = "assets/python.png",
		scale = (2,2,2),
		collider = "box",
		position = (uniform(-45,45), 1, uniform(33,45)))

	asObject=Entity(
		model='assets/python.png',
		collider = "box",
		parent=enemy,
		scale=(2,2,2),
		position = (0,30,0))

	asObject.visiable = False
	enemy.lookAt(player)
	enemy.rotation_x = 27000000
	enemy.rotation_z = 50000000
	enemies.append(enemy)
	objects.append(asObject)

def update():
	if held_keys['left mouse']:
		weapon.position = (0.75, -0.55)
	else:
		weapon.position = (0.8, -0.6)
	if player.y <-5:
		player.y=2
	for enemy in enemies:
		if enemy.visible:
			enemy.lookAt(player)
			enemy.rotation_x = 270
			enemy.rotation_z = 5
			dist = distance(enemy, player)
			if dist > 10:
				diff_x = player.x - enemy.x
				diff_z = player.z - enemy.z
				enemy.x += 0.0001*diff_x
				enemy.z += 0.0001*diff_z

def respawnEnemy(enemy):
	enemy.visible=True

def input(key):
	if key == 'left mouse down':
		for obj, en in zip(objects, enemies):
			if en.hovered:
				en.position = (uniform(-45,45), 1, uniform(33,45))
				en.visible=False
				invoke(respawnEnemy,en,delay=3)
			dust = Entity(model=Circle(),
				parent=camera.ui,
				scale=0.03,
				color=color.yellow,
				position=(0.14,-0.05))
			dust.animate_scale(0.001, duration=.1,curve=curve.linear)
			dust.fade_out(5)

app.run()