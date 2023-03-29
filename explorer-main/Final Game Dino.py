import pygame
import os
import random
import pickle
pygame.init()
points = 0
# run = False
basicFont = pygame.font.Font('freesansbold.ttf', 18)

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()

# Global Constants
SCREEN_HEIGHT = 850
SCREEN_WIDTH = 1600

font = pygame.font.Font('freesansbold.ttf', 20)

LEADERBOARDENTRIES = 10
leaderboard = open("leaderboard.txt", "r")
leaderboardValues = []

leaderboardScores = []
leaderboardNames = []


leaderboard = open("leaderboard.txt", "r")
leaderboardValues = []
for i in range(LEADERBOARDENTRIES*2):
    leaderboardValues.insert(100000000, leaderboard.readline())
for i in range(LEADERBOARDENTRIES):
    leaderboardScores.insert(1000000000000, int(leaderboardValues[2*i+1][:-1:]))
for i in range(LEADERBOARDENTRIES):
    leaderboardNames.insert(1000000000000, leaderboardValues[2*i][:-1:])
print(leaderboardNames)



def displayLBText():
    leaderboard = open("leaderboard.txt", "r")
    leaderboardValues = []
    for i in range(LEADERBOARDENTRIES*2):
        leaderboardValues.insert(100000000, leaderboard.readline())
    i = -1
    for j in range(LEADERBOARDENTRIES):
        text = ""
        i+=1
        text += leaderboardValues[i][:-1:]
        i+=1
        text += " " + leaderboardValues[i][:-1:]
        text = font.render(text, True, (0, 0, 0))
        score = font.render("Your Score: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200 + j * 30)
        SCREEN.blit(text, textRect)
    return text

def insertNewScoreIntoLB(name, score):
    if score > leaderboardScores[-1]:
        i=0
        while score < leaderboardScores[i]:
            i+=1
        leaderboardNames.insert(i, name)
        del leaderboardNames[-1]
        leaderboardScores.insert(i, score)
        del leaderboardScores[-1]
        leaderboardText = ""
        for i in range(LEADERBOARDENTRIES):
            leaderboardText += leaderboardNames[i] + "\n"
            leaderboardText += str(leaderboardScores[i]) + "\n"
        leaderboardText += " \n"
        f = open("leaderboard.txt", "w")
        f.write(leaderboardText)
        print(leaderboardText)


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Dino", "Robot.png")),
           pygame.image.load(os.path.join("Dino", "Robot.png"))]
JUMPING = pygame.image.load(os.path.join("Dino", "Robot.png"))
DUCKING = [pygame.image.load(os.path.join("Dino", "Robot.png")),
           pygame.image.load(os.path.join("Dino", "Robot.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Cactus", "Cone.png")),
                pygame.image.load(os.path.join("Cactus", "Cone.png")),
                pygame.image.load(os.path.join("Cactus", "Cone.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Cactus", "Cone.png")),
                pygame.image.load(os.path.join("Cactus", "Cone.png")),
                pygame.image.load(os.path.join("Cactus", "Cone.png"))]

BIRD = [pygame.image.load(os.path.join("Bird", "Cube.png")),
        pygame.image.load(os.path.join("Bird", "Cube.png"))]

CLOUD = pygame.image.load(os.path.join("Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.timeSinceJump = 0

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:      
            self.dino_duck = False      
            self.dino_run = False      
            self.dino_jump = True      
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True      
            self.dino_run = False      
            self.dino_jump = False      
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):      
            self.dino_duck = False      
            self.dino_run = True      
            self.dino_jump = False      
        if len (joysticks) > 0: 
            if joysticks[0].get_axis (1) > 0 and not self.dino_jump:
                self.dino_duck = False      
                self.dino_run = False      
                self.dino_jump = True      
            elif joysticks[0].get_axis (1) < 0 and not self.dino_jump:
                self.dino_duck = True      
                self.dino_run = False      
                self.dino_jump = False      
            elif not (self.dino_jump or joysticks[0].get_axis (1) < 0):      
                self.dino_duck = False      
                self.dino_run = True      
                self.dino_jump = False    

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump and self.timeSinceJump > 10:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, (255, 0, 0), self.dino_rect)
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        pygame.draw.rect(SCREEN, (255, 0, 0), self.rect)
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 260
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        pygame.draw.rect(SCREEN, (255, 0, 0), self.rect)
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


clock = pygame.time.Clock()
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    player = Dinosaur()
    player.timeSinceJump+=1
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        clock.tick(300)
        player.timeSinceJump+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()



        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))


        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)
 
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                HighScoreMenu()
                return
                # menu(death_count)

        player.update(userInput)
        player.draw(SCREEN)

        
        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    # global points
    run = True
    while run:
        clock.tick(30)

        
        
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 400))
            text = font.render("Press A to Start", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
        elif death_count > 0:
            SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 440))
            displayLBText()
            score = font.render("Your Score: " + str(points) + ". Press A to restart.", True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
            SCREEN.blit(score, scoreRect)
            name = font.render("Team Number: " + user_name, True, (0, 0, 0))
            nameRect = score.get_rect()
            nameRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150)
            SCREEN.blit(name, nameRect)

        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
            if event.type == pygame.KEYDOWN and death_count > 0 and points > leaderboardScores[-1]:
                if event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                elif event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER:
                    user_name += event.unicode
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and death_count != 0:
                    insertNewScoreIntoLB(user_name, points)
                    main()
                elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER):
                    main()


class HighScoreMenu:
    def __init__(self):
        self.score = points
        self.indexes = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
        self.timer = 30

        
        try:
            with open("High_Scores.txt", "rb") as f:
                self.highscores = pickle.load(f)
                f.close()
        except:
            self.highscores = ["aaaa", 10, "bbbb", 8, "cccc", 6, "dddd", 4, "eeee", 2, "aaaa", 10, "bbbb", 8, "cccc", 6, "dddd", 4, "eeee", 2]

        self.modifyHighscores()
        self.loop()

    def loop(self):

        while True:
            self.timer -= 1
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    return
                if len (joysticks) > 0:
                    if self.joystick.get_button(2) and self.timer <= 0:
                        return
            text = basicFont.render(str(self.highscores[0]) + " : " + str(self.highscores[1]), True, pygame.Color("cyan"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*4/16))
            text = basicFont.render(str(self.highscores[2]) + " : " + str(self.highscores[3]), True, pygame.Color("snow"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*5/16))
            text = basicFont.render(str(self.highscores[4]) + " : " + str(self.highscores[5]), True, pygame.Color("NavyBlue"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*6/16))
            text = basicFont.render(str(self.highscores[6]) + " : " + str(self.highscores[7]), True, pygame.Color("darkorange"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*7/16))
            text = basicFont.render(str(self.highscores[8]) + " : " + str(self.highscores[9]), True, pygame.Color("aquamarine"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*8/16))
            text = basicFont.render(str(self.highscores[10]) + " : " + str(self.highscores[11]), True, pygame.Color("lightseagreen"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*9/16))
            text = basicFont.render(str(self.highscores[12]) + " : " + str(self.highscores[13]), True, pygame.Color("lightslateblue"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*10/16))
            text = basicFont.render(str(self.highscores[14]) + " : " + str(self.highscores[15]), True, pygame.Color("blueviolet"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*11/16))
            text = basicFont.render(str(self.highscores[16]) + " : " + str(self.highscores[17]), True, pygame.Color("deeppink"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*12/16))
            text = basicFont.render(str(self.highscores[18]) + " : " + str(self.highscores[19]), True, pygame.Color("gold"))
            SCREEN.blit(text,(SCREEN_WIDTH/4, SCREEN_HEIGHT*13/16))
            text = basicFont.render("Your Score:   " + str(self.score), True, pygame.Color("magenta"))
            SCREEN.blit(text,(SCREEN_WIDTH/8, 100))
            pygame.display.update()
            SCREEN.fill(pygame.Color("black"))

    def modifyHighscores(self):
        for x in self.indexes:
            if self.score > self.highscores[x]:
                playerName = self.findPlayerName()
                self.highscores.insert((x-1), playerName)
                self.highscores.insert(((x)), self.score)
                del self.highscores[10]
                del self.highscores[10]
                with open("High_Scores.txt", "wb") as f:
                    f.truncate(0)
                    pickle.dump(self.highscores, f, pickle.HIGHEST_PROTOCOL)
                    f.close()
                for x in self.highscores:
                    print(x)
                break

    def findPlayerName(self):
        self.done = False
        self.initTimer = 20
        self.letters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " "]
        self.letter1 = self.letter2 = self.letter3 = self.letter4 = self.letters
        self.numpos1 = self.numpos2 = self.numpos3 = self.numpos4 = 0
        self.cursorpos = 0
        self.name = [self.letter1, self.letter2, self.letter3, self.letter4]
        while not self.done:
            self.initTimer -= 1
            self.eventHandler()


            self.name = "".join([str(self.letter1[self.numpos1]), str(self.letter2[self.numpos2]), str(self.letter3[self.numpos3]), str(self.letter4[self.numpos4])])
            rect=(80+self.cursorpos*140, 150, 130, 200)
            pygame.draw.rect(SCREEN, pygame.Color("grey"), rect)
            text = basicFont.render(str(self.letter1[self.numpos1]), True, pygame.Color("red"))
            SCREEN.blit(text,(80, SCREEN_HEIGHT*3/14))
            text = basicFont.render(str(self.letter2[self.numpos2]), True, pygame.Color("red"))
            SCREEN.blit(text,(220, SCREEN_HEIGHT*3/14))
            text = basicFont.render(str(self.letter3[self.numpos3]), True, pygame.Color("red"))
            SCREEN.blit(text,(360, SCREEN_HEIGHT*3/14))
            text = basicFont.render(str(self.letter4[self.numpos4]), True, pygame.Color("red"))
            SCREEN.blit(text,(500, SCREEN_HEIGHT*3/14))
            pygame.display.update()
            SCREEN.fill(pygame.Color("black"))
        self.name = "".join([str(self.letter1[self.numpos1]), str(self.letter2[self.numpos2]), str(self.letter3[self.numpos3]), str(self.letter4[self.numpos4])])
        print(self.name)
        return self.name

    def eventHandler(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.done = True
                if event.key == pygame.K_DOWN:
                    if self.cursorpos == 0:
                        self.numpos1 -= 1
                        if self.numpos1 < 0:
                            self.numpos1 = 10
                    elif self.cursorpos == 1:
                        self.numpos2 -= 1
                        if self.numpos2 < 0:
                            self.numpos2 = 10
                    elif self.cursorpos == 2:
                        self.numpos3 -= 1
                        if self.numpos3 < 0:
                            self.numpos3 = 10
                    elif self.cursorpos == 3:
                        self.numpos4 -= 1
                        if self.numpos4 < 0:
                            self.numpos4 = 10
                            #name[cursorpos] -= 1
                if event.key == pygame.K_UP:
                    if self.cursorpos == 0:
                        self.numpos1 += 1
                        if self.numpos1 > 10:
                            self.numpos1 = 0
                    elif self.cursorpos == 1:
                        self.numpos2 += 1
                        if self.numpos2 > 10:
                            self.numpos2 = 0
                    elif self.cursorpos == 2:
                        self.numpos3 += 1
                        if self.numpos3 > 10:
                            self.numpos3 = 0
                    elif self.cursorpos == 3:
                        self.numpos4 += 1
                        if self.numpos4 > 10:
                            self.numpos4 = 0
                if event.key == pygame.K_LEFT:
                    self.cursorpos -= 1
                    if self.cursorpos < 0:
                        self.cursorpos = 3
                if event.key == pygame.K_RIGHT:
                    self.cursorpos += 1
                    if self.cursorpos > 3:
                        self.cursorpos = 0
            if event.type == pygame.QUIT:
                pygame.quit()

                
            elif event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(2) and self.initTimer <= 0:
                    self.done = True
            if len (joysticks) > 0:

                if self.joystick.get_axis(0) > 0 and self.initTimer <= 0:
                    self.initTimer = 15
                    self.cursorpos -= 1
                    if self.cursorpos < 0:
                        self.cursorpos = 3
                if self.joystick.get_axis(0) < 0 and self.initTimer <= 0:
                    self.initTimer = 15
                    self.cursorpos += 1
                    if self.cursorpos > 3:
                        self.cursorpos = 0
                if self.joystick.get_axis(1) < 0 and self.initTimer <= 0:
                    self.initTimer = 15
                    if self.cursorpos == 0:
                        self.numpos1 -= 1
                        if self.numpos1 < 0:
                            self.numpos1 = 10
                    elif self.cursorpos == 1:
                        self.numpos2 -= 1
                        if self.numpos2 < 0:
                            self.numpos2 = 10
                    elif self.cursorpos == 2:
                        self.numpos3 -= 1
                        if self.numpos3 < 0:
                            self.numpos3 = 10
                    elif self.cursorpos == 3:
                        self.numpos4 -= 1
                        if self.numpos4 < 0:
                            self.numpos4 = 10
                if self.joystick.get_axis(1) > 0 and self.initTimer <= 0:
                    self.initTimer = 15
                    if self.cursorpos == 0:
                        self.numpos1 += 1
                        if self.numpos1 > 10:
                            self.numpos1 = 0
                    elif self.cursorpos == 1:
                        self.numpos2 += 1
                        if self.numpos2 > 10:
                            self.numpos2 = 0
                    elif self.cursorpos == 2:
                        self.numpos3 += 1
                        if self.numpos3 > 10:
                            self.numpos3 = 0
                    elif self.cursorpos == 3:
                        self.numpos4 += 1
                        if self.numpos4 > 10:
                            self.numpos4 = 0

menu(death_count=0)
