import getopt
import queue

cmd = 'tests_zad2.py -s -a arg1.txt -o arg2.txt'
sys_args = cmd.split()
mode, args = getopt.getopt(sys_args[1:], 'sopa:i:')
print('Command line : ' + cmd)
print('Command line arguments: ' + str(sys_args))
print('Options: ' + str(mode))
print('Arguments: ' + str(args))

help(queue)