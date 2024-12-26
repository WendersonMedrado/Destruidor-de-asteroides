import time
import sqlite3
import arcade
import arcade.gui
from sprites import *
from config import *

# ============================================================================================
# =================== TELA DE INÍCIO =========================================================
# ============================================================================================
class StartView(arcade.View):
    def on_show_view(self):
        self.background = arcade.load_texture(CAMINHO + "/img/background_start_0.jpg")
    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0,0,WIDTH,HEIGHT,self.background)
        arcade.draw_text("INSTRUÇÕES",WIDTH/4, HEIGHT - 150, arcade.color.BLACK, 40,
                            font_name="Kenney Future")
        arcade.draw_text("A,S,D e W controlam a direção,",
                            WIDTH/10, HEIGHT/2, arcade.color.BLACK, 20,
                            font_name="Kenney Future Narrow")
        arcade.draw_text("número 5 atira.",
                            WIDTH/10, HEIGHT/2 -30, arcade.color.BLACK, 20,
                            font_name="Kenney Future Narrow")

        arcade.draw_text("Clique na tela para prosseguir.", WIDTH/10, HEIGHT/2 - 100, 
                            arcade.color.WHITE, 25,font_name="Kenney Future Narrow")
    def on_mouse_press(self, _x,_y,_button, _modifiers):
        choice_view = ChoiceView()
        self.window.show_view(choice_view)

# ============================================================================================
# =================== ESCOLHA DA NAVE ========================================================
# ============================================================================================
class ChoiceView(arcade.View):
    def __init__(self):
        super().__init__()
        con = sqlite3.connect(CAMINHO + "/records.sqlite3")
        cur = con.cursor()
        record = cur.execute("SELECT pontuação FROM records WHERE record='recorde'")
        self.record = record.fetchone()
        con.close()
        self.ship = [
            CAMINHO + "/img/playerShip1_blue.png",
            CAMINHO + "/img/playerShip1_green.png",
            CAMINHO + "/img/playerShip1_orange.png",
            CAMINHO + "/img/playerShip2_orange.webp",
            CAMINHO + "/img/playerShip3_orange.webp"
        ]
        self.number_nave = 0
        self.start_sound = arcade.sound.load_sound(CAMINHO + "/sound/upgrade5.wav")
        self.nave = [
            arcade.load_texture(CAMINHO + "/img/playerShip1_blue.png"),
            arcade.load_texture(CAMINHO + "/img/playerShip1_green.png"),
            arcade.load_texture(CAMINHO + "/img/playerShip1_orange.png"),
            arcade.load_texture(CAMINHO + "/img/playerShip2_orange.webp"),
            arcade.load_texture(CAMINHO + "/img/playerShip3_orange.webp")
        ]
        self.ui_manager = arcade.gui.UIManager(self.window)
        box = arcade.gui.UIBoxLayout(vertical=False)
        # Left button
        normal = arcade.load_texture(CAMINHO + "/img/left2.webp")
        hover = arcade.load_texture(CAMINHO + "/img/left1.webp")
        self.left_button = arcade.gui.UITextureButton(texture=normal,texture_hovered=hover)
        self.left_button.on_click = self.left_button_clicked
        box.add(self.left_button)
        # Right button
        normal = arcade.load_texture(CAMINHO + "/img/right2.webp")
        hover = arcade.load_texture(CAMINHO + "/img/right1.webp")
        self.right_button = arcade.gui.UITextureButton(texture=normal,texture_hovered=hover)
        self.right_button.on_click = self.right_button_clicked
        box.add(self.right_button)
        # Start button
        normal = arcade.load_texture(CAMINHO + "/img/start2.webp")
        hover = arcade.load_texture(CAMINHO + "/img/start3.webp")
        self.start_button = arcade.gui.UITextureButton(texture=normal,texture_hovered=hover)
        self.start_button.on_click = self.start_button_clicked
        box.add(self.start_button)

        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box))
    def on_show_view(self):
        arcade.set_background_color(arcade.color.BOYSENBERRY)
        self.ui_manager.enable()
    def on_draw(self):
        self.clear()
        arcade.draw_text("Escolha sua nave", WIDTH/2-200,HEIGHT/2+110,arcade.color.WHITE,60,font_name="Kenney Pixel")
        self.ui_manager.draw()
        arcade.draw_text(f"Nave {self.number_nave+1}/5", WIDTH/2-50,HEIGHT/2-110,arcade.color.WHITE,30,font_name="Kenney Pixel")
        arcade.draw_lrwh_rectangle_textured(WIDTH/2-50,HEIGHT/2-250,100,100,self.nave[self.number_nave])

    def left_button_clicked(self, *_):
        self.number_nave -= 1
        if self.number_nave == -1:
            self.number_nave = 0
    
    def right_button_clicked(self, *_):
        self.number_nave += 1
        if self.number_nave == 5:
            self.number_nave = 4

    def start_button_clicked(self,*_):
        arcade.sound.play_sound(self.start_sound)
        ship = self.ship[self.number_nave]
        game_view = GameView(ship,self.record)
        self.window.show_view(game_view)

# ============================================================================================
# =================== TELA DO JOGO ===========================================================
# ============================================================================================
class GameView(arcade.View):
    def __init__(self,ship,record):
        super().__init__()
        self.ship = ship
        self.score = 0
        self.life  = 3
        self.number_asteroids = 5
        self.record = record[0]
        self.sound_game_over = arcade.sound.load_sound(CAMINHO + "/sound/gameover5.wav")
        self.background_game = arcade.load_texture(CAMINHO + "/img/background_game.png")
        # Variables that will hold sprite lists.
        self.player_list    = arcade.SpriteList()
        self.shoot_list     = arcade.SpriteList()
        self.asteroids_list = None
        self.explosion_list = None
        self.explosion_texture_list = []
        # Set up the player info
        self.explosion_texture_list = arcade.load_spritesheet(EXPLOSION_FILE, EXPLOSION_WIDTH, EXPLOSION_HEIGHT, COLUMNS, COUNT)
        self.shoot_sound   = arcade.sound.load_sound(CAMINHO + "/sound/laser2.wav")
        self.explosion_sound = arcade.sound.load_sound(CAMINHO + "/sound/explosion2.wav")
        self.player_sprite    = None
        self.shoot_sprite     = None
        self.asteroids_sprite = [i for i in range(100)]
        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)
        # Set background color
        arcade.set_background_color(arcade.color.TEAL_BLUE)
        self.cria()
        self.explosion_list = arcade.SpriteList()
        self.player_sprite =  Player(self.ship)
        self.player_list.append(self.player_sprite)
        self.cria()
    def cria(self):
        self.asteroids_list = arcade.SpriteList()
        for i in range(self.number_asteroids):
            self.asteroids_sprite[i] = Asteroids(CAMINHO + "/img/meteorGrey_small1.png")
            self.asteroids_list.append(self.asteroids_sprite[i])
    def update(self,delta_time):
        self.explosion_list.update()
        for asteroid in self.asteroids_list:
            hit_list = arcade.check_for_collision_with_list(asteroid, self.shoot_list)

            if len(hit_list) > 0:
                asteroid.remove_from_sprite_lists()
                self.score += 1

                explosion = Explosion(self.explosion_texture_list)
                explosion.center_x = hit_list[0].center_x
                explosion.center_y = hit_list[0].center_y
                explosion.update()
                arcade.sound.play_sound(self.explosion_sound)
                self.explosion_list.append(explosion)
            for shoot in hit_list:
                shoot.remove_from_sprite_lists()   

        for nave in self.player_list:
            hit_list = arcade.check_for_collision_with_list(nave, self.asteroids_list)
            if len(hit_list) > 0:
                self.life -= 1
                nave.remove_from_sprite_lists()
                for asteroids in self.asteroids_list:
                    asteroids.remove_from_sprite_lists()
                self.player_sprite =  Player(self.ship)
                self.player_list.append(self.player_sprite)
                self.cria()
                time.sleep(0.5)
                if self.life == 0:
                    arcade.sound.play_sound(self.sound_game_over)
                    game_over_view = GameOver(self.score,self.record)
                    self.window.show_view(game_over_view)
                 
        self.player_sprite.animate()
        self.shoot_list.update()
        
        for i in range(self.number_asteroids):
            self.asteroids_sprite[i].animate()
            
        self.asteroids_list.update()
        
        if len(self.asteroids_list) == 0:
            self.number_asteroids += 2
            self.cria()
        
        for shoot in self.shoot_list:
            if shoot.bottom > HEIGHT or shoot.top < -20 or shoot.left < -25 or shoot.right > WIDTH + 25:
                shoot.remove_from_sprite_lists()
        
    def on_draw(self):
        arcade.draw_lrwh_rectangle_textured(0,0,WIDTH,HEIGHT,self.background_game)
        arcade.draw_text(f'SCORE: {self.score}',10,HEIGHT-20,arcade.color.GREEN)
        arcade.draw_text(f'LIFE: {self.life}',WIDTH-70,HEIGHT-20,arcade.color.GREEN)
        arcade.draw_text(f'RECORD: {self.record}', WIDTH/2 - 55, HEIGHT- 20,arcade.color.GREEN)
        arcade.draw_rectangle_outline(WIDTH/2,HEIGHT/2,WIDTH-100,HEIGHT-100,arcade.color.GRAY)

        self.player_list.draw()
        self.shoot_list.draw()
        self.asteroids_list.draw()
        self.explosion_list.draw()
           
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S or key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.key_press(key)
        if key == arcade.key.NUM_5:
           self.shoot_sprite = Shoot(
                CAMINHO + "/img/laserBlue01.png",
                self.player_sprite.angle, 
                self.player_sprite.center_x, 
                self.player_sprite.center_y
            )
           self.shoot_list.append(self.shoot_sprite)
           arcade.sound.play_sound(self.shoot_sound, 0.2)
            
    def on_key_release(self, key, modifiers):
        self.player_sprite.key_release(key)

# ============================================================================================
# =================== GAME OVER ==============================================================
# ============================================================================================
class GameOver(arcade.View):
    def __init__(self,pontos,recorde):
        super().__init__()
        self.pontos = pontos
        self.record = recorde
        if self.pontos > self.record:     
            con = sqlite3.connect(CAMINHO + "/records.sqlite3")
            cur = con.cursor()
            cur.execute(f"UPDATE records SET pontuação={self.pontos} WHERE record='recorde'")
            con.commit()
            con.close()
        self.window.set_mouse_visible(True)
        self.ui_manager = arcade.gui.UIManager(self.window)
        box = arcade.gui.UIBoxLayout(vertical=True,align='left')

        label1 = arcade.gui.UILabel(text=f'Pontuação:  {self.pontos}',font_size=30)
        box.add(label1)
        
        normal = arcade.load_texture(CAMINHO + '/img/start2.webp')
        hover  = arcade.load_texture(CAMINHO + '/img/start3.webp')
        self.restart_button = arcade.gui.UITextureButton(texture=normal, texture_hovered=hover)
        self.restart_button.on_click = self.restart_button_clicked
        box.add(self.restart_button)

       
        self.ui_manager.add(arcade.gui.UIAnchorWidget(child=box))
    def on_show_view(self):
        arcade.set_background_color(arcade.color.RED)
        self.ui_manager.enable()
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("GAME OVER",WIDTH/4, HEIGHT - 150, arcade.color.BLACK, 40,
                            font_name="Kenney Future")
    
        self.ui_manager.draw()

    def restart_button_clicked(self, *_):
        
        choice_view = ChoiceView()
        self.window.show_view(choice_view)
# ============================================================================================
# =================== FUNÇÃO PRINCIPAL PARA RODAR O GAME =====================================
# ============================================================================================
def main():
    window = arcade.Window(WIDTH, HEIGHT, "Destruidor de Asteróides")
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()