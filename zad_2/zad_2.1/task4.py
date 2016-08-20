import sys
import getopt
import threading
import queue
import markdown
import os.path


def read_markdown(local_queue, file, local_mode=None):
    """Read file text and send it to queue.
    Can print information on command line about process.
    Args:
        local_queue: queue in which will be send text
        file: file to read
        local_mode: if got value, print on command line information
    Return:
        None
    """
    if local_mode:
        print(' '*10 + 'Start reading')
    md_file = open(file, 'r')
    md = md_file.read()
    md_file.close()
    local_queue.put(md)
    if local_mode:
        print(' '*10 + 'End reading')
    return


def translate_md_html(local_queue, new_file, local_mode=None):
    """Getting text from queue, translate it to html and write to file.
    Can print information on command line about process.
    Args:
        local_queue: queue from which will be get text
        new_file: file in which will be save html text
        local_mode: if not None, print on command line information
    Return:
        None
    """
    if local_mode:
        print(' '*20 + 'Start translate')
    tmp = local_queue.get()
    local_queue.task_done()
    html = markdown.markdown(tmp)
    write_file = open(new_file, 'w+')
    write_file.write(html)
    write_file.close()
    if local_mode:
        print(' '*20 + 'End translate')
    return


def new_file_html(cmd_args):
    """Return new name file depend on arguments from command line.

    Args:
        cmd_args: arguments from command line
    Returns:
        Return:
            if new name file is passed (second arg):
                new name file
            else:
                old file name (first arg) with proper extension
    """
    if len(cmd_args) > 1:
        n_file = cmd_args[1]
    else:
        name = os.path.splitext(cmd_args[0])[0]
        ext = 'html'
        n_file = '{name}.{ext}'.format(**vars())
    return n_file


def main(sys_args):
    """Translate markdown file to html file.

    Options:
        -s      Show information during threads

    Arguments:
        sys_args:
            1. markdown file
            2. html file (default markdown file name with proper extension)
    Returns:
        None
    """
    mode, args = getopt.getopt(sys_args, 's')
    try:
        tmp_file = args[0]
        n_file_name = new_file_html(args)
        tmp_queue = queue.Queue()
        r = threading.Thread(name='reading', target=read_markdown, args=(tmp_queue, tmp_file, mode))
        t = threading.Thread(name='translating', target=translate_md_html, args=(tmp_queue, n_file_name, mode))
        if mode:
            print('Start starting threads')
        r.start()
        t.start()
        if mode:
            print('End main thread')
    except IndexError:
        print('Error: Missing file operand')

if __name__ == "__main__":
    main(sys.argv[1:])
