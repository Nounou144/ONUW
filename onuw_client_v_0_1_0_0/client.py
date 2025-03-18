import socket
import threading
import pickle
from protocols import Protocols
from game_state import GameState
from role_prompt import RolePrompt

class Client:
    # Initiate Client
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        self.connected = False
        self.closed = False

        # Game State
        self.game_state = GameState.MAIN_MENU

        # Room
        self.room = None

        # Role Prompt
        self.role_prompt = RolePrompt.NONE
    
    # Start a thread to receive
    def run(self):
        print("Client created!")
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
    
    # Client Bootup
    def connect(self):
        self.connected = True

    # Receive Responses
    def receive(self):
        while True:
            try:
                # Get Response
                response = pickle.loads(self.server.recv(4096))
                self.handle_response(response)
            except:
                # Server likely disconnected
                print("Server Disconnected...")
                break
        
        self.close()
    
    # Handle Responses
    def handle_response(self, response):
        r_type = response.get("type")
        data = response.get("data")

        # Room
        # Get room
        if r_type == Protocols.Room.ROOM:
            self.room = data
        # Invalid Password
        elif r_type == Protocols.Room.INVALID_PASSWORD:
            print("[INVALID PASSWORD]: Password is not found.")
        # Maximum players
        elif r_type == Protocols.Room.MAXIMUM_PLAYERS:
            print("[MAXIMUM PLAYERS]: The room reached the maximum amount of players.")
        # Game Already Started
        elif r_type == Protocols.Room.GAME_ALREADY_STARTED:
            print("[GAME ALREADY STARTED]: The game has already started.")
        # Username Already Taken
        elif r_type == Protocols.Room.USERNAME_ALREADY_TAKEN:
            print("[USERNAME ALREADY TAKEN]: Your username is already used by another player.")
        
        # Game Start
        # Player Left
        elif r_type == Protocols.GameStart.PLAYER_LEFT:
            if self.room["role_picked"]:
                self.game_state = GameState.PLAYER_LEFT
            else:
                self.game_state = GameState.ROOM
        # Select Roles
        elif r_type == Protocols.GameStart.SELECT_ROLES:
            self.game_state = GameState.SELECT_ROLES
        # Get Role
        elif r_type == Protocols.GameStart.GET_ROLE:
            self.game_state = GameState.GET_ROLE
        # Night
        elif r_type == Protocols.GameStart.NIGHT:
            self.game_state = GameState.NIGHT
        # Day
        elif r_type == Protocols.GameStart.DAY:
            if self.game_state == GameState.NIGHT:
                self.game_state = GameState.DAY
        # End
        elif r_type == Protocols.GameStart.END:
            self.game_state = GameState.END

        # Night Order
        # Remove Prompt
        elif r_type == Protocols.NightOrder.REMOVE_PROMPT:
            self.role_prompt = RolePrompt.NONE
        # Doppelganger
        elif r_type == Protocols.NightOrder.DOPPELGANGER:
            self.role_prompt = RolePrompt.DOPPELGANGER_CHOOSE
        # Doppelganger Learn
        elif r_type == Protocols.NightOrder.DOPPELGANGER_LEARN:
            self.role_prompt = RolePrompt.DOPPELGANGER_LEARN
        # Doppelganger Action
        elif r_type == Protocols.NightOrder.DOPPELGANGER_ACTION:
            doppelganger_role = self.room["doppelganger_role"]
            if doppelganger_role == "Seer":
                self.role_prompt = RolePrompt.SEER_CHOOSE_OPTION
            elif doppelganger_role == "Robber":
                self.role_prompt = RolePrompt.ROBBER_CHOOSE
            elif doppelganger_role == "Troublemaker":
                self.role_prompt = RolePrompt.TROUBLEMAKER_FIRST
            elif doppelganger_role == "Drunk":
                self.role_prompt = RolePrompt.DRUNK_CHOOSE
        # Doppelganger Insomniac
        elif r_type == Protocols.NightOrder.DOPPELGANGER_MINION:
            if self.room["doppelganger_role"] == "Minion":
                self.role_prompt = RolePrompt.WEREWOLVES
        # Werewolves
        elif r_type == Protocols.NightOrder.WEREWOLVES:
            # Find if lone wolf
            number_of_wolves = 0
            for player_roles in self.room["player_roles"][:-3]:
                if player_roles == "Werewolf" or (player_roles == "Doppelganger" and self.room["doppelganger_role"] == "Werewolf"):
                    number_of_wolves += 1
            if number_of_wolves == 1:
                self.role_prompt = RolePrompt.LONE_WOLF_CHOOSE
            else:
                self.role_prompt = RolePrompt.WEREWOLVES
        # Minion
        elif r_type == Protocols.NightOrder.MINION:
            self.role_prompt = RolePrompt.WEREWOLVES
        # Masons
        elif r_type == Protocols.NightOrder.MASONS:
            self.role_prompt = RolePrompt.MASONS
        # Seer
        elif r_type == Protocols.NightOrder.SEER:
            self.role_prompt = RolePrompt.SEER_CHOOSE_OPTION
        # Robber
        elif r_type == Protocols.NightOrder.ROBBER:
            self.role_prompt = RolePrompt.ROBBER_CHOOSE
        # Troublemaker
        elif r_type == Protocols.NightOrder.TROUBLEMAKER:
            self.role_prompt = RolePrompt.TROUBLEMAKER_FIRST
        # Drunk
        elif r_type == Protocols.NightOrder.DRUNK:
            self.role_prompt = RolePrompt.DRUNK_CHOOSE
        # Insomniac
        elif r_type == Protocols.NightOrder.INSOMNIAC:
            self.role_prompt = RolePrompt.INSOMNIAC_LEARN
        # Doppelganger Insomniac
        elif r_type == Protocols.NightOrder.DOPPELGANGER_INSOMNIAC:
            if self.room["doppelganger_role"] == "Insomniac":
                self.role_prompt = RolePrompt.INSOMNIAC_LEARN
            
    # Sending Messages
    def send(self, r_type, data):
        message = {"type": r_type, "data": data}
        print(f"[SENDING]: {message}")
        message = pickle.dumps(message)
        self.server.sendall(message)
    
    # Close Client
    def close(self):
        if not self.closed:
            self.closed = True
            self.send(Protocols.Room.LEAVE_ROOM, None)
            print(f"Disconnected from {self.server}")
            self.server.close()