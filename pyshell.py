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
from rich.traceback import install as rich_tracebackInstaller
from rich.table import Table
from rich.console import RenderGroup
from rich.panel import Panel
from supports_color import supportsColor
import urllib.request
import speedtest

rich_tracebackInstaller()
console = Console()

logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

PS = "$COMPUTERNAME$$CWD$/> "

log = logging.getLogger("rich")

def detect_platform():
    isWindows = False
    isPosix = False
    isOther = False
    if sys.platform() == "win32":
        isWindows = True
    elif sys.platform() == "posix":
        isPosix = True
    else:
        isOther = True
    return (isWindows, isPosix, isOther)

def detect_color_support():
    supports_basic_colors = False
    supports_256_colors = False
    supports_true_colors = False

    if supportsColor.stdout:
        supports_basic_colors = True
    if supportsColor.stdout.has256:
        supports_256_colors = True
    if supportsColor.stderr.has16m:
        supports_true_colors = True
    return (supports_basic_colors, supports_256_colors, supports_true_colors)

def detect_internet_connection():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

# def detect_windows_terminal():
#     """
#     Returns True if detects to be running in a powershell, False otherwise.
#     """
#     return sys.platform == 'win32' and os.environ.get('WT_SESSION', None) is not None

# def supports_color():
#     """
#     Returns True if the running system's terminal supports color, and False
#     otherwise.
#     """
#     plat = sys.platform
#     supported_platform = plat != 'Pocket PC' and ('ANSICON' in os.environ)
#     is_wnd_term = detect_windows_terminal()
#     # isatty is not always implemented, #6223.
#     is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
#     if (not supported_platform and is_wnd_term and is_a_tty):
#         return True
#     if not supported_platform or not is_a_tty:
#         return False
#     return True

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

def prompt_parser(prompt_string: str) -> None:
    if "$COMPUTERNAME$" in prompt_string:
        prompt_string = prompt_string.replace("$COMPUTERNAME$", platform.node())
    if "$USERNAME$" in prompt_string:
        prompt_string = prompt_string.replace("$USERNAME$", getpass.getuser())
    if "$CWD$" in prompt_string:
        prompt_string = prompt_string.replace("$CWD$", os.getcwd())
    if "$TIME$" in prompt_string and "$/TIME$" in prompt_string:
        tmp1, tmp2 = prompt_string.split("$TIME$")
        timeformat, tmp2 = tmp2.split("$/TIME$")
        prompt_string = prompt_string.replace("$TIME$$/TIME$", datetime.now().strftime(timeformat))
    return prompt_string
    
def boot():
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
            console.log(f"Download speed: {'{:.2f}'.format(speed.download()/1024/1024)} Mb/s")
            status.update("[bold italic green] Detecting Upload Speed...[/]")
            console.log(f"Upload speed: {'{:.2f}'.format(speed.upload()/1024/1024)} Mb/s")
        else:
            console.log(f"Internet Access: {False}")
        time.sleep(2)
    printf(f"[bold]:heavy_check_mark:[/] [bold italic green]Booting Successfull![/]")
    time.sleep(3)
    main()

def command_parser(commands_string: str) -> None:
    commands = []
    for command in commands_string.split("&&"):
    	commands.append(command.strip())
    for command_str in commands:
    	command = command_str.split(" ")[0]
    	arguments = command_str.split(" ")[1:]
    	if command in ["echo", "print"]:
    		console.out(' '.join(arguments))
    	elif command == "cwd":
    		console.out(os.getcwd())
    	elif command == "set":
    		if arguments[0] == "PS":
    			PS = " ".join(arguments[1:])
    		else:
    			logger("Invalid Argument", "error")
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

def main():
    printf(prompt_parser(PS), end="")
    command = str(input())
    command_parser(command)

if __name__ == "__main__":
    boot()