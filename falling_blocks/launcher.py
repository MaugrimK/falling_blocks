import pygame

from config import FPS
from controller import GameController

def gameLoop(clock, controller, gameover):
    while not gameover:
        movement = None
        flip = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movement = -1
                if event.key == pygame.K_RIGHT:
                    movement = 1
                if event.key == pygame.K_UP:
                    flip = True

        if not gameover:
            controller.doNextStep(movement, flip)
            pygame.display.flip()

        if controller.isGameOver():
            print('Game Over')
            controller.endGame()
            gameover = True
            pygame.quit()

        clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.set_caption("game_of_blocks")
    clock = pygame.time.Clock()
    #pygame.mixer.init()
    #pygame.mixer.music.load('theme.mp3')
    #pygame.mixer.music.play(0)
    controller = GameController()
    controller.startGame()
    gameover = False
    gameLoop(clock, controller, gameover)
    pygame.quit()

if __name__ == '__main__':
    main()
