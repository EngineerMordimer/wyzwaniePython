import sys
import zmq
import json


def set_connection(port_server, port_client):
    """Setting connection on ports to push and pull

    Arguments:
        port_server: port to push data
        port_client: port to pull data
    Return:
        socket_server , socket_client
    """
    context_server = zmq.Context()
    context_client = zmq.Context()
    socket_server = context_server.socket(zmq.PUSH)
    socket_client = context_client.socket(zmq.PULL)
    socket_server.bind("tcp://*:{port_server}".format(**vars()))
    socket_client.connect("tcp://localhost:{port_client}".format(**vars()))
    return socket_server, socket_client


def make_dec(g_map):
    """Make decision if game is end.

    Arguments:
        g_map: Dictionary of game
    Returns:
        if game is end:
            'W'
        else:
            'L'
    """
    dec = 'L'
    for row in 'abc':
        if g_map[row+'1'] == g_map[row+'2'] == g_map[row+'3'] and g_map[row+'1'] != ' ':
            dec = 'W'
    for col in '123':
        if g_map['a' + col] == g_map['b' + col] == g_map['c' + col] and g_map['a' + col] != ' ':
            dec = 'W'
    if g_map['a1'] == g_map['b2'] == g_map['c3'] and g_map['a1'] != ' ':
        dec = 'W'
    if g_map['c1'] == g_map['b2'] == g_map['a3'] and g_map['c1'] != ' ':
        dec = 'W'
    return dec


def play_game(g_map, player_char):
    """Check and put player_char on position(from input) to g_map.

    Arguments:
        g_map: Dictionary of game
        player_char: char of player
    Returns:
        if from input word 'exit'
            2
        elif position is correct (not occupied)
            1
        else
            -1
    """
    pos = input().split()[0]
    try:
        if pos == 'exit':
            print("End game")
            return 2
        elif g_map[pos] == ' ':
            g_map[pos] = player_char
            return 1
        else:
            print("Wrong position chose other")
            return -1
    except KeyError:
        print("Wrong position chose other")
        return -1


def draw_map(board, g_map):
    """Print map with charts from g_map.

    Arguments:
        board: clean borad of game
        g_map: Dictionary of game
    Return:
        None
    """
    print(board.format(**g_map))


def main(sys_args):
    """Game Tic Tac Toe with 2 modes:
        1. On one command line. Play if there's not any arguments.
        2. On 2 commands line.

    Arguments:
        sys_args:
            1. server port
            2. client port
            3. type of player ('x' or 'o')
    Returns:
        None
     """
    game_map = {'a1': ' ', 'a2': ' ', 'a3': ' ', 'b1': ' ', 'b2': ' ', 'b3': ' ', 'c1': ' ', 'c2': ' ', 'c3': ' '}
    shell = ' {a1} | {a2} | {a3} \n---+---+---\n {b1} | {b2} | {b3} \n---+---+---\n {c1} | {c2} | {c3} '
    winner_text = """

     #     # ### #     # #     # ####### ######
     #  #  #  #  ##    # ##    # #       #     #
     #  #  #  #  # #   # # #   # #       #     #
     #  #  #  #  #  #  # #  #  # #####   ######
     #  #  #  #  #   # # #   # # #       #   #
     #  #  #  #  #    ## #    ## #       #    #
      ## ##  ### #     # #     # ####### #     #


    """
    loser_text = """
    #       #######  #####  ####### ######
    #       #     # #     # #       #     #
    #       #     # #       #       #     #
    #       #     #  #####  #####   ######
    #       #     #       # #       #   #
    #       #     # #     # #       #    #
    ####### #######  #####  ####### #     #
    """
    if len(sys_args) > 1:
        game_mode = "online"
        port_srv = sys.argv[1]
        port_clt = sys.argv[2]
        player = sys.argv[3]
    else:
        game_mode = "local"

    if game_mode == "local":
        iterator = 1
        while True:
            if iterator % 2 == 0:
                curr_char = 'x'
            else:
                curr_char = 'o'
            print('Now playing: ' + curr_char)
            decision = play_game(game_map, curr_char)
            if decision == 2:
                sys.exit(1)
            while decision == -1:
                decision = play_game(game_map, curr_char)
            draw_map(shell, game_map)
            if make_dec(game_map) == 'W':
                print(winner_text)
                print("Player: " + curr_char + " WIN !")
                sys.exit(1)
            iterator += 1
    elif game_mode == "online":
        socket_srv, socket_clt = set_connection(port_srv, port_clt)
        print("Hello player: " + player)
        if player == 'x':
            print("Round player: " + player)
            draw_map(shell, game_map)
            play_game(game_map, player)
            draw_map(shell, game_map)
            socket_srv.send_json(json.dumps(game_map))
        print("Waiting for another player")
        while True:
            game_map = json.loads(socket_clt.recv_json())
            if make_dec(game_map) == 'W':
                draw_map(shell, game_map)
                print(loser_text)
                sys.exit(1)
            else:
                print("Round player: " + player)
                draw_map(shell, game_map)
                decision = play_game(game_map, player)
                if decision == 2:
                    socket_srv.send_json(json.dumps(game_map))
                    sys.exit(1)
                while decision == -1:
                    decision = play_game(game_map, player)
                draw_map(shell, game_map)
                if make_dec(game_map) == 'W':
                    print(winner_text)
                    socket_srv.send_json(json.dumps(game_map))
                    sys.exit(1)
                socket_srv.send_json(json.dumps(game_map))
                print("Waiting for another player")
if __name__ == "__main__":
    main(sys.argv[1:])
