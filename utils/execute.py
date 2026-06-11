import subprocess


def exec_command(command_line, arg=None, shell=False):
    """
    :param command_line: Comando a ejecutar.
    :param arg: argumento que se puede añadir al comando.
    :param shell: True or False (Por defecto: False)
    :return: Respuesta de ejecutar el comando
    """
    if arg:
        command_line = command_line.format(arg)

    return subprocess.check_output(command_line, shell=shell).decode()
