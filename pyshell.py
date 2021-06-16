#!/usr/bin/env python
"""
	Python-based Shell
"""
from __future__ import print_function, division
import os
import os.path
import getpass
import sys
import platform
import requests
import logging
import rich
import time
import json
import re
import argparse
from math import sin, pi
from datetime import datetime
from rich import print as printf
from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.syntax import Syntax
from rich.traceback import install as rich_tracebackinstaller
from rich.table import Table
from rich.console import RenderGroup
from rich.panel import Panel
from rich.live import Live
from downcli import *
import urllib.request
import speedtest

rich_tracebackinstaller()
console = Console()

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

variables = {
    "PS": "$COMPUTERNAME$@$CWD$/> ",
    "CWD": "",
    "HOME_PATH": ""
}


def cd(new_directory: str) -> None:
    """
    change directory function for cd command
    :param new_directory: new directory path
    """
    global variables
    variables["CWD"] = new_directory


log = logging.getLogger("rich")


def detect_platform():
    """
    Detects platform
    :return: Results in tuple (isWindows, isPosix, isOther)
    """
    isWindows = False
    isPosix = False
    isOther = False
    if sys.platform == "win32":
        isWindows = True
    elif sys.platform == "posix":
        isPosix = True
    else:
        isOther = True
    return isWindows, isPosix, isOther


def detect_configuration_file() -> bool:
    """
    Detects if configuration file (conf.json) exists in HOME_PATH
    :return: Result bool
    """
    return True if os.path.exists("conf.json") else False


def create_configuration() -> None:
    """
    Creates configuration file if it doesn't exists
    """
    if detect_configuration_file():
        logger("Configuration file already exists", "info")
    else:
        conf = open("conf.json", "x")
        logger("Configuration file created", "info")
        conf.close()


def save_configuration() -> None:
    """
    Saves Configuration to conf.json
    """
    global variables
    if detect_configuration_file():
        os.remove("conf.json")
        conf = open("conf.json", "w")
        try:
            json.dump(variables, conf)
            logger("Configuration saved successfully!", "success")
        except Exception:
            logger("Configuration save failed!", "error")
        conf.close()
    else:
        logger("Configuration file doesn't exists. Creating New...", "info")
        create_configuration()


def read_configuration() -> object:
    """
    Reads Configuration from conf.json
    :return: configuration
    """
    global variables
    if detect_configuration_file():
        conf = open("conf.json", "r")
        variables = json.load(conf)
        conf.close()
        return variables
    else:
        logger("Configuration file doesn't exists. Creating New...", "info")
        create_configuration()


def detect_color_support():
    """
    Detects if terminal supports following colors: Standard (16 colors), 256 and True (16m) colors
    :return: detection results in tuple (Standard, 256, True)
    """
    supports_standard_colors = False
    supports_256_colors = False
    supports_true_colors = False

    if console.color_system == "truecolor":
        supports_standard_colors = True
        supports_256_colors = True
        supports_true_colors = True
    elif console.color_system == "256":
        supports_standard_colors = True
        supports_256_colors = True
    elif console.color_system == "standard":
        supports_standard_colors = True
    return supports_standard_colors, supports_256_colors, supports_true_colors


def detect_internet_connection():
    """
    Detects if internet connection exists
    :return: detection bool
    """
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except Exception:
        return False


# def rainbow(freq, i):
#     """Creates RGB values, inspired from https://github.com/busyloop/lolcat

#     Args:
#         freq (int): Frequency, more the value; more the colours
#         i (int): Current character position, used to set colours at character level

#     Returns:
#         tuple: Contains integers R, G, B
#     """
#     red = sin(freq * i + 0) * 127 + 128
#     green = sin(freq * i + 2*pi/3) * 127 + 128
#     blue = sin(freq * i + 4*pi/3) * 127 + 128
#     # return "%0x"%(int(red)), "%0x"%(int(green)), "%0x"%(int(blue))
#     return int(red), int(green), int(blue)

# def print_rainbow_text(text, freq=220, end="\n"):
#     """Prints rainbow text if terminal support for colour text is detected, 
#        else falls back to default terminal settings.

#     Args:
#         text (str/list(str)): String or list of str. Provide list to make the whole
#                               paragraph look consistent
#         freq (int, optional): Frequency determines rate of colour change. It's a sine wave so 
#                               changing values on extremes might not help. Sweet spot is 220,
#                               stick to it.
#         end (str, optional): Similar to `end` param in print function
#     """
#     if not supports_color():
#         # print to stderr so doesn't mess with IO redirections.
#         sys.stderr.write("No support for colour on this terminal. Try bash/cygwin." + os.linesep)        
#         if type(text) == list:
#             print("".join(text), end=end)
#         else:
#             print(text, end=end)
#         return
#     for i,c in enumerate(text):
#         if type(text) != list:
#             r,g,b = rainbow(freq, i)
#             color2 = "\033[38;2;%d;%d;%dm"%(r,g,b)
#             print(color2+c+"\033[0m", end="")
#         else:
#             for j, cagain in enumerate(c):
#                 # this formula helps colours spread on whole paragraph. 
#                 r,g,b = rainbow(freq, i*10 + j)
#                 color2 = "\033[38;2;%d;%d;%dm"%(r,g,b)
#                 print(color2+cagain+"\033[0m", end="")
#     print(end=end)

def logger(message: str, severity: str) -> None:
    """
    Log Function
    :param message: message to print
    :param severity: level of severity
    """
    if severity == "warning":
        log.warning(f"[bold yellow]{message}[/]", extra={"markup": True})
    elif severity == "critical":
        log.critical(f"[bold red]{message}[/]", extra={"markup": True})
    elif severity == "fatal":
        log.fatal(f"[bold red blink]{message}[/]", extra={"markup": True})
    elif severity == "error":
        log.error(f"[bold orange]{message}[/]", extra={"markup": True})
    elif severity == "info":
        log.info(f"[bold cyan]{message}[/]", extra={"markup": True})
    elif severity == "success":
        printf(f"[#1a3f5c][{datetime.now().strftime('%H:%M:%S')}][/] [bold green]SUCCESS[/]  [green]{message}[/]")
    elif severity == "log":
        printf(f"[gray]{message}[/]")


def cwd_parser(cwd: str) -> str:
    """
    Parses CWD
    :param cwd: cwd to parse
    :return: parsed cwd
    """
    global variables
    if cwd[0] == "~":
        return cwd.replace("~", variables["HOME_PATH"])
    else:
        return cwd


def prompt_parser(prompt_string: str) -> str:
    """
    Parses prompt for Command Line Prompt
    :param prompt_string: prompt to parse
    :return: parsed prompt
    """
    global variables
    if "$COMPUTERNAME$" in prompt_string:
        prompt_string = prompt_string.replace("$COMPUTERNAME$", platform.node())
    if "$USERNAME$" in prompt_string:
        prompt_string = prompt_string.replace("$USERNAME$", getpass.getuser())
    if "$CWD$" in prompt_string:
        if variables["CWD"] == variables["HOME_PATH"]:
            prompt_string = prompt_string.replace("$CWD$", "~")
        else:
            prompt_string = prompt_string.replace("$CWD$", variables["CWD"])
    if "$TIME$" in prompt_string and "$/TIME$" in prompt_string:
        tmp1, tmp2 = prompt_string.split("$TIME$")
        timeformat, tmp3 = tmp2.split("$/TIME$")
        prompt_string = prompt_string.replace(f"$TIME${timeformat}$/TIME$", datetime.now().strftime(timeformat))
    return prompt_string


def boot():
    """
    Boots Application and get information
    """
    global variables
    with console.status("[bold italic white]Booting[/]...") as status:
        time.sleep(5)
        status.update("[bold yellow]Detecting OS (Operating System) details...[/]")
        sysdetails = platform.uname()
        time.sleep(1)
        console.log(f"OS Name: {sysdetails[0]}")
        time.sleep(1)
        console.log(f"System Release: {sysdetails[2]}")
        time.sleep(1)
        console.log(f"System Version: {sysdetails[3]}")
        time.sleep(2)
        status.update("[bold italic yellow]Detecting Computer Details...[/]")
        time.sleep(1)
        console.log(f"Computer Name: {sysdetails[1]}")
        time.sleep(1)
        console.log(f"Computer Architecture: {sysdetails[4]}")
        time.sleep(1)
        console.log(f"UserName: {getpass.getuser()}")
        time.sleep(1)
        console.log(f"Current Working Directory: {os.getcwd()}")
        time.sleep(1)
        status.update("[italic yellow]Detecting if configuration file exists...[/]")
        time.sleep(3)
        status.update(".       ")
        if detect_configuration_file():
            status.update("[bold green]Exists[/]")
            read_configuration()
        else:
            status.update("[bold red]Does Not Exist! Creating New Configuration...[/]")
            time.sleep(2)
            status.update(".      ")
            create_configuration()
        variables["CWD"] = variables["HOME_PATH"] = os.getcwd()
        save_configuration()
        time.sleep(2)
        status.update("[bold italic white]Detecting[/] [red]C[orange]o[cyan]l[green]o[purple]r[/] Support...[/]")
        time.sleep(1)
        colorsupport = detect_color_support()
        console.log(f"Support for Basic Colors (16 colors): {colorsupport[0]}")
        time.sleep(1)
        console.log(f"Support for 256 Colors: {colorsupport[1]}")
        time.sleep(1)
        console.log(f"Support for true Colors (16 million colors): {colorsupport[2]}")
        time.sleep(2)
        status.update("[bold italic cyan]Detecting Internet Details...[/]")
        time.sleep(1)
        if detect_internet_connection():
            console.log(f"Internet Access: {True}")
            speed = speedtest.Speedtest()
            status.update("[bold italic green] Detecting Download Speed...[/]")
            console.log(f"Download speed: {'{:.2f}'.format(speed.download() / 1024 / 1024)} Mb/s")
            status.update("[bold italic green] Detecting Upload Speed...[/]")
            console.log(f"Upload speed: {'{:.2f}'.format(speed.upload() / 1024 / 1024)} Mb/s")
        else:
            console.log(f"Internet Access: {False}")
        status.update("[bold yellow]Finishing Booting...[/]")
        time.sleep(2)
    printf(f"[bold]:heavy_check_mark:[/] [bold italic green]Booting Successful![/]")
    time.sleep(3)
    main()


def command_parser(commands_string: str) -> None:
    """
    Parses commands from Command Line Prompt
    :param commands_string: command string to parse
    """
    global variables
    commands = []
    for command in commands_string.split("&&"):
        commands.append(command.strip())
    for command_str in commands:
        command = command_str.split(" ")[0]
        arguments = command_str.split(" ")[1:]
        if command in ["echo", "print"]:
            console.out(" ".join(arguments))
        elif command == "cwd":
            console.out(os.getcwd())
        elif command == "cd":
            if len(arguments) == 0:
                os.chdir(variables["HOME_PATH"])
                cd(variables["HOME_PATH"])
            elif len(arguments) == 1:
                if os.path.isdir(arguments[0]):
                    os.chdir(arguments[0])
                    cd(arguments[0])
                else:
                    logger("Directory Doesn't Exists!", "error")
            else:
                logger("Invalid amount of arguments! Only 1 is passed!", "error")
        elif command in ["mkdir", "makedir"]:
            if len(arguments) != 1:
                logger("Only 1 argument - new directory name, is passed!", "error")
            else:
                if os.path.exists(arguments[0]):
                    logger("Directory already exists", "info")
                else:
                    try:
                        os.mkdir(arguments[0])
                        logger("Directory created", "success")
                    except Exception as except_error:
                        logger(f"Failed to create directory! Exception Encountered: {except_error}", "error")
        elif command == "get":
            if len(arguments) != 0:
                try:
                    printf(variables[arguments[0]])
                except Exception:
                    logger("Invalid Variable!", "error")
        elif command == "set":
            if len(arguments) == 2:
                if arguments[0] in variables:
                    try:
                        variables[arguments[0]] = arguments[1]
                        logger("Variable changed successfully!", "success")
                    except Exception:
                        logger("Variable change failed!", "error")
                else:
                    logger("Variable doesn't exist!", "error")
            else:
                logger("Need Argument!", "error")
        elif command == "downcli":
            if len(arguments) >= 1:
                if arguments[0] in ["-h", "--help"]:
                    print_downcli_help_msg()
                    if arguments[1] in ["-d", "--directory"]:
                        downcli(arguments[3:], arguments[2])
                    else:
                        downcli(arguments[1:], "./")
                elif arguments[0] in ["-d", "--directory"]:
                    downcli(arguments[2:], arguments[1])
                else:
                    downcli(arguments[0:], "./")
            else:
                print_downcli_help_msg()
        elif command == "exit":
            if len(arguments) == 0:
                exit()
            elif len(arguments) == 1:
                sys.exit(int(arguments[0]))
            else:
                sys.exit(1)
        else:
            logger("Invalid Argument", "error")
    main()


def command_line():
    """
    Command Line Prompt Function
    """
    printf(prompt_parser(variables["PS"]), end="")
    command = str(input())
    command_parser(command)


def main():
    """
    Main Function
    """
    command_line()


if __name__ == "__main__":
    boot()
