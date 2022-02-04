"""
A non-UI (text-based) way of playing.
    This is functionally similar to ui.py in terms of processing actions
    but it lacks the 'automatic get_next_sprite() calling'. Instead, there's
    the choice to update the UI (which also happens after any attacks/actions
    are called).

Run this file to play the game.

This file simply calls on pygame and the code from game.py, which contains
all of your client code.
"""
import game

def start_game():
    """
    Start and initialize the game
    """
    game.set_up_game()

def update_game():
    """
    Update the game's UI.
    """
    to_draw = []
    
    draw_parameters = game.update_ui()
    
    p1_sprite = draw_parameters['p1_sprite']
    p1_hp = draw_parameters['p1_hp']
    p1_sp = draw_parameters['p1_sp']
    p1_name = draw_parameters['p1_name']
    
    p1_label = ("{}\nHP: {}\nSP: {}\nSprite: {}".format(p1_name,
                                                        p1_hp,
                                                        p1_sp,
                                                        p1_sprite))

    to_draw.append(p1_label)
    
    p2_sprite = draw_parameters['p2_sprite']
    p2_hp = draw_parameters['p2_hp']
    p2_sp = draw_parameters['p2_sp']
    p2_name = draw_parameters['p2_name']
    
    p2_label = ("{}\nHP: {}\nSP: {}\nSprite: {}".format(p2_name,
                                                        p2_hp,
                                                        p2_sp,
                                                        p2_sprite))
    
    to_draw.append(p2_label)
    
    # Update the current player and available actions
    if not game.GAME_IS_OVER:
        actions = draw_parameters['actions']
        current_player = draw_parameters['current_player']
        action_label = ["Current Character: {}".format(current_player),
                        "Available Actions: {}".format(", ".join(actions))]
        to_draw.append("\n".join(action_label))
    else:
        game_label = ["Game over!"]
        winner = game.GAME_WINNER
        if winner:
            game_label.append("The winner is {}!".format(winner.get_name()))
        else:
            game_label.append("The game ended in a tie!")
        to_draw.append("\n".join(game_label))
    
    print("\n".join(to_draw))
    print("-" * 20)
        

if __name__ == '__main__':
    start_game()
    update_game()
    
    while True:
        # If the current player isn't using a manual playstyle, pick a move
        if (not game.GAME_IS_OVER):
            if (not game.BATTLE_QUEUE.is_over() and 
                not game.BATTLE_QUEUE.peek().playstyle.is_manual):
                game.perform_attack()
                update_game()
            else:
                # Prompt for an action (until a valid one is provided)
                prompt = ("Select an action (A: Attack, S: Special Attack, " +
                          "U: Update Display, Q: Quit Game): ")
                k = input(prompt).strip().upper()
                
                game.LAST_KEY_PRESSED = k
                game.perform_attack()
                
                if (k in ['A', 'S', 'U']):
                    update_game()
                
                if k == 'Q':
                    break
        else:
            prompt = ("Select an action (U: Update Display, Q: Quit Game): ")
            k = input(prompt).strip().upper()
            
            if k == 'U':
                update_game()
            if k == 'Q':
                break
