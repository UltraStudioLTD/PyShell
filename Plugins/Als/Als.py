#!/usr/bin/env python3
"""Als Plugin for PyShell"""
import logging
import os
from datetime import datetime
from pathlib import Path
from rich import print as printf, pretty
from rich.console import Console
from rich.filesize import decimal
from rich.logging import RichHandler
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

pretty.install()
console = Console()
logging.basicConfig(
    level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)
log = logging.getLogger("rich")
__package__ = "[red]Als-Plugin[/]"
__version__ = "[yellow]0.0.1[/]"
__description__ = "[red]Als[/] Plugin for [bold green]Py[/][italic black on white]Shell[/]"
__package_link__ = "[bold black on white]Git[/][bold italic]Hub[/]: https://www.github.com/UltraStudioLTD/Als"
__author__ = "[bold blue]Luka Mamukashvili[/] ([bold black on white]Git[/][bold italic]Hub[/]: [italic cyan]UltraStudioLTD[/])"
__author_links__ = "[bold black on white]Git[/][bold italic]Hub[/]: https://www.github.com/UltraStudioLTD\n[bold black on white]Dev[/]: https://www.dev.to/ultrastudio"
audio_file_extensions = ["aac", "au", "flac", "mid", "midi", "mka", "mp3", "mpc", "ogg", "ra", "wav", "axa", "oga", "spx", "xspf"]
achieve_file_extensions = ["tar", "tgz", "arj", "taz", "lzh", "lzma", "tlz", "txz", "zip", "z", "Z", "dz", "gz", "lz", "xz", "bz2", "bz", "tbz", "tbz2", "tz", "deb", "rpm", "jar", "rar", "ace", "zoo", "cpio", "7z", "rz"]
media_file_extensions = ["jpg", "jpeg", "gif", "bmp", "pbm", "pgm", "ppm", "tga", "xbm", "xpm", "tif", "tiff", "png", "svg", "svgz", "mng", "pcx", "mov", "mpg", "mpeg", "m2v", "mkv", "ogm", "mp4", "m4v", "mp4v", "vob", "qt", "nuv", "wmv", "asf", "rm", "rmvb", "flc", "avi", "fli", "flv", "gl", "dl", "xcf", "xwd", "yuv", "cgm", "emf", "axv", "anx", "ogv", "ogx"]
python_file_extensions = [".py", ".pyw", ".pyc"]
pps_file_extension = [".pps"]
ppm_file_extension = [".ppm.lock"]
package_file_extension = [".package"]
lock_file_extension = [".lock"]
known_file_extensions = ["aac", "au", "flac", "mid", "midi", "mka", "mp3", "mpc", "ogg", "ra", "wav", "axa", "oga", "spx", "xspf", "tar", "tgz", "arj", "taz", "lzh", "lzma", "tlz", "txz", "zip", "z", "Z", "dz", "gz", "lz", "xz", "bz2", "bz", "tbz", "tbz2", "tz", "deb", "rpm", "jar", "rar", "ace", "zoo", "cpio", "7z", "rz", "jpg", "jpeg", "gif", "bmp", "pbm", "pgm", "ppm", "tga", "xbm", "xpm", "tif", "tiff", "png", "svg", "svgz", "mng", "pcx", "mov", "mpg", "mpeg", "m2v", "mkv", "ogm", "mp4", "m4v", "mp4v", "vob", "qt", "nuv", "wmv", "asf", "rm", "rmvb", "flc", "avi", "fli", "flv", "gl", "dl", "xcf", "xwd", "yuv", "cgm", "emf", "axv", "anx", "ogv", "ogx", ".py", ".pyw", ".pyc", ".pps", ".ppm.lock", ".package", ".lock"]
file_types = {
    "audio": "AUDIO-FILE",
    "achieve_file_extensions": "ACHIEVE-FILE",
    "media": "MEDIA-FILE",
    "python": "PYTHON-FILE",
    "pps": "PY$SHELL-SCRIPT",
    "ppm": "PY$SHELL_PACKAGE_MANAGER-LOCK",
    "package": "PACKAGE-FILE",
    "lock": "LOCK-FILE"
}
helper_ = ["-h", "--help"]
version_ = ["-v", "--version"]
tree_ = ["-t", "--tree"]
dir_only_ = ["-d", "--dir_only"]
colors_ = ["-c", "--colors"]
permissions_ = ["-p", "--permissions"]
rich_tree_ = ["-r", "--rich_tree"]


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


def print_als_help_msg() -> None:
    """Prints Help Message for Als Plugin"""
    description_panel = Panel.fit(f"{__description__}\n\tby: {__author__}", title="Package [italic purple]Description[/]", border_style="green")
    usage_panel = Panel.fit(
        "\tUsage: [bold red]als[/] [[bold italic]-h, --help[/]] [[bold italic]-v, --version[/]] [[bold italic]-t, --tree[/]] {[italic]-d, --dir_only[/]} {[italic]-p, --permissions[/]} {[italic]-c, --colors[/]}", title="Package [italic yellow]Command Line Usage[/]", border_style="purple")
    table = Table(title="[bold italic yellow]Usage Help[/]")
    package = Table(title="[bold italic yellow]Package[/]")
    package.add_row(description_panel)
    package.add_row(usage_panel)
    table.add_column("Argument Type")
    table.add_column("Argument(s)")
    table.add_column("Argument(s)'s Description")
    table.add_row("Optional", "[yellow]-h[/], [yellow]--help[/]", "Prints [purple]help[/] message and [yellow]exits[/]")
    table.add_row("Optional", "[yellow]-v[/], [yellow]--version[/]", "Prints [red]version[/] of plugin and [yellow]exits[/]")
    table.add_row("Optional", "[yellow]-t[/], [yellow]--tree[/]", "Use [italic green]\"tree\"[/] module of [bold italic red]\"Als\"[/]")
    table.add_row("Extension", "[yellow]-d[/], [yellow]--dir_only[/]", "set [italic green]\"tree\"[/] module to [italic]\"directory only\"[/]")
    table.add_row("Extension", "[yellow]-p[/], [yellow]--permissions[/]", "set [italic green]\"ls\"[/] module to [italic]\"show permissions\"[/]")
    table.add_row("Extension", "[yellow]-c[/], [yellow]--colors[/]", "set [italic green]\"ls\"[/] module to [italic]\"show colors\"[/]")
    table.add_row("Alternative", "[yellow]-rt[/], [yellow]--rich_tree[/]",
                  "change [italic green]\"tree\"[/] module to [italic]\"rich tree\"[/]")
    package_info = Table(title="Package Info")
    package_info.add_row(Panel.fit(f"{__package_link__}", title="Package Link", border_style="yellow"))
    package_info.add_row(Panel.fit(f"{__author_links__}", title="Author Links", border_style="cyan"))
    als_table = Table()
    als_table.add_row(package_info)
    als_table.add_row(table)
    console.print(Panel.fit(als_table, title=f"{__package__} v{__version__}", border_style="red"))


def als(args=None) -> None:
    """
    Als function
    :param args: Arguments
    """
    if args is None:
        args = ["ls"]
    if not args or args == ["ls"]:
        ls()
    elif len(args) > 2:
        logger("Invalid number of arguments", "error")
    elif len(args) == 1:
        if args[0] in version_:
            printf(f"{__package__} v{__version__}")
        elif args[0] in helper_:
            print_als_help_msg()
        elif args[0] in tree_:
            tree_generator(os.getcwd())
        elif args[0] in colors_:
            ls(color=True)
        elif args[0] in permissions_:
            ls(permissions=True)
        elif args[0] in rich_tree_:
            rich_tree()
    elif len(args) == 2:
        if args[0] in tree_:
            logger(f"only {dir_only_} is optional arguments for {tree_}", "error") if args[1] not in dir_only_ else tree_generator(os.getcwd(), True)
        elif args[0] in colors_:
            logger(f"only {permissions_} is optional arguments for {colors_}", "error") if args[1] not in permissions_ else ls(color=True, permissions=True)
        elif args[0] in permissions_:
            ls(color=True, permissions=True) if args[1] in colors_ else logger(f"only {colors_} is optional arguments for {permissions_}", "error")


def tree_generator(path, dir_only=False) -> None:
    """
    Tree Generator
    :param path: path_item to make tree from
    :param dir_only: display only directories (default: False)
    """
    DirectoryTree(path, dir_only).generate()


def file_type_finder(extension: str) -> str:
    """
    Finds type of file
    :param extension: file's extension
    :return: file type
    """
    if extension in known_file_extensions:
        if extension in audio_file_extensions:
            return file_types["audio"]
        elif extension in achieve_file_extensions:
            return file_types["achieve"]
        elif extension in media_file_extensions:
            return file_types["media"]
        elif extension in python_file_extensions:
            return file_types["python"]
        elif extension in pps_file_extension:
            return file_types["pps"]
        elif extension in ppm_file_extension:
            return file_types["ppm"]
        elif extension in package_file_extension:
            return file_types["package"]
        elif extension in lock_file_extension:
            return file_types["lock"]
    else:
        return "FILE"

def permissions_finder(file) -> list[str]:
    """
    Finds Permissions of file
    :param file: file
    :return: permissions array
    """
    if os.path.isfile(file) and os.access(file, os.F_OK):
        permissions = []
        if os.access(file, os.R_OK):
            permissions.append("+r")
        if os.access(file, os.W_OK):
            permissions.append("+w")
        if os.access(file, os.X_OK):
            permissions.append("+x")
        return permissions
    else:
        printf(f"{file} should be file")


PIPE = "║ "
ELBOW = "╚══⫸ "
TEE = "╠══⫸ "
PIPE_PREFIX = "║    "
SPACE_PREFIX = "     "


class DirectoryTree:
    """Tree Class"""
    def __init__(self, root_dir, dir_only=False):
        self._generator = _TreeGenerator(root_dir, dir_only)

    def generate(self):
        """
        Generate Tree
        """
        tree = self._generator.build_tree()
        for entry in tree:
            printf(entry)


class _TreeGenerator:
    def __init__(self, root_dir, dir_only=False):
        self._root_dir = Path(root_dir)
        self._dir_only = dir_only
        self._tree = []

    def build_tree(self):
        """
        Builds Tree
        :return: built tree
        """
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _tree_body(self, directory, prefix=""):
        entries = self._prepare_entries(directory)
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            self._add_directory(entry, index, entries_count, prefix, connector) if entry.is_dir() else self._add_file(entry, prefix, connector)

    def _prepare_entries(self, directory):
        entries = directory.iterdir()
        if self._dir_only:
            return [entry for entry in entries if entry.is_dir()]
        return sorted(entries, key=lambda entry: entry.is_file())

    def _add_directory(self, directory, index, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        prefix += PIPE_PREFIX if index != entries_count - 1 else SPACE_PREFIX
        self._tree_body(directory=directory, prefix=prefix, )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")


def ls(color=False, permissions=False, path=os.getcwd()):
    """
    Bash's ls function for Python
    :param color: display colors (default: False)
    :param permissions:  display permissions (default: False)
    :param path: path_item, from where to display items
    """
    for item in Path(path).iterdir():
        extension = "".join(item.suffixes) if item.is_file() else extension = None
        if not color and not permissions:
            if item.is_file():
                file_type = "FILE" if extension not in known_file_extensions else f"{file_type_finder(extension)}"
                printf(f"<item-type/{file_type}>    |   {item}")
            elif item.is_dir():
                printf(f"<item-type/DIRECTORY>  |   {item}")
            elif item.is_symlink():
                printf(f"<item-type/SYMBOLIC-LINK>  |   {item}")
            elif item.is_mount():
                printf(f"<item-type/MOUNT>  |   {item}")
            elif item.is_char_device():
                printf(f"<item-type/CHAR-DEVICE>    |   {item}")
            elif item.is_block_device():
                printf(f"<item-type/BLOCK-DEVICE>   |   {item}")
            elif item.is_socket():
                printf(f"<item-type/SOCKET> |   {item}")
            elif item.is_fifo():
                printf(f"<item-type/FIFO>   |   {item}")
            elif item.is_reserved():
                printf(f"<item-type/RESERVED>   |   {item}")
        elif not color and permissions:
            if os.path.isfile(item):
                printf(f"<item-type/FILE>   |   {item}  |   {''.join(permissions_finder(item))}" if os.path.isfile(item))
            else:
                printf(f"<item-type/DIRECTORY>  |   {item}")
        elif color and permissions:
            if os.path.isfile(item):
                permissionsList = permissions_finder(item)
                if "+x" in permissionsList and extension not in known_file_extensions:
                    printf(
                        f"<[yellow]item-type[/]/[bold italic green]FILE[/]> |   [italic green]{item}[/]    | {''.join(permissions_finder(item))}")
            elif item.is_dir():
                printf(f"<[yellow]item-type[/]/[bold italic blue]DIRECTORY[/]>  |   [italic blue]{item}[/]")
            elif item.is_symlink():
                printf(f"<[yellow]item-type[/]/[bold italic cyan]SYMBOLIC-LINK[/]>  |   [italic cyan]{item}[/]")
            elif item.is_mount():
                printf(
                    f"<[yellow]item-type[/]/[bold italic yellow on black]MOUNT[/]>  |   [italic yellow on black]{item}[/]")
            elif item.is_char_device():
                printf(f"<item-type/CHAR-DEVICE>    |   {item}")
            elif item.is_block_device():
                printf(f"<item-type/BLOCK-DEVICE>   |   {item}")
            elif item.is_socket():
                printf(f"<item-type/SOCKET> |   {item}")
            elif item.is_fifo():
                printf(f"<item-type/FIFO>   |   {item}")
            elif item.is_reserved():
                printf(f"<item-type/RESERVED>   |   {item}")


def walk_directory(directory: Path, tree: Tree) -> None:
    """Recursively build a Tree with directory contents"""
    for path in sorted(Path(directory).iterdir(), key=lambda path_item: (path_item.is_file(), path_item.name.lower()),):
        # Remove hidden files
        if path.name.startswith("."):
            continue
        if path.is_dir():
            style = "dim" if path.name.startswith("__") else ""
            for x in sorted(Path(directory).iterdir(), key=lambda path_: (path_.is_file(), path_.name.lower()),):
                branch = tree.add(f"[bold cyan] <[/]💠/📦[bold yellow]>[/] link file://{path}]{escape(path.name)}", style=style, guide_style=style, ) if x.is_file() and x.name.lower == "ppm_package" else branch = tree.add(f"[bold magenta]:open_file_folder: [link file://{path}]{escape(path.name)}", style=style, guide_style=style, )
            walk_directory(path, branch)
        else:
            is_PPM_Package = False
            is_Package = False
            file_name_color = "green"
            extension_color = "bold red"
            if path.suffixes == [".package"]:
                is_Package = True
            elif path.suffixes == [".ppm", ".package"]:
                is_PPM_Package = True
                is_Package = True
            if is_Package:
                extension_color = "bold yellow"
            if is_PPM_Package:
                file_name_color = "bold italic cyan"
            text_filename = Text(path.name, file_name_color)
            text_filename.highlight_regex(r"\..*$", extension_color)
            text_filename.stylize(f"link file://{path}")
            file_size = path.stat().st_size
            text_filename.append(f" ({decimal(file_size)})", "blue")
            if path.suffix in python_file_extensions:
                icon = "🐍 "
            elif path.suffix == pps_file_extension:
                icon = "💠 "
            elif path.suffix == lock_file_extension:
                icon = "🔒 "
            elif path.suffixe == package_file_extension:
                icon = "📦 "
            elif ".".join(path.suffixes) == ppm_file_extension:
                icon = "💠🔒 "
            else:
                icon = "📄 "
            tree.add(Text(icon) + text_filename)


def rich_tree(path=os.getcwd()):
    """
    Prints Rich Tree
    :param path: path_item
    """
    try:
        directory = os.path.abspath(path)
    except IndexError as ie:
        logger("f{ie}", "error")
    else:
        tree = Tree(f":open_file_folder: [link file://{directory}]{directory}",guide_style="bold bright_blue",)
        walk_directory(Path(directory), tree)
        printf(tree)