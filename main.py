import os
import sys

os.chdir(sys.path[0])
sys.path.insert(1, "P://Python Projects/assets/")

from GameObjects import *


class Attractor(Vec2):
	allAttractors = []
	allMovers = []

	def __init__(self, x, y, radius, color, mass, **kwargs):
		super().__init__(x, y)
		self.radius = radius
		self.color = color
		self.vel = Vec2.Random(-10, 10, -10, 10)
		self.vel.x = Constrain(self.vel.x, -5, 5)
		self.vel.y = Constrain(self.vel.y, -5, 5)
		self.acc = Vec2(0, 0)

		self.static = False

		self.mass = mass

		for key, value in kwargs.items():
			setattr(self, key, value)
		
		if not self.static:
			Attractor.allMovers.append(self)
			self.vel = Vec2(0, 0)

		Attractor.allAttractors.append(self)


		self.path = []

	def Draw(self):
		# if self.static:
		# pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

		if 0 - self.radius <= self.x <= width + self.radius and 0 - self.radius <= self.y <= height + self.radius:
			p = ParticleSystem.Particle(self.x, self.y, lifeReduction=3, radius=self.radius + 5, img_paths=[(self.color, "textures/particles/soft_1.png")])
			p.velocity = Vec2(0, 0)

			# if not self.static:
				# p = ParticleSystem.Particle(self.x, self.y, lifeReduction=-1, radius=self.radius, img_paths=[(self.color, "textures/particles/soft_1.png")])
				# p.velocity = Vec2(0, 0)
				# ParticleSystem.allParticles.remove(p)
				# p = Point(self.x, self.y, self.color, self.radius, lists=[])
				# self.path.append(p)

		for p in self.path:
			p.Draw()

		if len(self.path) >= 10:
			self.path.pop(0)

	def ApplyForce(self, force):
		self.acc = self.acc.Add(force)

	def Update(self):
		self.vel = self.vel.Add(self.acc)
		pos = self.Add(self.vel)
		self.x, self.y = pos.x, pos.y
		self.acc = Vec2(0, 0)
		
	def Attract(self, mover):
		force = self.Sub(mover)
		distanceSq = Constrain(force.MagnitudeSquared(), 100, 1000)

		g = 1

		try:
			strength = (g * (self.mass * mover.mass)) / distanceSq
		except ZeroDivisionError:
			pass

		force = force.SetMagnitude(strength)
		mover.ApplyForce(force)


def DrawLoop():
	screen.fill(black)

	DrawAllGUIObjects()

	for m in Attractor.allMovers:
		m.Draw()

	for p in ParticleSystem.allParticles:
		p.Draw()

	for a in Attractor.allAttractors:
		a.Draw()

	pg.display.update()


def HandleEvents(event):
	HandleGui(event)

	if event.type == pg.MOUSEBUTTONDOWN:
		if event.button == 3:
			a = Attractor(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 10, RandomColor(), mass=5)
			a.vel = Vec2(0, 4)


def Update():
	for a in Attractor.allAttractors:
		for m in Attractor.allMovers:
			a.Attract(m)

	for m in Attractor.allMovers:
		m.Update()

	for p in ParticleSystem.allParticles:
		p.Update()


Vec2.origin = (width // 2, height // 2)
Attractor(width // 2, height // 2, 10, yellow, mass=50, static=True)


# for i in range(0):
# 	minM, maxM = 5, 10
# 	m = randint(minM, maxM)
# 	Attractor(randint(0, width), randint(0, height), 10, (Map(m, minM, maxM, 100, 255), Map(m, minM, maxM, 100, 255), Map(m, minM, maxM, 100, 255)), mass=m)

# for i in range(10):
# 	minM, maxM = 5, 10
# 	m = 10
# 	a = Attractor(i * 10, height // 2, 10, RandomColor(), mass=m)
# 	a.vel = Vec2(0, i + 1)
# 	Attractor.allAttractors.remove(a)


displacement = 300
startV = 4
mass = 2
a1 = Attractor(width // 2 + displacement, height // 2, 10, red, mass=mass)
a1.vel = Vec2(0, startV + randint(0, 10) / 10)
a2 = Attractor(width // 2 - displacement, height // 2, 10, green, mass=mass)
a2.vel = Vec2(0, -startV + randint(0, 10) / 10)
a3 = Attractor(width // 2, height // 2 + displacement, 10, blue, mass=mass)
a3.vel = Vec2(-startV + randint(0, 10) / 10, 0)
a4 = Attractor(width // 2, height // 2 - displacement, 10, white, mass=mass)
a4.vel = Vec2(startV + randint(0, 10) / 10, 0)


# x = 40
# for i in range(x):
# 	i = radians(Map(i, 0, x, 0, 360))
# 	a4 = Attractor(width // 2 + (displacement * cos(i)), height // 2 + (displacement * sin(i)), 10, white if i == 0 else red, mass=mass)
# 	a4.vel = Vec2(-cos(i + radians(90)) * startV, -sin(i + radians(90)) * startV)



fps = 60
fpsLbl = Label((0, 0, 100, 50), (lightBlack, darkWhite), str(fps), textData={"fontSize": 12, "alignText": "left-top", "fontColor": white}, drawData={"drawBackground": False, "drawBorder": False})

while running:
	clock.tick_busy_loop(fps)
	fpsLbl.UpdateText(f"{round(clock.get_fps())}")

	deltaTime = clock.get_time()
	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

		HandleEvents(event)

	Update()

	DrawLoop()
