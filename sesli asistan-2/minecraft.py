from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController



chosenBlock = 1

def update():
    global chosenBlock

    if held_keys['1']:
        chosenBlock = 1
        print("Beyaz küp seçildi")
    if held_keys['2']:
        chosenBlock = 2
        print("Çimen seçildi")
    if held_keys['3']:
        chosenBlock = 3
        print("Taş seçildi")
    if held_keys['4']:
        chosenBlock = 4
        print("parke taşı")
    if held_keys['5']:
        chosenBlock=5
        print("odun")
    if held_keys['6']:
        chosenBlock=6
        print("yaprak")
    if held_keys['7']:
        chosenBlock=7
        print("cam blok seçildi")
    if held_keys['8']:
        chosenBlock=8
        print('kaya seçildi')
class Gokyuzu(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture='sky_default',
            double_sided=True,
            scale=150,
        )

class Block(Button):
    def __init__(self, position=(0,0,0), texture ='grass'):
             super().__init__(
                parent = scene,
                position = position,
                model = 'cube',
                texture = texture,
                color =  color.color(0, 0, random.uniform(0.9, 1)),
                origin_y = .5,

             )

    def input(self,key):
        if self.hovered:
            if key == 'right mouse down':
                if chosenBlock == 1:
                    block = Block(position = self.position + mouse.normal,texture='white_cube')
                elif chosenBlock == 2:
                    block = Block(position=self.position + mouse.normal, texture='grass')
                elif chosenBlock == 3:
                    block = Block(position=self.position + mouse.normal, texture='brick')
                elif chosenBlock == 4:
                    block = Block(position=self.position + mouse.normal, texture='tuğla.png')
                elif chosenBlock == 5:
                    block = Block(position=self.position + mouse.normal, texture='odun.jpg')
                elif chosenBlock == 6:
                    block = Block(position=self.position + mouse.normal, texture='yaprak.jpg')
                elif chosenBlock==7:
                    block=Block(position=self.position+mouse.normal,texture='cam.png')
                elif chosenBlock==8:
                    block=Block(position=self.position+mouse.normal,texture='kaya.png')

            if key == 'left mouse down':
                destroy(self)

app = Ursina()

player = FirstPersonController()
gokyuzuz=Gokyuzu()


for x in range(25):
    for y in range(25):
        block = Block(position=(x,0,y))
for z in range(10):
    for j in range(10):
        block=Block(position=(z,1,j),texture='kaya.png')

for a in range(8):
    for b in range(8):
        block=Block(position=(a,2,b),texture='kaya.png')
for t in range(6):
    for e in range(6):
        block=Block(position=(t,3,e),texture='kaya.png')

app.run()
