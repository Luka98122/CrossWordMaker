import pygame

pygame.init()


class Button:
    def __init__(self, rect, text, textSize) -> None:
        self.rect = rect
        self.text = text
        self.textSize = textSize
        self.font = pygame.font.Font(None, self.textSize)
        self.text1 = self.font.render(self.text, True, pygame.Color("Black"))
        self.text_rect = self.text1.get_rect(
            center=(
                self.rect.x + self.rect.width / 2,
                self.rect.y + self.rect.height / 2,
            )
        )


    def update(self, mouseB,mousePos):
        if (
            mousePos[0] > self.rect.x
            and mousePos[0] < self.rect.x + self.rect.width
            and mousePos[1] > self.rect.y
            and mousePos[1] < self.rect.y + self.rect.height
            and mouseB[0] == True
        ):
            return True
        return False

    def draw(self, window,activity,color=pygame.Color("Blue")):
        if activity == True:
            pygame.draw.rect(window,color, self.rect)
        window.blit(self.text1, self.text_rect)
