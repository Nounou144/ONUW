class Protocols:
    # Main Menu
    class Main_Menu:
        USERNAME = "protocol.username"
    # Room
    class Room:
        CREATE_ROOM = "protocol.create_room"
        JOIN_ROOM = "protocol.join_room"
        INVALID_PASSWORD = "protocol.invalid_password"
        MAXIMUM_PLAYERS = "protocol.maximum_players"
        USERNAME_ALREADY_TAKEN = "protocol.username_already_taken"
        ROOM = "protocol.room"
        LEAVE_ROOM = "protocol.leave_room"
        READY = "protocol.ready"
        GAME_ALREADY_STARTED = "protocol.game_already_started"
    # Game Start
    class GameStart:
        PLAYER_LEFT = "protocol.player_left"
        SELECT_ROLES = "protocol.select_roles"
        ROLE_SELECTED = "protocol.role_selected"
        GET_ROLE = "protocol.get_role"
        NIGHT = "protocol.night"
        DAY = "protocol.day"
        VOTE = "protocol.vote"
        END = "protocol.end"
    class NightOrder:
        REMOVE_PROMPT = "protocol.remove_prompt"
        DOPPELGANGER = "protocol.doppelganger"
        DOPPELGANGER_LEARN = "protocol.doppelganger_learn"
        DOPPELGANGER_ACTION = "protocol.doppelganger_action"
        DOPPELGANGER_MINION = "protocol.doppelganger_minion"
        WEREWOLVES = "protocol.werewolves"
        MINION = "protocol.minion"
        MASONS = "protocol.masons"
        SEER = "protocol.seer"
        ROBBER = "protocol.robber"
        TROUBLEMAKER = "protocol.troublemaker"
        DRUNK = "protocol.drunk"
        INSOMNIAC = "protocol.insomniac"
        DOPPELGANGER_INSOMNIAC = "protocol.doppelganger_insomniac"