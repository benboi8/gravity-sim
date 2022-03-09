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
		self.vel = Vec2(0, 0)
		self.acc = Vec2(0, 0)

		self.static = False

		self.mass = mass

		for key, value in kwargs.items():
			setattr(self, key, value)

		
		if not self.static:
			Attractor.allMovers.append(self)
		Attractor.allAttractors.append(self)

		self.vel = Vec2.Random(-7, 7, -7, 7)

	def Draw(self):
		pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)

	def ApplyForce(self, force):
		self.acc = self.acc.Add(force)

	def Update(self):
		self.vel = self.vel.Add(self.acc)
		pos = self.Add(self.vel)
		self.x, self.y = pos.x, pos.y
		self.acc = Vec2(0, 0)
		
		if 0 - self.radius <= self.x <= width + self.radius and 0 - self.radius <= self.y <= height + self.radius:
			p = ParticleSystem.Particle(self.x, self.y, lifeReduction=10, radius=self.radius+5)
			p.velocity = Vec2(0, 0)

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
		if event.button == 1:
			Attractor(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 10, blue, mass=10)


def Update():
	for a in Attractor.allAttractors:
		for m in Attractor.allMovers:
			a.Attract(m)

	for m in Attractor.allMovers:
		m.Update()

	for p in ParticleSystem.allParticles:
		p.Update()



Vec2.origin = (width // 2, height // 2)
Attractor(width // 2, height // 2, 10, yellow, 20, static=True)

for i in range(1):
	Attractor(randint(0, width), randint(0, height), 10, blue, mass=10)


while running:
	clock.tick_busy_loop(fps)
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
