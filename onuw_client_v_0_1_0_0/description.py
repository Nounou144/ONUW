class Description:
    description = {
        "Doppelganger": ["Wake and MUST choose a player:", "Look and copy that player's role, alignment, creature and night action.", "If you are a Villager, Tanner or Hunter, you do not wake up anymore.", "If you become a Mason or Werewolf, you wake and know the others of your type.", "If you are a Minion, you know the other werewolf.", "If you are an Insomniac, you view your role right after the original Insomniac.", "If you have a night action, you do it now.", "If you are a Tanner, you are in your own team and must vote yourself out."],
        "Werewolf": ["Wake with the other werewolves.", "If you are the only werewolf, choose and look at a void role."],
        "Minion": ["Wake and knows all werewolves.", "If there are no other werewolves at the end of the night,", " you win when at least one player (not yourself) dies.", "If there is a rare case where there is a Doppelganger Minion", "and a Minion together with no werewolves,", "they win when at least one player (including themselves) dies."],
        "Mason": ["Wake and know the other mason (if any)."],
        "Seer": ["Wake and may choose either:", "- Look at another player's role;", "- Looks at 2 void roles."],
        "Robber": ["Wake and may choose a player:", "Exchange your role with their role and view your new role.", "You do not gain their night action."],
        "Troublemaker": ["Wake and may exchange 2 other players' role."],
        "Drunk": ["Wake and MUST choose and exchange their role with a void role.", "You do not know your new role."],
        "Insomniac": ["Wake and view your own role."],
        "Villager": ["Does nothing."],
        "Hunter": ["Does nothing at night.", "If you are voted out, the player you are voting is also killed."],
        "Tanner": ["Does nothing at night.", "You win if you die.", "Werewolves can't win if you win."]
    }