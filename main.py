from random import randint, choice as randch

import pygame.draw

from BulletsHolder import BulletsHolder
from ChickenHolder import ChicksHolder
from Player import Player
from ab import Node, expectiminimax, alphabeta
from sources import *

pygame.font.init()

pygame.display.set_caption('Space Chicken')
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def collide(chicks, bulls):
    for bul in bulls:
        for chick in chicks:
            offset = (bul.x-chick.x-4 ,  bul.y-chick.y )
            if chick.mask.overlap(bul.mask, offset) is not None:
                return chick, bul
    return False


def collide_egg(obj1, obj2):
    offset_x = -obj1.x + obj2.x + 5
    offset_y = -obj1.y + obj2.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) is not None


def game_over(score):
    global start_time
    print("--- %s seconds ---" % (time.time() - start_time))
    write_to_csv('lose', "%s s" % (time.time() - start_time), get_score(), 'emm')
    main_font = pygame.font.SysFont('arialms', FONT)
    
    def update_window():
        
        WIN.blit(SPACE_IMG, (0, 0))
        
        pause_label = main_font.render('YOU LOST', 1, (255, 255, 255), )
        pause_label2 = main_font.render(f'YOUR SCORE IS: {get_score()}', 1, (255, 255, 255), )
        pause_label3 = main_font.render('PRESS SPACE TO TRY AGAIN', 1, (255, 255, 255), )
        pause_label4 = main_font.render('PRESS ESC TO QUIT', 1, (255, 255, 255), )
        WIN.blit(pause_label,
                 (WIDTH / 2 - pause_label.get_width() / 2, HEIGHT / 2 - pause_label.get_height() / 2 - 60 - 30,))
        WIN.blit(pause_label2,
                 (WIDTH / 2 - pause_label2.get_width() / 2, HEIGHT / 2 - pause_label2.get_height() / 2 - 30,))
        WIN.blit(pause_label3,
                 (WIDTH / 2 - pause_label3.get_width() / 2, HEIGHT / 2 - pause_label3.get_height() / 2 + 30,))
        WIN.blit(pause_label4,
                 (WIDTH / 2 - pause_label4.get_width() / 2, HEIGHT / 2 - pause_label4.get_height() / 2 + 60 * 2,))
        
        pygame.display.update()
    
    while 1:
        update_window()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    start_time = time.time()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit('quit from gameover menu')


def main():
    global serach_method
    paused = False
    run = True
    set_score(0)
    lives = 10
    main_font = pygame.font.SysFont('arialms', 50)
    player = Player(WIDTH / 2 - SHIP_IMG.get_width() / 2, 700 - 400, lives)
    print(player.mask.outline())
    
    chicks = ChicksHolder()
    bulls = BulletsHolder()
    clock = pygame.time.Clock()
    
    def update_window():
        bulls.create_laser(player.x+int(player.image.get_width()/2),player.y+int(player.image.get_height()/2),)
        WIN.blit(SPACE_IMG, (0, 0))
        lives_text = main_font.render('♥' * lives, 1, (255, 0, 0))
        score_text = main_font.render(f'{get_score()}', 1, (255, 255, 255))
        WIN.blit(lives_text, (WIDTH - lives_text.get_width() - 5, 5))
        WIN.blit(score_text, (5, 5))
        
        bulls.draw_all_bullets(WIN)
        chicks.draw_all(WIN)
        
        player.draw(WIN)
        
        for i in player.mask.outline():
            # print(player.mask.outline())
            tetet = (i[0] + int(player.x), i[1] + int(player.y))
            WIN.set_at(tetet, (255, 0, 0))
        
        # import time
        # start_time = time.time()

    
    while run:
        if len(chicks.chicks) == 0:
            chicks.set_chicks()
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit('player quit')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bulls.create_laser(player.x + player.image.get_width() / 2, player.y)
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    print(('resumed', 'paused')[paused])
                if event.key == pygame.K_z:
                    serach_method = snext(serach_method)
                    print(serach_method)
        
        if paused:
            pause_label = main_font.render('paused...', 1, (255, 255, 255), )
            pause_label2 = main_font.render('press ESC to resume', 1, (255, 255, 255), )
            WIN.blit(pause_label, (WIDTH / 2 - pause_label.get_width() / 2, HEIGHT / 2 - pause_label.get_height() / 2,))
            WIN.blit(pause_label2,
                     (WIDTH / 2 - pause_label2.get_width() / 2, HEIGHT / 2 - pause_label2.get_height() / 2 + 60,))
            
            # search(WIN,player,chicks.chicks,bulls.bullets)
            pygame.display.update()
            # paused=False
            # quit(0)
            continue
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player.x - 1 > 0:
                player.x -= player.velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player.x + player.image.get_width()+player.velocity < WIDTH:
                player.x += player.velocity
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.y + player.image.get_height()+player.velocity+5 < HEIGHT:
            player.y += player.velocity
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.y -player.velocity-5 >0:
            player.y -= player.velocity
        # max eggs
        if len(bulls.bullets) < 5:
            rand_koef = randint(0, 700)
            if rand_koef > 680:
                rand_chick = randch(chicks.chicks)
                bulls.create_egg(rand_chick.x, rand_chick.y)
        
        kurkaIlaser = collide(chicks.chicks, bulls.lasers)
        
        if kurkaIlaser:
            print(kurkaIlaser[0].lives, kurkaIlaser[0].type)
            if kurkaIlaser[0].lives == 1:
                inc_score(100 if kurkaIlaser[0].type == 'yellow' else 200 if kurkaIlaser[0].type == 'blue' else 300 if kurkaIlaser[0].type == 'red' else 0)
                print(kurkaIlaser[0].type)
                try:
                    bulls.lasers.pop(bulls.lasers.index(kurkaIlaser[1]))
                    chicks.chicks.pop(chicks.chicks.index(kurkaIlaser[0]))
                except ValueError:
                    print('err')
            else:
                kurkaIlaser[0].lives -= 1
                bulls.lasers.pop(bulls.lasers.index(kurkaIlaser[1]))
                continue
        
        for egg in bulls.bullets:
            if collide_egg(egg, player):
                lives -= 1
                if lives == 0:
                    game_over(get_score())
                try:
                    bulls.bullets.pop(bulls.bullets.index(egg))
                except ValueError:
                    print('err')
        # result_of_search = search(WIN, player, chicks.chicks, bulls.bullets, serach_method)
        # from ab import alphabeta
        # (alpha_beta_result, direction) = alphabeta(Node(player,chicks,bulls,''),depth_recurtion,-float('inf'),float('inf'),True)
        (alpha_beta_result, direction) = expectiminimax(Node(player,chicks,bulls,''),depth_recurtion,True)
        # print(alpha_beta_result,direction.move)
        dirs={"<":(-8,0),">":(8,0),'':(0,0),'↑':(0, -8), '↓':(0, 8)}
        ## move player in direction
        # for i in result_of_search:
        #     for j in i:
        #         WIN.set_at(j,(255,255,255))
        # move to target
        
        player.x+=dirs[direction.move][0]
        # useless
        # player.y+=dirs[direction.move][1]
        
        
        pygame.display.update()
        chicks.move(bulls)
        bulls.move_all()
        update_window()


main()
