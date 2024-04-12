#Thư viện
import pygame 
from pygame.locals import *
import random
pygame.init()

#CHỉnh màu nền
gray = (100,100,100)
green = (76,208,56)
yellow = (255,232,0)
red = (200,0,0)
white = (255,255,255) 

#Tạo cửa sổ game
width = 500
height = 500
screen_size = (width,height)
screen =pygame.display.set_mode(screen_size)
pygame.display.set_caption('GAME ĐUA XE')

#Khởi tạo biến 
gameover = False
speed = 2
speed_change = 1
score = 0
high_score = 0
try:
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    pass

#Vẽ đường xe chạy
road_width = 300   #Độ rộng đường xe chạy
street_width = 10   #Vạch kẻ  đường
street_height = 50

#Các lane đường
lane_left= 150
lane_center= 250
lane_right= 350
lanes= [lane_left,lane_center,lane_right]
lane_move_y= 0

#Đường xe chạy và biên đường
road= (100,0,road_width,height)
left_edge= (95,0,street_width,height)
right_edge= (395,0,street_width,height)

#Vị trí ban đầu 
player_x= 250
player_y= 400

#Đối tượng xe lưu thông
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        #Scale images
        image_scale= 45 / image.get_rect().width
        new_width = image.get_rect().width *image_scale
        new_heigh = image.get_rect().height *image_scale
        self.image = pygame.transform.scale(image,(new_width,new_heigh))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
#Xe người chơi
class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image,x,y)

#Sprite groups
player_group = pygame.sprite.Group()
Vehicle_group = pygame.sprite.Group()

#tạo đối tượng người chơi
player = PlayerVehicle(player_x,player_y)
player_group.add(player)

#Load xe lưu thông vào
image_name = ['pickup_truck.png','semi_trailer.png','taxi.png','van.png']
Vehicle_images = []
for name in image_name:
    image= pygame.image.load('images/' + name)
    Vehicle_images.append(image)
#Load hình va  chạm
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()


#Cài đặt FPS
clock = pygame.time.Clock()
fps = 120
#Vòng lặp xử lý game
running = True
while running:
    #Chỉnh rem hình trên giây
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==QUIT:
            running=False
        #Điều khiển xe:
        if event.type==KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0]>lane_left:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0]<lane_right:
                player.rect.x += 100 
            elif event.key == K_UP:
                speed += speed_change  # Tăng tốc độ từ từ
            elif event.key == K_DOWN:
                speed -= speed_change  # Giảm tốc độ từ từ
            if speed < 1:  # Đảm bảo tốc độ không nhỏ hơn 1
                speed = 1
        #Check va chạm khi điều khiển
        for vehicle in Vehicle_group:
            if pygame.sprite.collide_rect(player,vehicle):
                gameover= True   
                crash_rect.center = [player.rect.center[0],player.rect.top] #Tạo hình vụ va chạm
    #Check va chạm khi đưng yên
    if pygame.sprite.spritecollide(player,Vehicle_group,True):
        gameover =True
    #Vẽ nền địa hình cỏ
    screen.fill(green )
    #Vẽ đường chạy(Road)
    pygame.draw.rect(screen,gray,road)
    #Vẽ biên đường (Edge)
    pygame.draw.rect(screen,yellow,left_edge)
    pygame.draw.rect(screen,yellow,right_edge)
    #Vẽ lane đường 
    lane_move_y += speed* 2
    if lane_move_y >= street_height *2:
        lane_move_y= 0
    for y  in range(street_height * -2,height,street_height * 2):
        pygame.draw.rect(screen,white,(lane_left + 45,y + lane_move_y,street_width,street_height))
        pygame.draw.rect(screen,white,(lane_center + 45,y + lane_move_y,street_width,street_height))
    #Vẽ xe player
    player_group.draw(screen)
    #Vẽ phương tiện gt
    if len(Vehicle_group) < 3 :
        add_verhicle = True
        for verhicle in Vehicle_group:
            if verhicle.rect.top < verhicle.rect.height * 1:
                add_verhicle = False
        if add_verhicle:
            lane= random.choice(lanes)
            image= random.choice(Vehicle_images)
            verhicle=Vehicle(image,lane,height / -3)
            Vehicle_group.add(verhicle)
    #Cho xe công cộng chạy
    for vehicle in Vehicle_group:
        vehicle.rect.y += speed

        #Remove verhicle
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1

    #Vẽ nhóm xe lưu thông
    Vehicle_group.draw(screen)
    #Hiển thị điểm
    font= pygame.font.Font(pygame.font.get_default_font(),16)
    text= font.render(f'Socre: {score}',True,white)
    text_rect= text.get_rect()
    text_rect.center= (50,40)
    screen.blit(text,text_rect)
    # Hiển thị điểm cao nhất
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    high_score_text = font.render(f"High Score: {high_score}", True, white)
    high_score_rect = high_score_text.get_rect()
    high_score_rect.center = (50,70)
    screen.blit(high_score_text, high_score_rect)
    #Ktr game over
    if gameover:
        screen.blit(crash,crash_rect)
        pygame.draw.rect(screen,red,(0,50,width,100))
        font= pygame.font.Font(pygame.font.get_default_font(),16)
        text= font.render(f'GAME OVER! PLAY AGAIN? (Y or N) ',True,white)
        text_rect= text.get_rect()
        text_rect.center= (width / 2,100)
        screen.blit(text,text_rect)
    pygame.display.update()
    while gameover:
        clock.tick(fps)
        for event in pygame.event.get():
            # Cập nhật điểm cao nhất:
            if score > high_score:
                high_score = score
                with open("high_score.txt", "w") as f:
                    f.write(str(high_score))

            if event.type==QUIT:
                gameover= False
                running = False

            if event.type==KEYDOWN:
                if event.key == K_y:
                    #Reset game
                    gameover = False
                    score = 0
                    speed = 2
                    Vehicle_group.empty()
                    player.rect.center = [player_x, player_y]  
                elif event.key == K_n:
                    #Exit game
                    gameover = False
                    running = False              
pygame.quit()

