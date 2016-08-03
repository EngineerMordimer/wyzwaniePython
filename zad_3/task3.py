import os
import sys
import shutil


def get_ext(path):
    """Return extension of file("dir" if not file) (to 5 charts).

    Args:
        path: path of file
    Returns:
        name of extension ("dir" if not file). If extension is longer, last char is *.
    """
    if os.path.isfile(path):
        extension = os.path.splitext(path)[1][1:]
        if len(extension) <= 5:
            return extension[:5]
        else:
            return extension[:4] + '*'
    else:
        return "dir"


def get_type(path):
    """Return type of path.

    Args:
        path: real path
    Returns:
        if path is:
        file - "plik"
        directory - "katalog"
        other - "inny"
    """
    if os.path.isfile(path):
        return "plik"
    elif os.path.isdir(path):
        return "katalog"
    else:
        return "inny"


def get_size(path):
    """Return size and number of elements in path and sub-folders in path

    Args:
        path: real path
    Returns:
        Return dictionary {"size": total_size, "count": count_files}
    """
    if os.path.isfile(path):
        return {"size": os.stat(path).st_size, "count": 1}
    else:
        total_size = 0
        count_files = 0
        for dirpath, dirnames, filenames in os.walk(path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
                count_files += 1
        return {"size": total_size, "count": count_files}


def cmd_ls(path):
    """List directory contents

    Args:
        path: real path
    Returns:
        List of elements in path
    """
    return os.listdir(path)


def cmd_ls_exclusive(path):
    """List directory contents with long listing

    Args:
        path: real path
    Returns:
        List of elements in path with information about extension and size
    """
    view_text = '{name:>20} {extension:>10} {size:>15}\n'.format(name='name', extension='extension', size='size')
    view_text += '=' * 47 + '\n'
    for element in os.listdir(path):
        name = element
        extension = get_ext('{path}/{file}'.format(path=path, file='element'))
        size = get_size('{path}/{file}'.format(path=path, file='element'))["size"]
        view_text += '{name:>20} {extension:>10} {size:>15}\n'.format(**vars())
    return view_text


def cmd_info(path):
    """Return information about path. Type(file,dir,other), path, size, create time, modification time

    Args:
        path: real path
    Returns:
        Type(file,dir,other), path, size, create time, modification time
    """
    view_text = "typ: " + get_type(path) + '\n'
    view_text += "ścieżka: " + path + '\n'
    view_text += "rozmiar: " + str(get_size(path)["size"]) + 'B\n'
    if os.path.isdir(path):
        view_text += "liczba_plikow: " + str(get_size(path)["count"]) + '\n'
    view_text += "ctime: " + str(os.path.getctime(path)) + '\n'
    view_text += "mtime: " + str(os.path.getmtime(path))
    return view_text


def cmd_pwd():
    """Return information about local path

    Returns:
        Local path
    """
    return os.getcwd()


def cmd_cd(path):
    """Change local path

    Returns:
        None
    """
    os.chdir(path)
    return None


def cmd_cp(old_path, new_path):
    """Copy file using shutil.copy2

    Args:
        old_path: path of file
        new_path: new path of copied file
    Returns:
        None
    """
    shutil.copy2(old_path, new_path)
    return None


def cmd_mv(old_path, new_path):
    """Move file to new directory

    Args:
        old_path: path of file
        new_path: new path of moved file
    Returns:
        None
    """
    shutil.move(old_path, new_path)
    return None


def cmd_rm(path):
    """Remove file or directory recursive

    Args:
        path:
    Returns:
        None
    """
    if os.path.isfile(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    return None


def cmd_touch(path):
    """Create new empty file

    Args:
        path:
    Returns:
        None
    """
    open(path, 'a').close()
    return None


def parse(cmd, args):
    """Execute command with arguments
    Command list:
        pwd, ls, info, cd, cp, mv, touch, rm

    For help type "help 'command' ", where 'command' is one from list

    Args:
        cmd: command from list
        args: arguments for command
    Returns:
        Depend on command.
    """
    try:
        if cmd == "pwd":
            return cmd_pwd()
        elif cmd == "ls":
            return cmd_ls(args[0] if len(args) > 0 and len(args[0]) > 0 else cmd_pwd())
        elif cmd == "info":
            return cmd_info(args[0])
        elif cmd == "cd":
            return cmd_cd(args[0], args[1])
        elif cmd == "cp":
            return cmd_cp(args[0], args[1])
        elif cmd == "mv":
            return cmd_mv(args[0], args[1])
        elif cmd == "touch":
            return cmd_touch(args[0])
        elif cmd == "rm":
            return cmd_rm(args[0])
        elif cmd == "help":
            my_command = "cmd_" + args[0] if len(args) > 0 and len(args[0]) > 0 else "parse"
            return eval("help(" + my_command + ")")
        else:
            return "Wrong command!"
    except IndexError:
        return cmd + ": Wrong number of arguments!"
    except:
        return cmd + ": " + str(sys.exc_info())

localPath = (sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
print("You are in: " + cmd_pwd())
print("Type 'help' for usage info.")
print("Type 'exit' to end program.")
while True:
    command = input().split()
    if command[0] == "exit":
        break
    print(parse(command[0], command[1:]))
