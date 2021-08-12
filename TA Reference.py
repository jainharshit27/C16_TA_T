import pygame, pymunk
import pymunk.pygame_util

class Arrow:
    def __init__(self,x,y):
        vs = [(-80, 0), (0, 2), (2, 0), (0, -2)]
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Poly(self.body, vs)
        self.shape.collision_type = 1
        self.shape.density = 0.1
        self.body.position = x,y
        space.add(self.body, self.shape)
    
    def power(self, start, end):
        diff = end - start
        power = min(diff, 1000) * 13.5
        impulse = (power*1, 0)
        self.body.body_type = pymunk.Body.DYNAMIC
        self.body.apply_impulse_at_world_point(impulse, self.body.position)
    
class Target:
    def __init__(self):
        vs = [(1, -80), (1, 80), (-1, 80), (-1, -80)]
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.shape = pymunk.Poly(self.body, vs)
        self.body.position = 600,400
        space.add(self.body, self.shape)
    
    def draw(self, image):
        screen.blit(rope_img, (round(self.body.position.x-85), 0))
        screen.blit(rope_img, (round(self.body.position.x-70), 0))
        screen.blit(image, (round(self.body.position.x-15), round(self.body.position.y-80)))
    
def powerbar(ticks):
    current_time = pygame.time.get_ticks()
    diff = current_time - start_time
    power = min(diff, 1000)
    h = power / 2
    pygame.draw.line(screen, pygame.Color("red"), (650, 550), (650, 550 - h), 10)

def post_solve_arrow_hit(arbiter, space, data):
    a, b = arbiter.shapes
    position = arbiter.contact_point_set.points[0].point_a
    add_to_score(position[1])
    if position[0] == 599.0:
        b.collision_type = 0
        b.group = 1
        target_body = a.body
        arrow_body = b.body
        pivot_joint = pymunk.PivotJoint(arrow_body, target_body, position)
        phase = target_body.angle - arrow_body.angle
        gear_joint = pymunk.GearJoint(arrow_body, target_body, phase, 0.1)
        space.add(pivot_joint)
        space.add(gear_joint)

def add_to_score(position):
    global score
    if position > 320 and position <= 370:
        score += 10
    elif position > 370 and position <= 430:
        score += 20
    elif position > 430 and position <= 480:
        score += 10

pygame.init()

height = 600
width = 690
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

score = 0
score_font = pygame.font.Font("freesansbold.ttf", 16)

#pymunk space
gravity = 1000
wind = 200
space = pymunk.Space()
space.gravity = wind, gravity
draw_options = pymunk.pygame_util.DrawOptions(screen)
draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES

#background
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (width, height))

#archer
archer = pygame.image.load("bow.png")
archer = pygame.transform.scale(archer, (100,150))

#Target
target = Target()
target_image = pygame.image.load("target.png")
target_image = pygame.transform.scale(target_image, (25,160))
rope_img = pygame.image.load("rope.png")
rope_img = pygame.transform.scale(rope_img, (150,400))

#Arrow
arrow = Arrow(130,85)
flying_arrows = []
handler = space.add_collision_handler(0, 1)
handler.data["flying_arrows"] = flying_arrows
handler.post_solve = post_solve_arrow_hit

while True:
    screen.blit(bg, (0,0))
    screen.blit(archer, (25,40))
    
    if len(flying_arrows) == 5:
        screen.fill((255,255,255))
        score_show = score_font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(score_show, (250,300))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                start_time = pygame.time.get_ticks()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                end_time = pygame.time.get_ticks()
            
                arrow.power(start_time, end_time)
                flying_arrows.append(arrow.body)
                
                arrow = Arrow(130,85)
                
    if pygame.mouse.get_pressed()[0]:
        powerbar(pygame.time.get_ticks())
        
    space.debug_draw(draw_options)
    
    target.draw(target_image)
    score_show = score_font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_show, (600,10))
    
    #space reload
    space.step(1/60)
    pygame.display.update()
    clock.tick(60)