import pygame
import random

pygame.init()



class Apple:
    def __init__(self, display):
        self.x_pos = 0
        self.y_pos = 0

        self.display = display

        self.randomize()

    def randomize(self):
        height = Config['game']['height']
        width = Config['game']['width']
        bumper = Config['game']['bumper_size']

        max_x = (height - bumper - Config['snake']['width'])
        max_y = (height - bumper - Config['snake']['height']) 
        
        self.x_pos = random.randint(bumper, max_x)
        self.y_pos = random.randint(bumper, max_y)

    def draw(self):
        return pygame.draw.rect(
            self.display, 
            Config['colors']['red'],
            [
                self.x_pos,
                self.y_pos,
                Config['apple']['height'],
                Config['apple']['width']
            ]
        )

Config = {
    'game': {
        'caption': 'zmeika 2000',
        'height': 600,
        'width': 600,
        'fps': 45,
        'records': [], 
        'bumper_size': 30 #30
    },
    'snake': {
        'height': 20,
        'width': 20,
        'speed': 3
    },
    'apple': {
        'width': 20,
        'height': 20
    },
    'colors': {
        'white': (255, 255, 255),
        'black': (0, 0, 0),
        'green': (0, 0, 150), #0 100 0
        'red': (255, 0, 0) #100 0 0
    }
}



class Game:
    def __init__(self, display):
        self.display = display
        self.score = 0

    def loop(self):
        clock = pygame.time.Clock()
        snake = Snake(self.display)
        apple = Apple(self.display)

        x_change = 0
        y_change = 0
        
        self.score = 0
        
        button = pygame.Rect(575, 6, 20, 20)
        button2 = pygame.Rect(775, 6, 20, 20)
        
        speed1button = pygame.Rect(620, 30 + 50, 150, 20)
        speed2button = pygame.Rect(620, 30 + 80, 150, 20)
        speed3button = pygame.Rect(620, 30 + 110, 150, 20)
        
        sizeborder1button = pygame.Rect(620, 30 + 182, 150, 20)
        sizeborder2button = pygame.Rect(620, 30 + 212, 150, 20)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #exit()
                    pygame.quit()
                    

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -Config['snake']['speed']
                        y_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x_change = Config['snake']['speed']
                        y_change = 0
                    elif event.key == pygame.K_UP:
                        x_change = 0
                        y_change = -Config['snake']['speed']
                    elif event.key == pygame.K_DOWN:
                        x_change = 0
                        y_change = Config['snake']['speed']
                        
                        
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos 
                    
                    if button2.collidepoint(mouse_pos):
                        display = pygame.display.set_mode((
                           600, 
                            Config['game']['height']
                        ))                                            
                        
                    elif button.collidepoint(mouse_pos):
                        display = pygame.display.set_mode((
                           800, 
                            Config['game']['height']
                        ))                        
                        
                    elif speed1button.collidepoint(mouse_pos):
                        Config['snake']['speed'] = 3
                    elif speed2button.collidepoint(mouse_pos):
                        Config['snake']['speed'] = 6
                    elif speed3button.collidepoint(mouse_pos):
                        Config['snake']['speed'] = 10
                        
                    elif sizeborder1button.collidepoint(mouse_pos):
                        Config['game']['bumper_size'] = 110
                        
                    elif sizeborder2button.collidepoint(mouse_pos):
                        Config['game']['bumper_size'] = 30
                    
                    
                                      
                                        
        
           
            
            # заполнение заднего фона, рисование стенки
            self.display.fill(Config['colors']['green'])
            
            pygame.draw.rect(
                self.display, 
                Config['colors']['black'],
                [
                    Config['game']['bumper_size'],
                    Config['game']['bumper_size'],
                    Config['game']['height'] - Config['game']['bumper_size'] * 2,
                    Config['game']['width'] - Config['game']['bumper_size'] * 2
                ]
            )
            
            # рисование яблока
            apple_rect = apple.draw()

            # двигать и перерисовывать змейку
            snake.move(x_change, y_change)
            snake_rect = snake.draw()
            snake.draw_body()

            # замечать столкновения со стенкой
            bumper_x = Config['game']['width'] - Config['game']['bumper_size']
            bumper_y = Config['game']['height'] - Config['game']['bumper_size']

            if (
                snake.x_pos < Config['game']['bumper_size'] or
                snake.y_pos < Config['game']['bumper_size'] or
                snake.x_pos + Config['snake']['width'] > bumper_x or
                snake.y_pos + Config['snake']['height'] > bumper_y
            ):
                ##########
                Config['game']['records'].append(self.score)
                print(Config['game']['records'])
                self.loop()

            # замечать столкновения с яблоком
            if apple_rect.colliderect(snake_rect):
                apple.randomize()
                self.score += 1
                snake.eat()

            # столкновения змейки с самой собой
            if len(snake.body) >= 1:
                for cell in snake.body:
                    if snake.x_pos == cell[0] and snake.y_pos == cell[1]:
                        #############
                        Config['game']['records'].append(self.score)
                        print(Config['game']['records'])
                        self.loop()

            # рисовать заголовок и счёт
            pygame.font.init()
           
            
            font = pygame.font.SysFont("comicsansms", 27)
            
            score_text = 'Счёт: {}'.format(self.score)
            score = font.render(score_text, True, Config['colors']['white'])
            title = font.render('Управляй стелками на клавиатуре', True, Config['colors']['white'])
            
            #####
            settings = font.render('->', True, Config['colors']['white'])
            
            settings2 = font.render('<-', True, Config['colors']['white'])
            speed = font.render('Скорость:', True, Config['colors']['white'])
            speed1 = font.render('медленный', True, Config['colors']['white'])
            speed2 = font.render('средний', True, Config['colors']['white'])
            speed3 = font.render('быстрый', True, Config['colors']['white'])
            
            
            sizeborder = font.render('Размер поля:', True, Config['colors']['white'])
            
            sizeborder1 = font.render('маленький', True, Config['colors']['white'])
                        
            sizeborder2 = font.render('большой', True, Config['colors']['white'])
                     
            records = font.render('Рекорды:', True, Config['colors']['white'])
            
            
            font2 = pygame.font.SysFont("comicsansms", 17)
            
            rules = font2.render('Правила:', True, Config['colors']['white'])
            rules1 = font2.render('ешь красные яблоки', True, Config['colors']['white'])
            rules2 = font2.render('чтобы расти, проигра-', True, Config['colors']['white'])
            rules3 = font2.render('ешь, если столкнёшься ', True, Config['colors']['white'])
            rules4 = font2.render('с самим собой или со', True, Config['colors']['white'])
            rules5 = font2.render('стеной.', True, Config['colors']['white'])
            
            rules_rect = score.get_rect(
                center=(660, 30 + 380))
            rules1_rect = score.get_rect(
                center=(650, 30 + 410))
            rules2_rect = score.get_rect(
                center=(650, 30 + 440))
            rules3_rect = score.get_rect(
                center=(650, 30 + 470))
            rules4_rect = score.get_rect(
                center=(650, 30 + 500)) 
            rules5_rect = score.get_rect(
                center=(650, 30 + 530))             
            
                    
            
            self.display.blit(rules, rules_rect)
            self.display.blit(rules1, rules1_rect)
            self.display.blit(rules2, rules2_rect)
            self.display.blit(rules3, rules3_rect)
            self.display.blit(rules4, rules4_rect)
            self.display.blit(rules5, rules5_rect)
            
            
            if len(Config['game']['records']) > 0:
                records1text = '1: {}'.format(max(Config['game']['records']))
                records1 = font.render(records1text, True, Config['colors']['white'])
                records1_rect = score.get_rect(
                    center=(
                         660, 
                         30 + 290
                    )
                )   
                self.display.blit(records1, records1_rect)                
                if len(Config['game']['records']) > 1:
                    
                       
                    records2text = '2: {}'.format(sorted(Config['game']['records'])[-2])
                    records2= font.render(records2text, True, Config['colors']['white'])                     
                    records2_rect = score.get_rect(
                    center=(
                                660, 
                                30 + 320
                            )
                        )   
                    self.display.blit(records2, records2_rect)
                    if len(Config['game']['records']) > 2:
             
                        records3text = '3: {}'.format(sorted(Config['game']['records'])[-3])
                        records3= font.render(records3text, True, Config['colors']['white'])                     
                        records3_rect = score.get_rect(
                        center=(
                                 660, 
                                 30 + 350
                                )
                            )   
                        self.display.blit(records3, records3_rect)
               
            ########


            title_rect = title.get_rect(
                center=(
                    600 / 2, 
                    Config['game']['bumper_size'] / 2  ####
                )
            )

            score_rect = score.get_rect(
                center=(
                    90, 
                    600 - Config['game']['bumper_size'] / 2
                )
            )
            
            
            #######
            settings_rect = score.get_rect(
                center=(
                  600 , 
                    30 - 20 ##
                )
            )                
            
            settings2_rect = score.get_rect(
                center=(
                     800, 
                    30 - 20
                )
            )   
            
            
            speed_rect = score.get_rect(
                center=(
                     660, 
                     30 + 20
                )
            )               
            
            speed1_rect = score.get_rect(
                center=(
                     670, 
                     30 + 52
                )
            )           
            speed2_rect = score.get_rect(
                center=(
                     670, 
                   30 + 82
                )
            )           
            speed3_rect = score.get_rect(
                center=(
                     670, 
                     30 + 112
                )
            )                       
            
            
            
            sizeborder_rect = score.get_rect(
                center=(
                     660, 
                     30 + 150
                )
            )           
            
            sizeborder1_rect = score.get_rect(
                center=(
                     670, 
                     30 + 182
                )
            )                                   
            sizeborder2_rect = score.get_rect(
                center=(
                     670, 
                     30 + 212
                )
            )                                               
            
            records_rect = score.get_rect(
                center=(
                     660, 
                     30 + 260
                )
            )                  
            
                       
            ######
            

            self.display.blit(score, score_rect)
            self.display.blit(title, title_rect)
            
            self.display.blit(settings, settings_rect)
            self.display.blit(settings2, settings2_rect)
            self.display.blit(speed, speed_rect)
            
            self.display.blit(speed1, speed1_rect)
            self.display.blit(speed2, speed2_rect)
            self.display.blit(speed3, speed3_rect)
            
            
            self.display.blit(sizeborder, sizeborder_rect)
            self.display.blit(sizeborder1, sizeborder1_rect)
            self.display.blit(sizeborder2, sizeborder2_rect)
            
            self.display.blit(records, records_rect)
            ##########################
            pygame.draw.rect(self.display, Config['colors']['white'], (575, 6, 20, 20))
                       
            pygame.draw.rect(self.display, Config['colors']['white'], (775, 6, 20, 20))
            
            
            
            #speed adjust
            #pygame.draw.rect(self.display, Config['colors']['white'], (620, 30 + 182, 150, 20))
            
            
            #pygame.draw.rect(self.display, Config['colors']['white'], (620, 30+ 212, 150, 20))
            
            #pygame.draw.rect(self.display, Config['colors']['green'], (620, Config['game']['bumper_size'] + 110, 150, 20))
            
            ######################
            
            
            
            

            pygame.display.update()
            clock.tick(Config['game']['fps'])

        pygame.quit()
        sys.exit
        
     


class Snake:
    def __init__(self, display):
        self.x_pos = (Config['game']['width'] -30) / 2
        self.y_pos = (Config['game']['height'] - 30) / 2
        self.display = display
        self.body = []
        self.max_size = 0

    def eat(self):
        self.max_size += 10

    def draw(self):
        return pygame.draw.rect(
            self.display, 
            Config['colors']['green'],
            [
                self.x_pos,
                self.y_pos,
                Config['snake']['height'],
                Config['snake']['width']
            ]
        )

    def draw_body(self):
        for item in self.body:
            pygame.draw.rect(
                self.display, 
                Config['colors']['green'],
                [
                    item[0],
                    item[1],
                    Config['snake']['width'],
                    Config['snake']['height']
                ]
            )

    def move(self, x_change, y_change):
        self.body.append((self.x_pos, self.y_pos))
        self.x_pos += x_change
        self.y_pos += y_change

        if len(self.body) > self.max_size:
            del(self.body[0])
   



        





def main():
    display = pygame.display.set_mode((
        Config['game']['width'], 
        Config['game']['height']
    ))
    pygame.display.set_caption(Config['game']['caption'])
    
    game = Game(display)
    game.loop()

if __name__ == '__main__':
    
    main()
    

