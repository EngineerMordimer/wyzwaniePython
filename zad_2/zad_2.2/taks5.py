import sys
import zmq
import json


def set_connection(port_server, port_client):
    context_server = zmq.Context()
    context_client = zmq.Context()
    socket_server = context_server.socket(zmq.PUSH)
    socket_client = context_client.socket(zmq.PULL)
    socket_server.bind("tcp://*:{port_server}".format(**vars()))
    socket_client.connect("tcp://localhost:{port_client}".format(**vars()))
    return socket_server, socket_client


def make_dec(g_map):
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
    pos = input().split()[0]
    try:
        if pos == 'exit':
            print("End game")
            return 2
        elif g_map[pos] == ' ':
            g_map[pos] = player_char
        else:
            print("Wrong position chose other")
            return -1
    except KeyError:
        print("Wrong position chose other")
        return -1
    return 1


def draw_map(board, g_map):
    print(board.format(**g_map))


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
if len(sys.argv[1:]) > 1:
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
        iterator += play_game(game_map, curr_char)
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
