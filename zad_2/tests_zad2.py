import zmq
import time
import sys


if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    # mode = "sender"
     mode = "receiver"
context = zmq.Context()

print('0')
if mode == "sender":
    socket = context.socket(zmq.PUSH)
    print('1s')
    socket.bind("tcp://*:5551")
    while True:
        print('2s')
        socket.send(b"Server message to client3")
        #msg = socket.recv()
        #print("Sender: " + str(msg))
        time.sleep(3)
else:
    socket = context.socket(zmq.PULL)
    print('1r')
    socket.connect("tcp://localhost:5551")
    while True:
        print('2r')
        msg = socket.recv()
        print("Client: " + str(msg))
        #socket.send(b"client message to server1")
        time.sleep(1)
# import getopt
# import queue
#
# cmd = 'tests_zad2.py -s -a arg1.txt -o arg2.txt'
# sys_args = cmd.split()
# mode, args = getopt.getopt(sys_args[1:], 'sopa:i:')
# print('Command line : ' + cmd)
# print('Command line arguments: ' + str(sys_args))
# print('Options: ' + str(mode))
# print('Arguments: ' + str(args))
#
# game_map = {'a1': ' ', 'a2': ' ', 'a3': ' ', 'b1': ' ', 'b2': ' ', 'b3': ' ', 'c1': ' ', 'c2': ' ', 'c3': ' '}
# print(game_map)
# # print(game_map['a*'])
#
#
# def make_dec(g_map):
#     decision = 'P'
#     for row in 'abc':
#         if g_map[row+'1'] == g_map[row+'2'] == g_map[row+'3']:
#             decision = 'W'
#         print(row)
#     for col in '123':
#         if g_map['a' + col] == g_map['b' + col] == g_map['c' + col]:
#             decision = 'W'
#     if g_map['a1'] == g_map['b2'] == g_map['c3']:
#         decision = 'W'
#     if g_map['c1'] == g_map['b2'] == g_map['a3']:
#         decision = 'W'
#     return decision
