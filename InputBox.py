import pygame

pygame.init()


def quickCollide(pos, rect):
    if (
        pos[0] > rect.x
        and pos[0] < rect.x + rect.w
        and pos[1] > rect.y
        and pos[1] < rect.y + rect.h
    ):
        return True
    return False


class inputBox:
    def __init__(self, rect, limit) -> None:

        self.font = pygame.font.Font(None, 32)
        self.input_box = rect
        self.color_inactive = pygame.Color("lightskyblue3")
        self.color_active = pygame.Color("dodgerblue2")
        self.color = self.color_inactive
        self.active = False
        self.text = ""
        self.lines = [""]
        self.limit = limit
        self.maxCD = 100
        self.cd = self.maxCD

    def update_text(self, text, font, box_width):
        words = text.split(" ")
        lines = [""]
        for word in words:
            temp_line = lines[-1] + " " + word if lines[-1] else word
            temp_text = font.render(temp_line, True, self.color)
            if temp_text.get_width() <= box_width:
                lines[-1] = temp_line
            else:
                lines.append(word)
        return lines

    def update(self, mouseState, events,alwaysReturn=True):
        self.cd -=1
        if self.active == True:
            a = 2
        if self.active == False:
            self.color = self.color_inactive
        for event in events:
            if mouseState[0] == True:
                mPos = pygame.mouse.get_pos()
                if quickCollide(mPos, self.input_box) and self.cd < 0:
                    self.active = not self.active
                    self.cd = self.maxCD
                    self.color = self.color_active
                else:
                    self.active = False
                
            if event.type == pygame.KEYDOWN:
                print("KD")
                if self.active == True:
                    print("ACTIVE")
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                        a = self.text
                        self.text = ""
                        self.lines = [""]
                        print(a)
                        return a

                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        print("Text added")
                        if len(self.text) < self.limit:
                            self.text += event.unicode
                            self.text = self.text.upper()
                    self.lines = self.update_text(
                        self.text, self.font, self.input_box.width - 10
                    )
                    text_surface = self.font.render(self.text, True, (0, 0, 0))
                    while text_surface.get_width() > self.input_box.width - 10:
                        # Remove the last character until it fits
                        self.text = self.text[:-1]
                        text_surface = self.font.render(self.text, True, (0, 0, 0))

                    # if len(self.text) > 16:
                    #    self.text = self.text[:-1]
        if alwaysReturn:
            return self.text

    def draw(self, window):
        for i, line in enumerate(self.lines):
            txt_surface = self.font.render(line, True, self.color)
            window.blit(
                txt_surface, (self.input_box.x + 5, self.input_box.y + 5 + i * 32)
            )
        self.input_box.h = max(32, len(self.lines) * 32)
        pygame.draw.rect(window, self.color, self.input_box, 2)
