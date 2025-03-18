import pygame
from sys import exit
from protocols import Protocols
from game_state import GameState
from description import Description
from role_prompt import RolePrompt

class ONUW:
    #Initiate Game
    def __init__(self, client):
        self.client = client
        self.client.run()

        #Initiate PyGame
        pygame.init()
        self.width = 640 # Width Window
        self.height = 480 # Height Window
        self.flags = pygame.SCALED | pygame.RESIZABLE # Flags
        self.screen = pygame.display.set_mode((self.width, self.height), self.flags)
        pygame.display.set_caption("One Night Ultimate Werewolf") # Caption
        self.FPS = 60 # FPS
        self.clock = pygame.time.Clock()

        # Inputs
        self.select_input = False
        self.error_text = ""
        # Username
        self.username = ""
        # Password
        self.password_input = ""
        # Role Selection
        self.role_select_input = ""
        # Role Detail
        self.viewing_role = ""
        self.viewing_alignment = ""
        self.viewing_creature = ""
        # Role Choose
        self.choices = []
        self.choice_input = ""
        self.choice_submit = []
        self.choosing = False
        self.doppelganger_temp = None
        # Voting
        self.vote_input = ""
    
    # Loading
    def loading(self):
        # Interactives
        # Quit Button
        quit_button = pygame.Rect(self.width - 50, 0, 50, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and quit_button.collidepoint(pygame.mouse.get_pos())):
                self.client.close()
                pygame.quit()
                exit()

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Loading Text
        loading_font = pygame.font.SysFont("Arial", 50)
        loading_surface = loading_font.render("Loading...", True, (0, 0, 0))
        loading_rect = loading_surface.get_rect(center = (self.width/2, self.height/2))
        self.screen.blit(loading_surface, loading_rect)
        # Quit Button
        pygame.draw.rect(self.screen, (255, 0, 0), quit_button)
        quit_font = pygame.font.SysFont("Arial", 50)
        quit_surface = quit_font.render("X", True, (255, 255, 255))
        quit_rect = quit_surface.get_rect(center = (self.width - 25, 25))
        self.screen.blit(quit_surface, quit_rect)

    # Main Menu
    def main_menu(self):
        # Interactives
        # Quit Button
        quit_button = pygame.Rect(self.width - 50, 0, 50, 50)
        # Username Input Box
        username_input_box = pygame.Rect(self.width/2 - 150, self.height/2 - 25, 300, 50)
        # How To Play Button
        how_to_play_button = pygame.Rect(5, self.height - 110, 100, 50)
        # Credits Button
        credits_button = pygame.Rect(5, self.height - 55, 100, 50)
        
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and quit_button.collidepoint(pygame.mouse.get_pos())):
                self.client.close()
                pygame.quit()
                exit()
            # How To Play
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and how_to_play_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.HOW_TO_PLAY
            # Credits
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and credits_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.CREDITS
            # Select Username Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and username_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = True
            # Unselect Username Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not username_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = False
            # Attempt username
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Error no username
                if len(self.username) <= 0:
                    self.error_text = "Invalid - Empty Username"
                 # Submit username and go to Host or Join
                else:
                    self.error_text = ""
                    self.select_input = False
                    self.client.room = None
                    self.client.send(Protocols.Main_Menu.USERNAME, self.username)
                    self.client.game_state = GameState.HOST_OR_JOIN
            # Enter Username Text
            elif event.type == pygame.KEYDOWN and self.select_input:
                # Remove a letter
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                # Enter a letter
                elif event.key != pygame.K_SPACE: # No space in username
                    if len(self.username) < 12: # MAXIMUM USERNAME LENGTH = 12
                        self.username += event.unicode

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Title
        title_font = pygame.font.SysFont("Arial", 50)
        title_surface = title_font.render("One Night Ultimate Werewolf", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center = (self.width/2, self.height/4))
        self.screen.blit(title_surface, title_rect)
        # Quit Button
        pygame.draw.rect(self.screen, (255, 0, 0), quit_button)
        quit_text_font = pygame.font.SysFont("Arial", 50)
        quit_text_surface = quit_text_font.render("X", True, (255, 255, 255))
        quit_text_rect = quit_text_surface.get_rect(center = (self.width - 25, 25))
        self.screen.blit(quit_text_surface, quit_text_rect)
        # Enter Username text
        enter_username_font = pygame.font.SysFont("Arial", 30)
        enter_username_surface = enter_username_font.render("Enter your username (Max 12 characters): ", True, (0, 0, 0))
        enter_username_rect = enter_username_surface.get_rect(center = (self.width/2, self.height/2 - 50))
        self.screen.blit(enter_username_surface, enter_username_rect)
        # Username Input Box
        if self.select_input:
            pygame.draw.rect(self.screen, (75, 75, 255), username_input_box, 4)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), username_input_box, 2)
        # Username
        username_font = pygame.font.SysFont("Arial", 30)
        username_surface = username_font.render(self.username, True, (0, 0, 0))
        username_rect = username_surface.get_rect(center = (self.width/2, self.height/2))
        self.screen.blit(username_surface, username_rect)
        # Error Text
        error_font = pygame.font.SysFont("Arial", 30)
        error_surface = error_font.render(self.error_text, True, (255, 0, 0))
        error_rect = error_surface.get_rect(center = (self.width/2, self.height*2/3))
        self.screen.blit(error_surface, error_rect)
        # Enter Text
        enter_font = pygame.font.SysFont("Arial", 30)
        enter_surface = enter_font.render("Press ENTER to start", True, (0, 0, 0))
        enter_rect = enter_surface.get_rect(midbottom = (self.width/2, self.height - 5))
        self.screen.blit(enter_surface, enter_rect)
        # How To Play Button
        pygame.draw.rect(self.screen, (200, 200, 200), how_to_play_button)
        pygame.draw.rect(self.screen, (100, 100, 100), how_to_play_button, 10)
        how_to_play_text_font = pygame.font.SysFont("Arial", 15)
        how_to_play_text_surface = how_to_play_text_font.render("How To Play", True, (0, 0, 0))
        how_to_play_text_rect = how_to_play_text_surface.get_rect(center = (55, self.height - 85))
        self.screen.blit(how_to_play_text_surface, how_to_play_text_rect)
        # Credits Button
        pygame.draw.rect(self.screen, (200, 200, 200), credits_button)
        pygame.draw.rect(self.screen, (100, 100, 100), credits_button, 10)
        credits_text_font = pygame.font.SysFont("Arial", 25)
        credits_text_surface = credits_text_font.render("Credits", True, (0, 0, 0))
        credits_text_rect = credits_text_surface.get_rect(center = (55, self.height - 30))
        self.screen.blit(credits_text_surface, credits_text_rect)
        # Python
        version_font = pygame.font.SysFont("Arial", 30)
        version_surface = version_font.render("py. 3.13.2", True, (0, 0, 0))
        version_rect = version_surface.get_rect(bottomright = (self.width, self.height - 40))
        self.screen.blit(version_surface, version_rect)
        # Version
        version_font = pygame.font.SysFont("Arial", 30)
        version_surface = version_font.render("v. 0.1.0.0", True, (0, 0, 0))
        version_rect = version_surface.get_rect(bottomright = (self.width, self.height - 5))
        self.screen.blit(version_surface, version_rect)

        # Stop Music
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    
    # How To Play
    def how_to_play(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.MAIN_MENU

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Youtube Link
        youtube_link_font = pygame.font.SysFont("Arial", 20)
        youtube_link_surface = youtube_link_font.render("https://www.youtube.com/watch?v=7rwi40IG-_0", True, (0, 0, 0))
        youtube_link_rect = youtube_link_surface.get_rect(center = (self.width/2, self.height/2))
        self.screen.blit(youtube_link_surface, youtube_link_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(back_text_surface, back_text_rect)

    # Credits
    def credits(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.MAIN_MENU

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Credits
        credits_font = pygame.font.SysFont("Arial", 20)
        credits_text = ["Game made by Nounou144", "", "Based on the game \"One Night Ultimate Werewolf\"", "by Bézier Games, Inc.", "", "Thanks ChatGPT for helping me through some roadblocks", "", "Thank you for playing!"]
        for line in range(len(credits_text)):
            credits_surface = credits_font.render(credits_text[line], True, (0, 0, 0))
            credits_rect = credits_surface.get_rect(topleft = (5, 5 + line*20))
            self.screen.blit(credits_surface, credits_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(back_text_surface, back_text_rect)

    # Host or Join
    def host_or_join(self):
        # Interactives
        # Host Button
        host_button = pygame.Rect(self.width/3 - 100, self.height/2 - 50, 200, 100)
        # Join Button
        join_button = pygame.Rect(self.width*2/3 - 100, self.height/2 - 50, 200, 100)
        # Back Button
        back_button = pygame.Rect(self.width/2 - 100, self.height*3/4 - 50, 200, 100)
        
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.MAIN_MENU
            # Join
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and join_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.PASSWORD
            # Host
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and host_button.collidepoint(pygame.mouse.get_pos()):
                self.client.send(Protocols.Room.CREATE_ROOM, None)
                self.client.game_state = GameState.ROOM

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Title
        title_font = pygame.font.SysFont("Arial", 50)
        title_surface = title_font.render("One Night Ultimate Werewolf", True, (0, 0, 0))
        title_rect = title_surface.get_rect(center = (self.width/2, self.height/4))
        self.screen.blit(title_surface, title_rect)
        # Host Button
        pygame.draw.rect(self.screen, (0,0, 255), host_button)
        pygame.draw.rect(self.screen, (127, 127, 255), host_button, 20)
        host_text = pygame.font.SysFont("Arial", 50)
        host_text_surface = host_text.render("Host", True, (0, 0, 0))
        host_text_rect = host_text_surface.get_rect(center = (self.width/3, self.height/2))
        self.screen.blit(host_text_surface, host_text_rect)
        # Join Button
        pygame.draw.rect(self.screen, (255, 255, 0), join_button)
        pygame.draw.rect(self.screen, (0, 0, 0), join_button, 20)
        join_text = pygame.font.SysFont("Arial", 50)
        join_text_surface = join_text.render("Join", True, (0, 0, 0))
        join_text_rect = join_text_surface.get_rect(center = (self.width*2/3, self.height/2))
        self.screen.blit(join_text_surface, join_text_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 20)
        back_text = pygame.font.SysFont("Arial", 50)
        back_text_surface = back_text.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width/2, self.height*3/4))
        self.screen.blit(back_text_surface, back_text_rect)

    # Password
    def password(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Password Input Box
        password_input_box = pygame.Rect(self.width/2 - 150, self.height/2 - 25, 300, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Host or Join
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.HOST_OR_JOIN
            # Select Password Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and password_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = True
            # Unselect Password Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not password_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = False
            # Attempt password
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Error not exactly 4 characters
                if len(self.password_input) < 4:
                    self.error_text = "Invalid - Needs 4 characters"
                 # Join Room
                else:
                    self.error_text = "Something went wrong. Check commande prompt."
                    self.client.send(Protocols.Room.JOIN_ROOM, self.password_input.upper())
            # Enter Password Text
            elif event.type == pygame.KEYDOWN and self.select_input:
                # Remove a letter
                if event.key == pygame.K_BACKSPACE:
                    self.password_input = self.password_input[:-1]
                # Enter a letter
                elif event.key != pygame.K_SPACE: # No space in password
                    if len(self.password_input) < 4: # MAXIMUM PASSWORD LENGTH = 4
                        self.password_input += event.unicode

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Password Text
        password_text_font = pygame.font.SysFont("Arial", 50)
        password_text_surface = password_text_font.render("Enter password (4 characters):", True, (0, 0, 0))
        password_text_rect = password_text_surface.get_rect(center = (self.width/2, self.height/2 - 50))
        self.screen.blit(password_text_surface, password_text_rect)
        # Password Input Box
        if self.select_input:
            pygame.draw.rect(self.screen, (75, 75, 255), password_input_box, 4)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), password_input_box, 2)
        # Password
        password_font = pygame.font.SysFont("Arial", 30)
        password_surface = password_font.render(self.password_input, True, (0, 0, 0))
        password_rect = password_surface.get_rect(center = (self.width/2, self.height/2))
        self.screen.blit(password_surface, password_rect)
        # Error Text
        error_font = pygame.font.SysFont("Arial", 20)
        error_surface = error_font.render(self.error_text, True, (255, 0, 0))
        error_rect = error_surface.get_rect(center = (self.width/2, self.height*2/3))
        self.screen.blit(error_surface, error_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(back_text_surface, back_text_rect)

        # Check if room has been sent
        if self.client.room != None:
            self.error_text = ""
            self.select_input = False
            self.client.game_state = GameState.ROOM

    # Room
    def room(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Ready Button
        ready_button = pygame.Rect(self.width/2 - 100, self.height - 105, 200, 100)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.send(Protocols.Room.LEAVE_ROOM, None)
                self.client.close()
                pygame.quit()
                exit()
            # Back to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.MAIN_MENU
                self.client.send(Protocols.Room.LEAVE_ROOM, None)
            # Ready or Unready
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and ready_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.role_select_input = ""
                self.client.send(Protocols.Room.READY, None)

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Password
        password_font = pygame.font.SysFont("Arial", 30)
        password_surface = password_font.render(f"Password: {self.client.room["password"]}", True, (0, 0, 0))
        password_rect = password_surface.get_rect(midtop = (self.width/2, 5))
        self.screen.blit(password_surface, password_rect)
        # Players
        players_font = pygame.font.SysFont("Arial", 20)
        for player in range(len(self.client.room["username"])):
            players_surface = players_font.render(f"{player+1}. {self.client.room["username"][player]} - {"Ready" if self.client.room["ready"][player] else "Not Ready"}", True, (0, 0, 0))
            players_rect = players_surface.get_rect(topleft = (5, 40 + player*20))
            self.screen.blit(players_surface, players_rect)
        # Ready Button
        pygame.draw.rect(self.screen, (0, 255, 0), ready_button)
        pygame.draw.rect(self.screen, (127, 255, 127), ready_button, 20)
        ready_text_font = pygame.font.SysFont("Arial", 50)
        ready_text_surface = ready_text_font.render("Ready", True, (0, 0, 0))
        ready_text_rect = ready_text_surface.get_rect(center = (self.width/2, self.height - 55))
        self.screen.blit(ready_text_surface, ready_text_rect)
        # Min - Max
        minmax_font = pygame.font.SysFont("Arial", 20)
        minmax_surface = minmax_font.render("Required - Min: 3; Max: 10", True, (0, 0, 0))
        minmax_rect = minmax_surface.get_rect(center = (self.width/2, self.height - 120))
        self.screen.blit(minmax_surface, minmax_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(back_text_surface, back_text_rect)
    
    # Player Left
    def player_left(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, 5, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Room
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.ROOM

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Winners
        winners_font = pygame.font.SysFont("Arial", 30)
        winners_surface = winners_font.render("Player left...", True, (0, 0, 0))
        winners_rect = winners_surface.get_rect(midtop = (self.width / 2, 5))
        self.screen.blit(winners_surface, winners_rect)
        # Player
        player_font = pygame.font.SysFont("Arial", 15)
        for end_player in range(len(self.client.room["end_players"])):
            player_text = f"{end_player + 1}. {self.client.room["end_players"][end_player]} - Original:{self.client.room["player_roles"][end_player]}"
            player_surface = player_font.render(player_text, True, (0, 0, 0))
            player_rect = player_surface.get_rect(topleft = (5, 40 + end_player * 15))
            self.screen.blit(player_surface, player_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, 30))
        self.screen.blit(back_text_surface, back_text_rect)

        self.vote_input = ""

        # Stop Music
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    # Select Roles
    def select_roles(self):
        # Interactives
        # Exit Button
        exit_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Role Select Input
        role_select_input_box = pygame.Rect(self.width/2 - 25, self.height - 210, 50, 50)
        # Start Button
        start_button = pygame.Rect(self.width/2 - 100, self.height - 105, 200, 100)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Exit Game to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and exit_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.MAIN_MENU
                self.client.send(Protocols.Room.LEAVE_ROOM, None)
            # Start to get role
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and start_button.collidepoint(pygame.mouse.get_pos()):
                number_of_roles_selected = 0
                for role in range(len(self.client.room["roles"])):
                    if list(self.client.room["roles"].values())[role][1]:
                        number_of_roles_selected += 1
                if number_of_roles_selected != len(self.client.room["username"]) + 3:
                    self.error_text = "Invalid - Number of role selected is not correct"
                else:
                    self.error_text = ""
                    self.select_input = False
                    self.role_select_input = ""
                    self.client.send(Protocols.GameStart.GET_ROLE, None)
            # Role Select Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and role_select_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = True
            # Role Unselect Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not role_select_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = False
            # Attempt Selecting Role
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # If there are no inputs
                if len(self.role_select_input) <= 0:
                    self.role_select_input = ""
                    self.error_text = "Invalid - No Input"
                # If the input is 0 or lower
                elif int(self.role_select_input) <= 0:
                    self.role_select_input = ""
                    self.error_text = "Invalid - Input is 0 or lower"
                # If the input exceeds the number of roles
                elif int(self.role_select_input) > len(self.client.room["roles"]):
                    self.role_select_input = ""
                    self.error_text = "Invalid - Exceeds the number of roles"
                else:
                    role_selected = list(self.client.room["roles"].keys())[int(self.role_select_input) - 1]
                    self.error_text = ""
                    self.role_select_input = ""
                    self.client.send(Protocols.GameStart.ROLE_SELECTED, role_selected)
            # Enter Number
            elif event.type == pygame.KEYDOWN and self.select_input:
                # Remove a number
                if event.key == pygame.K_BACKSPACE:
                    self.role_select_input = self.role_select_input[:-1]
                # Enter a number
                else:
                    if len(self.role_select_input) < 2: # MAXIMUM ROLE SELECT LENGTH = 2
                        # Only type numbers
                        if event.unicode in "1234567890":
                            self.role_select_input += event.unicode

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Wait for the first player to select roles
        waiting_font = pygame.font.SysFont("Arial", 30)
        waiting_surface = waiting_font.render(f"Wait for {self.client.room["username"][0]} to select roles...", True, (0, 0, 0))
        waiting_rect = waiting_surface.get_rect(midtop = (self.width/2, 5))
        self.screen.blit(waiting_surface, waiting_rect)
        # Roles
        roles_font = pygame.font.SysFont("Arial", 20)
        for role in range(len(self.client.room["roles"])):
            roles_surface = roles_font.render(f"{role+1}. {list(self.client.room["roles"].values())[role][0]} - {"SELECTED" if list(self.client.room["roles"].values())[role][1] else "OFF"}", True, (0, 0, 0))
            roles_rect = roles_surface.get_rect(topleft = (5, 40 + role*20))
            self.screen.blit(roles_surface, roles_rect)
        # If you are the first player, you can select roles
        if self.client.room["username"][0] == self.username:
            # Role Select Input Box
            if self.select_input:
                pygame.draw.rect(self.screen, (75, 75, 255), role_select_input_box, 4)
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), role_select_input_box, 2)
            # Enter number
            enter_number_font = pygame.font.SysFont("Arial", 20)
            enter_number_surface = enter_number_font.render(f"Enter a role number to select it", True, (0, 0, 0))
            enter_number_rect = enter_number_surface.get_rect(center = (self.width/2, self.height - 225))
            self.screen.blit(enter_number_surface, enter_number_rect)
            # Role Select Input
            role_select_input_font = pygame.font.SysFont("Arial", 30)
            role_select_input_surface = role_select_input_font.render(self.role_select_input, True, (0, 0, 0))
            role_select_input_rect = role_select_input_surface.get_rect(center = (self.width/2, self.height - 185))
            self.screen.blit(role_select_input_surface, role_select_input_rect)
            # Error Text
            error_font = pygame.font.SysFont("Arial", 20)
            error_surface = error_font.render(self.error_text, True, (255, 0, 0))
            error_rect = error_surface.get_rect(center = (self.width/2, self.height - 145))
            self.screen.blit(error_surface, error_rect)
            # Number of roles required
            num_roles_font = pygame.font.SysFont("Arial", 20)
            number_of_roles_selected = 0
            for role in range(len(self.client.room["roles"])):
                if list(self.client.room["roles"].values())[role][1]:
                    number_of_roles_selected += 1
            num_roles_surface = num_roles_font.render(f"Numer of roles required: ({number_of_roles_selected}/{len(self.client.room["username"]) + 3})", True, (0, 0, 0))
            num_roles_rect = num_roles_surface.get_rect(center = (self.width/2, self.height - 120))
            self.screen.blit(num_roles_surface, num_roles_rect)
            # Start Button
            pygame.draw.rect(self.screen, (0, 255, 0), start_button)
            pygame.draw.rect(self.screen, (127, 255, 127), start_button, 20)
            start_text_font = pygame.font.SysFont("Arial", 50)
            start_text_surface = start_text_font.render("Start", True, (0, 0, 0))
            start_text_rect = start_text_surface.get_rect(center = (self.width/2, self.height - 55))
            self.screen.blit(start_text_surface, start_text_rect)
        # Exit Button
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button)
        pygame.draw.rect(self.screen, (255, 127, 127), exit_button, 10)
        exit_text_font = pygame.font.SysFont("Arial", 25)
        exit_text_surface = exit_text_font.render("Exit", True, (0, 0, 0))
        exit_text_rect = exit_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(exit_text_surface, exit_text_rect)

    # Get Role
    def get_role(self):
        # Interactives
        # Exit Button
        exit_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Ready Button
        ready_button = pygame.Rect(self.width/2 - 100, self.height - 105, 200, 100)
        # Night Order Button
        night_order_button = pygame.Rect(5, self.height - 110, 100, 50)
        # View Roles Button
        view_roles_button = pygame.Rect(5, self.height - 55, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Exit Game to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and exit_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.MAIN_MENU
                self.client.send(Protocols.Room.LEAVE_ROOM, None)
            # Ready or Unready
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and ready_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.send(Protocols.Room.READY, None)
            # Night Order
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and night_order_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.NIGHT_ORDER
            # View Roles
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and view_roles_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.VIEW_ROLES

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Role Text
        role_text_font = pygame.font.SysFont("Arial", 30)
        role_text_surface = role_text_font.render("Your role is:", True, (0, 0, 0))
        role_text_rect = role_text_surface.get_rect(center = (self.width/2, 20))
        self.screen.blit(role_text_surface, role_text_rect)
        # Role
        role_font = pygame.font.SysFont("Arial", 30)
        role_surface = role_font.render(self.client.room["player_roles"][self.client.room["username"].index(self.username)], True, (0, 0, 0))
        role_rect = role_surface.get_rect(center = (self.width/2, 55))
        self.screen.blit(role_surface, role_rect)
        # Players
        players_font = pygame.font.SysFont("Arial", 20)
        for player in range(len(self.client.room["username"])):
            players_surface = players_font.render(f"{player+1}. {self.client.room["username"][player]} - {"Ready" if self.client.room["ready"][player] else "Not Ready"}", True, (0, 0, 0))
            players_rect = players_surface.get_rect(topleft = (5, 40 + player*20))
            self.screen.blit(players_surface, players_rect)
        # Ready Button
        pygame.draw.rect(self.screen, (0, 255, 0), ready_button)
        pygame.draw.rect(self.screen, (127, 255, 127), ready_button, 20)
        ready_text_font = pygame.font.SysFont("Arial", 50)
        ready_text_surface = ready_text_font.render("Ready", True, (0, 0, 0))
        ready_text_rect = ready_text_surface.get_rect(center = (self.width/2, self.height - 55))
        self.screen.blit(ready_text_surface, ready_text_rect)
        # Night Order Button
        pygame.draw.rect(self.screen, (200, 200, 200), night_order_button)
        pygame.draw.rect(self.screen, (100, 100, 100), night_order_button, 10)
        night_order_text_font = pygame.font.SysFont("Arial", 20)
        night_order_text_surface = night_order_text_font.render("Night Order", True, (0, 0, 0))
        night_order_text_rect = night_order_text_surface.get_rect(center = (55, self.height - 85))
        self.screen.blit(night_order_text_surface, night_order_text_rect)
        # View Roles Button
        pygame.draw.rect(self.screen, (200, 200, 200), view_roles_button)
        pygame.draw.rect(self.screen, (100, 100, 100), view_roles_button, 10)
        view_roles_text_font = pygame.font.SysFont("Arial", 20)
        view_roles_text_surface = view_roles_text_font.render("View Roles", True, (0, 0, 0))
        view_roles_text_rect = view_roles_text_surface.get_rect(center = (55, self.height - 30))
        self.screen.blit(view_roles_text_surface, view_roles_text_rect)
        # Exit Button
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button)
        pygame.draw.rect(self.screen, (255, 127, 127), exit_button, 10)
        exit_text_font = pygame.font.SysFont("Arial", 25)
        exit_text_surface = exit_text_font.render("Exit", True, (0, 0, 0))
        exit_text_rect = exit_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(exit_text_surface, exit_text_rect)

        self.client.role_prompt = RolePrompt.NONE

    # Night Order
    def night_order(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, 5, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Game
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                if not self.client.room["night_started"]:
                    self.client.game_state = GameState.GET_ROLE
                elif not self.client.room["night_ended"]:
                    self.client.game_state = GameState.NIGHT
                else:
                    self.client.game_state = GameState.DAY

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Night Order
        night_order_font = pygame.font.SysFont("Arial", 30)
        night_order_surface = night_order_font.render("Night Order", True, (0, 0, 0))
        night_order_rect = night_order_surface.get_rect(topleft = (5, 5))
        self.screen.blit(night_order_surface, night_order_rect)
        # Selected Player Roles
        roles_font = pygame.font.SysFont("Arial", 20)
        for order in range(len(self.client.room["role_order"])):
            roles_surface = roles_font.render(f"{order+1}. {self.client.room["role_order"][order]}", True, (0, 0, 0))
            roles_rect = roles_surface.get_rect(topleft = (5, 40 + order*20))
            self.screen.blit(roles_surface, roles_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, 30))
        self.screen.blit(back_text_surface, back_text_rect)

        # Music at Night
        if not pygame.mixer.music.get_busy() and self.client.room["night_started"] and not self.client.room["night_ended"]:
            pygame.mixer.music.play()

    # View Roles
    def view_roles(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, 5, 100, 50)
        # Role Select Input
        role_select_input_box = pygame.Rect(self.width/2 - 25, self.height - 80, 50, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Game
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.role_select_input = ""
                if not self.client.room["night_started"]:
                    self.client.game_state = GameState.GET_ROLE
                else:
                    if not self.client.room["night_ended"]:
                        self.client.game_state = GameState.NIGHT
                    else:
                        self.client.game_state = GameState.DAY
            # Role Select Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and role_select_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = True
            # Role Unselect Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not role_select_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = False
            # Attempt Selecting Role
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # If there are no inputs
                if len(self.role_select_input) <= 0:
                    self.role_select_input = ""
                    self.error_text = "Invalid - No Input"
                # If the input is 0 or lower
                elif int(self.role_select_input) <= 0:
                    self.role_select_input = ""
                    self.error_text = "Invalid - Input is 0 or lower"
                # If the input exceeds the number of roles
                elif int(self.role_select_input) > len(self.client.room["selected_player_roles"]):
                    self.role_select_input = ""
                    self.error_text = "Invalid - Exceeds the number of roles"
                else:
                    self.error_text = ""
                    self.select_input = False
                    self.viewing_role = self.client.room["selected_player_roles"][int(self.role_select_input) - 1]
                    self.viewing_alignment = self.client.room["selected_alignment"][int(self.role_select_input) - 1]
                    self.viewing_creature = self.client.room["selected_creature"][int(self.role_select_input) - 1]
                    self.role_select_input = ""
                    self.client.game_state = GameState.ROLE_DETAIL
            # Enter Number
            elif event.type == pygame.KEYDOWN and self.select_input:
                # Remove a number
                if event.key == pygame.K_BACKSPACE:
                    self.role_select_input = self.role_select_input[:-1]
                # Enter a number
                else:
                    if len(self.role_select_input) < 2: # MAXIMUM ROLE SELECT LENGTH = 2
                        # Only type numbers
                        if event.unicode in "1234567890":
                            self.role_select_input += event.unicode

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # View Roles
        view_roles_font = pygame.font.SysFont("Arial", 30)
        view_roles_surface = view_roles_font.render("View Roles", True, (0, 0, 0))
        view_roles_rect = view_roles_surface.get_rect(topleft = (5, 5))
        self.screen.blit(view_roles_surface, view_roles_rect)
        # Selected Player Roles
        roles_font = pygame.font.SysFont("Arial", 20)
        for role in range(len(self.client.room["selected_player_roles"])):
            roles_surface = roles_font.render(f"{role+1}. {self.client.room["selected_player_roles"][role]}", True, (0, 0, 0))
            roles_rect = roles_surface.get_rect(topleft = (5, 40 + role*20))
            self.screen.blit(roles_surface, roles_rect)
        # Role Select Input Box
        if self.select_input:
            pygame.draw.rect(self.screen, (75, 75, 255), role_select_input_box, 4)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), role_select_input_box, 2)
        # Enter number
        enter_number_font = pygame.font.SysFont("Arial", 20)
        enter_number_surface = enter_number_font.render(f"Enter a role number to select it", True, (0, 0, 0))
        enter_number_rect = enter_number_surface.get_rect(center = (self.width/2, self.height - 95))
        self.screen.blit(enter_number_surface, enter_number_rect)
        # Role Select Input
        role_select_input_font = pygame.font.SysFont("Arial", 30)
        role_select_input_surface = role_select_input_font.render(self.role_select_input, True, (0, 0, 0))
        role_select_input_rect = role_select_input_surface.get_rect(center = (self.width/2, self.height - 55))
        self.screen.blit(role_select_input_surface, role_select_input_rect)
        # Error Text
        error_font = pygame.font.SysFont("Arial", 20)
        error_surface = error_font.render(self.error_text, True, (255, 0, 0))
        error_rect = error_surface.get_rect(center = (self.width/2, self.height - 15))
        self.screen.blit(error_surface, error_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, 30))
        self.screen.blit(back_text_surface, back_text_rect)

        # Music at Night
        if not pygame.mixer.music.get_busy() and self.client.room["night_started"] and not self.client.room["night_ended"]:
            pygame.mixer.music.play()

    # Role Detail
    def role_detail(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, 5, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to View Roles
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.VIEW_ROLES

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Role
        role_font = pygame.font.SysFont("Arial", 50)
        role_surface = role_font.render(self.viewing_role, True, (0, 0, 0))
        role_rect = role_surface.get_rect(topleft = (5, 5))
        self.screen.blit(role_surface, role_rect)
        # Alignment
        alignment_font = pygame.font.SysFont("Arial", 30)
        alignment_surface = alignment_font.render(f"Alignment: {self.viewing_alignment}", True, (0, 0, 0))
        alignment_rect = alignment_surface.get_rect(topleft = (5, 60))
        self.screen.blit(alignment_surface, alignment_rect)
        # Creature
        creature_font = pygame.font.SysFont("Arial", 30)
        creature_surface = creature_font.render(f"Creature: {self.viewing_creature}", True, (0, 0, 0))
        creature_rect = creature_surface.get_rect(topleft = (5, 95))
        self.screen.blit(creature_surface, creature_rect)
        # Description
        description_font = pygame.font.SysFont("Arial", 20)
        description_text = Description.description[self.viewing_role]
        for line in range(len(description_text)):
            description_surface = description_font.render(description_text[line], True, (0, 0, 0))
            description_rect = description_surface.get_rect(topleft = (5, 130 + line*20))
            self.screen.blit(description_surface, description_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, 30))
        self.screen.blit(back_text_surface, back_text_rect)

        # Music at Night
        if not pygame.mixer.music.get_busy() and self.client.room["night_started"] and not self.client.room["night_ended"]:
            pygame.mixer.music.play()

    # Night
    def night(self):
        # Interactives
        # Exit Button
        exit_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Night Order Button
        night_order_button = pygame.Rect(5, self.height - 110, 100, 50)
        # View Roles Button
        view_roles_button = pygame.Rect(5, self.height - 55, 100, 50)
        # Role Select Input
        choice_input_box = pygame.Rect(self.width/2 - 25, self.height - 80, 50, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Exit Game to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and exit_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.MAIN_MENU
                self.client.send(Protocols.Room.LEAVE_ROOM, None)
            # Night Order
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and night_order_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.NIGHT_ORDER
            # View Roles
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and view_roles_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.VIEW_ROLES
            # Choices
            elif self.choosing:
                # Role Select Input Box
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and choice_input_box.collidepoint(pygame.mouse.get_pos()):
                    self.select_input = True
                # Role Unselect Input Box
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not choice_input_box.collidepoint(pygame.mouse.get_pos()):
                    self.select_input = False
                # Attempt Selecting Role
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    # If there are no inputs
                    if len(self.choice_input) <= 0:
                        self.choice_input = ""
                        self.error_text = "Invalid - No Input"
                    # If the input is 0 or lower
                    elif int(self.choice_input) <= 0:
                        self.choice_input = ""
                        self.error_text = "Invalid - Input is 0 or lower"
                    # If the input exceeds the number of roles
                    elif int(self.choice_input) > len(self.choices):
                        self.choice_input = ""
                        self.error_text = "Invalid - Exceeds the number of choices"
                    else:
                        self.error_text = ""
                        self.choice_submit.append(self.choice_input)
                        self.choice_input = ""
                        # Doppelganger Choose
                        if self.client.role_prompt == RolePrompt.DOPPELGANGER_CHOOSE:
                            if self.client.room["username"][int(self.choice_submit[0]) - 1] == self.username:
                                self.choice_submit.pop(0)
                                self.error_text = "Invalid - Can't choose yourself"
                            else:
                                self.client.send(Protocols.NightOrder.DOPPELGANGER, self.client.room["username"][int(self.choice_submit[0]) - 1])
                                self.doppelganger_temp = self.choice_submit.pop(0)
                                self.client.role_prompt = RolePrompt.DOPPELGANGER_LEARN
                        # Lone Wolf Choose
                        elif self.client.role_prompt == RolePrompt.LONE_WOLF_CHOOSE:
                            self.client.role_prompt = RolePrompt.LONE_WOLF_LEARN
                        # Seer Choose Option
                        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_OPTION:
                            if self.choice_submit[0] == "1":
                                self.client.role_prompt = RolePrompt.SEER_CHOOSE_PLAYER
                            else:
                                self.client.role_prompt = RolePrompt.SEER_CHOOSE_FIRST_VOID
                        # Seer Choose Player
                        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_PLAYER:
                            if self.client.room["username"][int(self.choice_submit[1]) - 1] == self.username:
                                self.choice_submit.pop(1)
                                self.error_text = "Invalid - Can't choose yourself"
                            else:
                                self.client.role_prompt = RolePrompt.SEER_LEARN
                        # Seer Choose First Void
                        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_FIRST_VOID:
                            self.client.role_prompt = RolePrompt.SEER_CHOOSE_SECOND_VOID
                        # Seer Choose Second Void
                        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_SECOND_VOID:
                            if self.choice_submit[1] == self.choice_submit[2]:
                                self.choice_submit.pop(2)
                                self.choice_submit.pop(1)
                                self.client.role_prompt = RolePrompt.SEER_CHOOSE_FIRST_VOID
                            else:
                                self.client.role_prompt = RolePrompt.SEER_LEARN
                        # Robber Learn
                        elif self.client.role_prompt == RolePrompt.ROBBER_CHOOSE:
                            if self.client.room["username"][int(self.choice_submit[0]) - 1] == self.username:
                                self.error_text = "Invalid - Can't choose yourself"
                            else:
                                self.client.send(Protocols.NightOrder.ROBBER, (self.username, self.client.room["username"][int(self.choice_submit[0]) - 1]))
                                self.client.role_prompt = RolePrompt.ROBBER_LEARN
                        # Troublemaker First
                        elif self.client.role_prompt == RolePrompt.TROUBLEMAKER_FIRST:
                            if self.client.room["username"][int(self.choice_submit[0]) - 1] == self.username:
                                self.choice_submit.pop(0)
                                self.error_text = "Invalid - Can't choose yourself"
                            else:
                                self.client.role_prompt = RolePrompt.TROUBLEMAKER_SECOND
                        # Troublemaker Second
                        elif self.client.role_prompt == RolePrompt.TROUBLEMAKER_SECOND:
                            if self.client.room["username"][int(self.choice_submit[0]) - 1] == self.username:
                                self.choice_submit.pop(1)
                                self.error_text = "Invalid - Can't choose yourself"
                            elif self.choice_submit[0] == self.choice_submit[1]:
                                self.choice_submit.pop(1)
                                self.choice_submit.pop(0)
                                self.client.role_prompt = RolePrompt.TROUBLEMAKER_FIRST
                            else:
                                self.client.send(Protocols.NightOrder.TROUBLEMAKER, (self.client.room["username"][int(self.choice_submit[0]) - 1], self.client.room["username"][int(self.choice_submit[1]) - 1]))
                                self.client.role_prompt = RolePrompt.NONE
                        # Drunk Choose
                        elif self.client.role_prompt == RolePrompt.DRUNK_CHOOSE:
                            self.client.send(Protocols.NightOrder.DRUNK, (self.username, int(self.choice_submit[0])))
                            self.client.role_prompt = RolePrompt.NONE
                # Enter Number
                elif event.type == pygame.KEYDOWN and self.select_input:
                    # Remove a number
                    if event.key == pygame.K_BACKSPACE:
                        self.choice_input = self.choice_input[:-1]
                    # Enter a number
                    else:
                        if len(self.choice_input) < 2: # MAXIMUM CHOICE INPUT = 2
                            # Only type numbers
                            if event.unicode in "1234567890":
                                self.choice_input += event.unicode

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Timer
        timer_font = pygame.font.SysFont("Arial", 20)
        timer_surface = timer_font.render(f"Time: {self.client.room["wait_time"]}", True, (0, 0, 0))
        timer_rect = timer_surface.get_rect(topleft = (5, 5))
        self.screen.blit(timer_surface, timer_rect)
        # Role Turn
        role_turn_font = pygame.font.SysFont("Arial", 30)
        if self.client.room["number_order"] == -1:
            role_turn_surface = role_turn_font.render("Get ready!", True, (0, 0, 0))
            role_turn_rect = role_turn_surface.get_rect(midtop = (self.width/2, 5))
            self.screen.blit(role_turn_surface, role_turn_rect)
        elif self.client.room["number_order"] >= len(self.client.room["role_order"]):
            role_turn_surface = role_turn_font.render("Waiting to go to day phase...", True, (0, 0, 0))
            role_turn_rect = role_turn_surface.get_rect(midtop = (self.width/2, 5))
            self.screen.blit(role_turn_surface, role_turn_rect)
        else:
            role_turn_surface = role_turn_font.render(f"{self.client.room["role_order"][self.client.room["number_order"]]} Turn", True, (0, 0, 0))
            role_turn_rect = role_turn_surface.get_rect(midtop = (self.width/2, 5))
            self.screen.blit(role_turn_surface, role_turn_rect)
        # Original Role
        original_role_font = pygame.font.SysFont("Arial", 15)
        original_role_surface = original_role_font.render(f"Original Role: {self.client.room["player_roles"][self.client.room["username"].index(self.username)]}", True, (0, 0, 0))
        original_role_rect = original_role_surface.get_rect(topright = (self.width - 5, 5))
        self.screen.blit(original_role_surface, original_role_rect)

        # None
        if self.client.role_prompt == RolePrompt.NONE:
            self.choices = []
            self.choice = ""
            self.choice_submit = []
            self.choosing = False
            self.error_text = ""
            self.select_input = False
            self.doppelganger_temp = None
        # Doppelganger Choose
        elif self.client.role_prompt == RolePrompt.DOPPELGANGER_CHOOSE:
            self.choices = self.client.room["username"].copy()
            if self.username == self.client.room["username"][0]:
                self.choices[1] += " (default)"
            else:
                self.choices[0] += " (default)"
            self.choosing = True
        # Doppelganger Learn
        elif self.client.role_prompt == RolePrompt.DOPPELGANGER_LEARN:
            self.choices = []
            self.choice = ""
            self.choice_submit = []
            self.choosing = False
            self.error_text = ""
            self.select_input = False
            if self.doppelganger_temp == None:
                if self.username == self.client.room["username"][0]:
                    self.doppelganger_temp = "2"
                else:
                    self.doppelganger_temp = "1"
            # Learn Player
            learn_player_font = pygame.font.SysFont("Arial", 30)
            learn_player_surface = learn_player_font.render(f"You learn that {self.client.room["username"][int(self.doppelganger_temp) - 1]} is and you become:", True, (0, 0, 0))
            learn_player_rect = learn_player_surface.get_rect(midtop = (self.width/2, 40))
            self.screen.blit(learn_player_surface, learn_player_rect)
            # Player Role
            player_role_font = pygame.font.SysFont("Arial", 30)
            player_role_surface = player_role_font.render(self.client.room["player_roles_final"][int(self.doppelganger_temp) - 1], True, (0, 0, 0))
            player_role_rect = player_role_surface.get_rect(midtop = (self.width/2, 75))
            self.screen.blit(player_role_surface, player_role_rect)
        # Werewolves
        elif self.client.role_prompt == RolePrompt.WEREWOLVES:
            self.choices = []
            self.choice = ""
            self.choice_submit = []
            self.choosing = False
            self.error_text = ""
            self.select_input = False
            # Werewolves
            werewolves_font = pygame.font.SysFont("Arial", 30)
            werewolves_surface = werewolves_font.render("Werewolves:", True, (0, 0, 0))
            werewolves_rect = werewolves_surface.get_rect(topleft = (5, 30))
            self.screen.blit(werewolves_surface, werewolves_rect)
            # Werewolf Player
            werewolf_players = []
            for player_creature in range(len(self.client.room["creature"][:-3])):
                if self.client.room["creature"][player_creature] == "Werewolf" or (self.client.room["creature"][player_creature] == "Doppelganger" and self.client.room["doppelganger_creature"] == "Werewolf"):
                    werewolf_players.append(self.client.room["username"][player_creature])
            # Show Werewolf Players
            werewolf_players_font = pygame.font.SysFont("Arial", 20)
            for werewolf_player in range(len(werewolf_players)):
                werewolf_players_surface = werewolf_players_font.render(f"{werewolf_player+1}. {werewolf_players[werewolf_player]}", True, (0, 0, 0))
                werewolf_players_rect = werewolf_players_surface.get_rect(topleft = (5, 65 + werewolf_player*20))
                self.screen.blit(werewolf_players_surface, werewolf_players_rect)
        # Lone Wolf Choose
        elif self.client.role_prompt == RolePrompt.LONE_WOLF_CHOOSE:
            self.choices = ["Void 1", "Void 2", "Void 3"]
            self.choosing = True
            # Lone Wolf
            lone_wolf_font = pygame.font.SysFont("Arial", 30)
            lone_wolf_surface = lone_wolf_font.render("You are the only wolf!", True, (0, 0, 0))
            lone_wolf_rect = lone_wolf_surface.get_rect(midtop = (self.width/2, 40))
            self.screen.blit(lone_wolf_surface, lone_wolf_rect)
        # Lone Wolf Learn
        elif self.client.role_prompt == RolePrompt.LONE_WOLF_LEARN:
            self.choices = []
            self.choice = ""
            self.choosing = False
            self.error_text = ""
            self.select_input = False
            # Learn
            learn_font = pygame.font.SysFont("Arial", 30)
            learn_surface = learn_font.render(f"You learn that Void {self.choice_submit[0]} is:", True, (0, 0, 0))
            learn_rect = learn_surface.get_rect(midtop = (self.width/2, 40))
            self.screen.blit(learn_surface, learn_rect)
            # Role
            void_role_font = pygame.font.SysFont("Arial", 30)
            void_role_surface = void_role_font.render(self.client.room["player_roles_final"][len(self.client.room["username"]) - 1 + int(self.choice_submit[0])], True, (0, 0, 0))
            void_role_rect = void_role_surface.get_rect(midtop = (self.width/2, 75))
            self.screen.blit(void_role_surface, void_role_rect)
        # Masons
        elif self.client.role_prompt == RolePrompt.MASONS:
            # Masons
            masons_font = pygame.font.SysFont("Arial", 30)
            masons_surface = masons_font.render("Mason:", True, (0, 0, 0))
            masons_rect = masons_surface.get_rect(topleft = (5, 30))
            self.screen.blit(masons_surface, masons_rect)
            mason_players = []
            for player_roles in range(len(self.client.room["player_roles"][:-3])):
                if self.client.room["player_roles"][player_roles] == "Mason" or (player_roles == "Doppelganger" and self.client.room["doppelganger_role"] == "Mason"):
                    mason_players.append(self.client.room["username"][player_roles])
            # Show Mason Players
            mason_players_font = pygame.font.SysFont("Arial", 20)
            for mason_player in range(len(mason_players)):
                mason_players_surface = mason_players_font.render(f"{mason_player+1}. {mason_players[mason_player]}", True, (0, 0, 0))
                mason_players_rect = mason_players_surface.get_rect(topleft = (5, 65 + mason_player*20))
                self.screen.blit(mason_players_surface, mason_players_rect)
        # Seer Choose Option
        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_OPTION:
            self.choices = ["Look at a player's role", "Look at 2 void roles"]
            self.choosing = True
        # Seer Choose Player
        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_PLAYER:
            self.choices = self.client.room["username"].copy()
            self.choosing = True
        # Seer Choose First Void
        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_FIRST_VOID:
            self.choices = ["Void 1", "Void 2", "Void 3"]
            self.choosing = True
        # Seer Choose Second Void
        elif self.client.role_prompt == RolePrompt.SEER_CHOOSE_SECOND_VOID:
            self.choices = ["Void 1", "Void 2", "Void 3"]
            self.choices[int(self.choice_submit[1]) - 1] += " - CHOSEN"
            self.choosing = True
        # Seer Learn
        elif self.client.role_prompt == RolePrompt.SEER_LEARN:
            self.choices = []
            self.choice = ""
            self.choosing = False
            self.error_text = ""
            self.select_input = False
            # Player
            if self.choice_submit[0] == "1":
                # Learn Player
                learn_player_font = pygame.font.SysFont("Arial", 30)
                learn_player_surface = learn_player_font.render(f"You learn that {self.client.room["username"][int(self.choice_submit[1]) - 1]} is:", True, (0, 0, 0))
                learn_player_rect = learn_player_surface.get_rect(midtop = (self.width/2, 40))
                self.screen.blit(learn_player_surface, learn_player_rect)
                # Player Role
                player_role_font = pygame.font.SysFont("Arial", 30)
                player_role_surface = player_role_font.render(self.client.room["player_roles_final"][int(self.choice_submit[1]) - 1], True, (0, 0, 0))
                player_role_rect = player_role_surface.get_rect(midtop = (self.width/2, 75))
                self.screen.blit(player_role_surface, player_role_rect)
            else:
                # Learn 2 Void Roles
                learn_void_font = pygame.font.SysFont("Arial", 30)
                learn_void_surface = learn_void_font.render(f"You learn that Void {self.choice_submit[1]} and Void {self.choice_submit[2]} is:", True, (0, 0, 0))
                learn_void_rect = learn_void_surface.get_rect(midtop = (self.width/2, 40))
                self.screen.blit(learn_void_surface, learn_void_rect)
                # First Void Role
                first_void_role_font = pygame.font.SysFont("Arial", 30)
                first_void_role_surface = first_void_role_font.render(f"Void {self.choice_submit[1]}: {self.client.room["player_roles_final"][len(self.client.room["username"]) - 1 + int(self.choice_submit[1])]}", True, (0, 0, 0))
                first_void_role_rect = first_void_role_surface.get_rect(midtop = (self.width/2, 75))
                self.screen.blit(first_void_role_surface, first_void_role_rect)
                # Second Void Role
                second_void_role_font = pygame.font.SysFont("Arial", 30)
                second_void_role_surface = second_void_role_font.render(f"Void {self.choice_submit[2]}: {self.client.room["player_roles_final"][len(self.client.room["username"]) - 1 + int(self.choice_submit[2])]}", True, (0, 0, 0))
                second_void_role_rect = second_void_role_surface.get_rect(midtop = (self.width/2, 105))
                self.screen.blit(second_void_role_surface, second_void_role_rect)
        # Robber Choose
        elif self.client.role_prompt == RolePrompt.ROBBER_CHOOSE:
            self.choices = self.client.room["username"].copy()
            self.choosing = True
        # Robber Learn
        elif self.client.role_prompt == RolePrompt.ROBBER_LEARN:
            self.choices = []
            self.choice = ""
            self.choosing = False
            self.error_text = ""
            self.select_input = False
            # Your new role
            your_new_role_font = pygame.font.SysFont("Arial", 30)
            your_new_role_surface = your_new_role_font.render("Your new role is:", True, (0, 0, 0))
            your_new_role_rect = your_new_role_surface.get_rect(midtop = (self.width/2, 40))
            self.screen.blit(your_new_role_surface, your_new_role_rect)
            # New Role
            new_role_font = pygame.font.SysFont("Arial", 30)
            new_role_surface = new_role_font.render(self.client.room["player_roles_final"][self.client.room["username"].index(self.username)], True, (0, 0, 0))
            new_role_rect = new_role_surface.get_rect(midtop = (self.width/2, 75))
            self.screen.blit(new_role_surface, new_role_rect)
        # Troublemaker First
        elif self.client.role_prompt == RolePrompt.TROUBLEMAKER_FIRST:
            self.choices = self.client.room["username"].copy()
            self.choosing = True
        # Troublemaker Second
        elif self.client.role_prompt == RolePrompt.TROUBLEMAKER_SECOND:
            self.choices = self.client.room["username"].copy()
            self.choices[int(self.choice_submit[0]) - 1] += " - CHOSEN"
            self.choosing = True
        # Drunk Choose
        elif self.client.role_prompt == RolePrompt.DRUNK_CHOOSE:
            self.choices = ["Void 1 (default)", "Void 2", "Void 3"]
            self.choosing = True
        # Insomniac Learn
        elif self.client.role_prompt == RolePrompt.INSOMNIAC_LEARN:
            self.choices = []
            self.choice = ""
            self.choosing = False
            self.error_text = ""
            self.select_input = False
            # Your new role
            your_new_role_font = pygame.font.SysFont("Arial", 30)
            your_new_role_surface = your_new_role_font.render("Your new role is:", True, (0, 0, 0))
            your_new_role_rect = your_new_role_surface.get_rect(midtop = (self.width/2, 40))
            self.screen.blit(your_new_role_surface, your_new_role_rect)
            # New Role
            new_role_font = pygame.font.SysFont("Arial", 30)
            new_role_surface = new_role_font.render(self.client.room["player_roles_final"][self.client.room["username"].index(self.username)], True, (0, 0, 0))
            new_role_rect = new_role_surface.get_rect(midtop = (self.width/2, 75))
            self.screen.blit(new_role_surface, new_role_rect)

        # Choosing
        if self.choosing:
            # Choose
            choose_font = pygame.font.SysFont("Arial", 30)
            choose_surface = choose_font.render("Choose:", True, (0, 0, 0))
            choose_rect = choose_surface.get_rect(topleft = (5, 30))
            self.screen.blit(choose_surface, choose_rect)
            # Show Choices
            choices_font = pygame.font.SysFont("Arial", 20)
            for choice in range(len(self.choices)):
                choices_surface = choices_font.render(f"{choice+1}. {self.choices[choice]}", True, (0, 0, 0))
                choices_rect = choices_surface.get_rect(topleft = (5, 65 + choice*20))
                self.screen.blit(choices_surface, choices_rect)
            # Role Select Input Box
            if self.select_input:
                pygame.draw.rect(self.screen, (75, 75, 255), choice_input_box, 4)
            else:
                pygame.draw.rect(self.screen, (0, 0, 0), choice_input_box, 2)
            # Enter number
            enter_number_font = pygame.font.SysFont("Arial", 20)
            enter_number_surface = enter_number_font.render(f"Enter a number to select it", True, (0, 0, 0))
            enter_number_rect = enter_number_surface.get_rect(center = (self.width/2, self.height - 95))
            self.screen.blit(enter_number_surface, enter_number_rect)
            # Choice Input
            choice_input_font = pygame.font.SysFont("Arial", 30)
            choice_input_surface = choice_input_font.render(self.choice_input, True, (0, 0, 0))
            choice_input_rect = choice_input_surface.get_rect(center = (self.width/2, self.height - 55))
            self.screen.blit(choice_input_surface, choice_input_rect)
            # Error Text
            error_font = pygame.font.SysFont("Arial", 20)
            error_surface = error_font.render(self.error_text, True, (255, 0, 0))
            error_rect = error_surface.get_rect(center = (self.width/2, self.height - 15))
            self.screen.blit(error_surface, error_rect)

        # Night Order Button
        pygame.draw.rect(self.screen, (200, 200, 200), night_order_button)
        pygame.draw.rect(self.screen, (100, 100, 100), night_order_button, 10)
        night_order_text_font = pygame.font.SysFont("Arial", 20)
        night_order_text_surface = night_order_text_font.render("Night Order", True, (0, 0, 0))
        night_order_text_rect = night_order_text_surface.get_rect(center = (55, self.height - 85))
        self.screen.blit(night_order_text_surface, night_order_text_rect)
        # View Roles Button
        pygame.draw.rect(self.screen, (200, 200, 200), view_roles_button)
        pygame.draw.rect(self.screen, (100, 100, 100), view_roles_button, 10)
        view_roles_text_font = pygame.font.SysFont("Arial", 20)
        view_roles_text_surface = view_roles_text_font.render("View Roles", True, (0, 0, 0))
        view_roles_text_rect = view_roles_text_surface.get_rect(center = (55, self.height - 30))
        self.screen.blit(view_roles_text_surface, view_roles_text_rect)
        # Exit Button
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button)
        pygame.draw.rect(self.screen, (255, 127, 127), exit_button, 10)
        exit_text_font = pygame.font.SysFont("Arial", 25)
        exit_text_surface = exit_text_font.render("Exit", True, (0, 0, 0))
        exit_text_rect = exit_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(exit_text_surface, exit_text_rect)

        # Music
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
    
    # Day
    def day(self):
        # Interactives
        # Exit Button
        exit_button = pygame.Rect(self.width - 105, self.height - 55, 100, 50)
        # Role Select Input
        vote_input_box = pygame.Rect(self.width/2 - 25, self.height - 185, 50, 50)
        # Ready Button
        ready_button = pygame.Rect(self.width/2 - 100, self.height - 105, 200, 100)
        # Night Order Button
        night_order_button = pygame.Rect(5, self.height - 110, 100, 50)
        # View Roles Button
        view_roles_button = pygame.Rect(5, self.height - 55, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Exit Game to Main Menu
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and exit_button.collidepoint(pygame.mouse.get_pos()):
                self.error_text = ""
                self.select_input = False
                self.client.game_state = GameState.MAIN_MENU
                self.client.send(Protocols.Room.LEAVE_ROOM, None)
            # Ready or Unready
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and ready_button.collidepoint(pygame.mouse.get_pos()):
                self.client.send(Protocols.Room.READY, None)
            # Night Order
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and night_order_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.NIGHT_ORDER
            # View Roles
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and view_roles_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.VIEW_ROLES
            # Role Select Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and vote_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = True
            # Role Unselect Input Box
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not vote_input_box.collidepoint(pygame.mouse.get_pos()):
                self.select_input = False
            # Attempt Selecting Role
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # If there are no inputs
                if len(self.vote_input) <= 0:
                    self.vote_input = ""
                    self.error_text = "Invalid - No Input"
                # If the input is 0 or lower
                elif int(self.vote_input) <= 0:
                    self.vote_input = ""
                    self.error_text = "Invalid - Input is 0 or lower"
                # If the input exceeds the number of players
                elif int(self.vote_input) > len(self.client.room["username"]):
                    self.vote_input = ""
                    self.error_text = "Invalid - Exceeds the number of players"
                elif self.client.room["username"][int(self.vote_input) - 1] == self.username:
                    self.vote_input = ""
                    self.error_text = "Invalid - Can't choose yourself"
                else:
                    self.error_text = ""
                    self.client.send(Protocols.GameStart.VOTE, (self.username, int(self.vote_input) - 1))
                    self.vote_input = ""
            # Enter Number
            elif event.type == pygame.KEYDOWN and self.select_input:
                # Remove a number
                if event.key == pygame.K_BACKSPACE:
                    self.vote_input = self.vote_input[:-1]
                # Enter a number
                else:
                    if len(self.vote_input) < 2: # MAXIMUM ROLE SELECT LENGTH = 2
                        # Only type numbers
                        if event.unicode in "1234567890":
                            self.vote_input += event.unicode

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Timer
        timer_font = pygame.font.SysFont("Arial", 20)
        timer_surface = timer_font.render(f"Time: {self.client.room["wait_time"]}", True, (0, 0, 0))
        timer_rect = timer_surface.get_rect(topleft = (5, 5))
        self.screen.blit(timer_surface, timer_rect)
        # Discuss and choose who to vote
        choose_vote_font = pygame.font.SysFont("Arial", 30)
        choose_vote_surface = choose_vote_font.render("Discuss and choose who to vote!", True, (0, 0, 0))
        choose_vote_rect = choose_vote_surface.get_rect(midtop = (self.width/2, 5))
        self.screen.blit(choose_vote_surface, choose_vote_rect)
        players_font = pygame.font.SysFont("Arial", 20)
        for player in range(len(self.client.room["username"])):
            players_surface = players_font.render(f"{player+1}. {self.client.room["username"][player]} - {"Ready" if self.client.room["ready"][player] else "Not Ready"} {"[CHOSEN]" if player == self.client.room["voting"][self.client.room["username"].index(self.username)] else ""}", True, (0, 0, 0))
            players_rect = players_surface.get_rect(topleft = (5, 40 + player*20))
            self.screen.blit(players_surface, players_rect)
        # Original Role
        original_role_font = pygame.font.SysFont("Arial", 15)
        original_role_surface = original_role_font.render(f"Original Role: {self.client.room["player_roles"][self.client.room["username"].index(self.username)]}", True, (0, 0, 0))
        original_role_rect = original_role_surface.get_rect(topright = (self.width - 5, 5))
        self.screen.blit(original_role_surface, original_role_rect)
        # Vote Input Box
        if self.select_input:
            pygame.draw.rect(self.screen, (75, 75, 255), vote_input_box, 4)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), vote_input_box, 2)
        # Enter number
        enter_number_font = pygame.font.SysFont("Arial", 20)
        enter_number_surface = enter_number_font.render(f"Enter a player number to vote that player", True, (0, 0, 0))
        enter_number_rect = enter_number_surface.get_rect(center = (self.width/2, self.height - 200))
        self.screen.blit(enter_number_surface, enter_number_rect)
        # Vote Input
        vote_input_font = pygame.font.SysFont("Arial", 30)
        vote_input_surface = vote_input_font.render(self.vote_input, True, (0, 0, 0))
        vote_input_rect = vote_input_surface.get_rect(center = (self.width/2, self.height - 160))
        self.screen.blit(vote_input_surface, vote_input_rect)
        # Error Text
        error_font = pygame.font.SysFont("Arial", 20)
        error_surface = error_font.render(self.error_text, True, (255, 0, 0))
        error_rect = error_surface.get_rect(center = (self.width/2, self.height - 120))
        self.screen.blit(error_surface, error_rect)
        # Ready Button
        pygame.draw.rect(self.screen, (0, 255, 0), ready_button)
        pygame.draw.rect(self.screen, (127, 255, 127), ready_button, 20)
        ready_text_font = pygame.font.SysFont("Arial", 50)
        ready_text_surface = ready_text_font.render("Ready", True, (0, 0, 0))
        ready_text_rect = ready_text_surface.get_rect(center = (self.width/2, self.height - 55))
        self.screen.blit(ready_text_surface, ready_text_rect)
        # Night Order Button
        pygame.draw.rect(self.screen, (200, 200, 200), night_order_button)
        pygame.draw.rect(self.screen, (100, 100, 100), night_order_button, 10)
        night_order_text_font = pygame.font.SysFont("Arial", 20)
        night_order_text_surface = night_order_text_font.render("Night Order", True, (0, 0, 0))
        night_order_text_rect = night_order_text_surface.get_rect(center = (55, self.height - 85))
        self.screen.blit(night_order_text_surface, night_order_text_rect)
        # View Roles Button
        pygame.draw.rect(self.screen, (200, 200, 200), view_roles_button)
        pygame.draw.rect(self.screen, (100, 100, 100), view_roles_button, 10)
        view_roles_text_font = pygame.font.SysFont("Arial", 20)
        view_roles_text_surface = view_roles_text_font.render("View Roles", True, (0, 0, 0))
        view_roles_text_rect = view_roles_text_surface.get_rect(center = (55, self.height - 30))
        self.screen.blit(view_roles_text_surface, view_roles_text_rect)
        # Exit Button
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button)
        pygame.draw.rect(self.screen, (255, 127, 127), exit_button, 10)
        exit_text_font = pygame.font.SysFont("Arial", 25)
        exit_text_surface = exit_text_font.render("Exit", True, (0, 0, 0))
        exit_text_rect = exit_text_surface.get_rect(center = (self.width - 55, self.height - 30))
        self.screen.blit(exit_text_surface, exit_text_rect)

        # Stop Music
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    
    # End
    def end(self):
        # Interactives
        # Back Button
        back_button = pygame.Rect(self.width - 105, 5, 100, 50)
        # Events
        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                self.client.close()
                pygame.quit()
                exit()
            # Back to Room
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and back_button.collidepoint(pygame.mouse.get_pos()):
                self.client.game_state = GameState.ROOM

        # Draw
        # Background
        self.screen.fill((255, 255, 255))
        # Winners
        winners_font = pygame.font.SysFont("Arial", 30)
        winners_text = ""
        for winner in self.client.room["alignment_winners"]:
            winners_text += winner
            winners_text += ", "
        winners_text = winners_text[:-2]
        winners_text += " win!"
        winners_surface = winners_font.render(winners_text, True, (0, 0, 0))
        winners_rect = winners_surface.get_rect(midtop = (self.width / 2, 5))
        self.screen.blit(winners_surface, winners_rect)
        # Player
        player_font = pygame.font.SysFont("Arial", 15)
        for end_player in range(len(self.client.room["end_players"])):
            player_text = f"{end_player + 1}. {self.client.room["end_players"][end_player]} - Original:{self.client.room["player_roles"][end_player]}"
            if self.client.room["player_roles"][end_player] == "Doppelganger":
                player_text += f"({self.client.room["doppelganger_role"]})"
            player_text += f" - Final:{self.client.room["player_roles_final"][end_player]}"
            if self.client.room["player_roles_final"][end_player] == "Doppelganger":
                player_text += f"({self.client.room["doppelganger_role"]})"
            player_text += f" - {"Alive" if self.client.room["living"][end_player] else "Dead"} - {"WIN" if self.client.room["player_winners"][end_player] else "LOSE"}"
            player_surface = player_font.render(player_text, True, (0, 0, 0))
            player_rect = player_surface.get_rect(topleft = (5, 40 + end_player * 15))
            self.screen.blit(player_surface, player_rect)
        # Back Button
        pygame.draw.rect(self.screen, (255, 0, 0), back_button)
        pygame.draw.rect(self.screen, (255, 127, 127), back_button, 10)
        back_text_font = pygame.font.SysFont("Arial", 25)
        back_text_surface = back_text_font.render("Back", True, (0, 0, 0))
        back_text_rect = back_text_surface.get_rect(center = (self.width - 55, 30))
        self.screen.blit(back_text_surface, back_text_rect)
        self.vote_input = ""

    # Running game
    def run(self):
        # Start up
        self.client.connect()

        # Load Music
        pygame.mixer.music.load("audio/fantasy.mp3")
        pygame.mixer.music.set_volume(0.2)

        while True:
            self.clock.tick(self.FPS)
            # Screens
            # Loading
            if not self.client.connected:
                self.loading()
            else:
                # Main Menu
                if self.client.game_state == GameState.MAIN_MENU:
                    self.main_menu()
                # How To Play
                elif self.client.game_state == GameState.HOW_TO_PLAY:
                    self.how_to_play()
                # Credits
                elif self.client.game_state == GameState.CREDITS:
                    self.credits()
                # Host or Join
                elif self.client.game_state == GameState.HOST_OR_JOIN:
                    self.host_or_join()
                # Password
                elif self.client.game_state == GameState.PASSWORD:
                    self.password()
                # Room
                elif self.client.game_state == GameState.ROOM:
                    if self.client.room != None:
                        self.room()
                    else:
                        self.loading()
                # Player Left
                elif self.client.game_state == GameState.PLAYER_LEFT:
                    self.player_left()
                # Select Roles
                elif self.client.game_state == GameState.SELECT_ROLES:
                    self.select_roles()
                # Get Role
                elif self.client.game_state == GameState.GET_ROLE:
                    self.get_role()
                # Night Order
                elif self.client.game_state == GameState.NIGHT_ORDER:
                    self.night_order()
                # View Roles
                elif self.client.game_state == GameState.VIEW_ROLES:
                    self.view_roles()
                # Role Detail
                elif self.client.game_state == GameState.ROLE_DETAIL:
                    self.role_detail()
                # Night
                elif self.client.game_state == GameState.NIGHT:
                    self.night()
                # Day
                elif self.client.game_state == GameState.DAY:
                    self.day()
                # End
                elif self.client.game_state == GameState.END:
                    self.end()
            
            # Update
            pygame.display.update()