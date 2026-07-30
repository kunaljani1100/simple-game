from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.model = self.loader.loadModel("models/box")
        self.model.reparentTo(self.render)
        self.model.setPos(0, 10, 0)

        # Movement direction
        self.movement = [0, 0, 0]

        # Bind key press and release events
        self.accept("arrow_up", self.set_movement, [0, 0.1, 0])
        self.accept("arrow_up-up", self.set_movement, [0, 0, 0])
        self.accept("arrow_down", self.set_movement, [0, -0.1, 0])
        self.accept("arrow_down-up", self.set_movement, [0, 0, 0])
        self.accept("arrow_left", self.set_movement, [-0.1, 0, 0])
        self.accept("arrow_left-up", self.set_movement, [0, 0, 0])
        self.accept("arrow_right", self.set_movement, [0.1, 0, 0])
        self.accept("arrow_right-up", self.set_movement, [0, 0, 0])

        # Add update task
        self.taskMgr.add(self.update, "update")

    def set_movement(self, dx, dy, dz):
        self.movement = [dx, dy, dz]

    def update(self, task):
        # Update the cube's position based on movement
        x, y, z = self.model.getPos()
        self.model.setPos(x + self.movement[0], y + self.movement[1], z + self.movement[2])
        return Task.cont

Game().run()