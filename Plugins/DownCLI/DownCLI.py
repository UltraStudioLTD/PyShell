#!/usr/bin/env python3
"""DownCLI Plugin for PyShell"""
import os.path
import signal
from concurrent.futures import ThreadPoolExecutor
import requests
from rich import print as printf, pretty
from rich.progress import *
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

pretty.install()
console = Console()
__package__ = "[red]DownCLI-Plugin[/]"
__version__ = "[yellow]0.0.1[/]"
__description__ = "DownCLI Plugin for PyShell"
__package_link__ = "[bold black on white]Git[/][bold italic]Hub[/]: https://www.github.com/UltraStudioLTD/DownCLI"
__author__ = "[bold blue]Luka Mamukashvili[/] ([bold black on white]Git[/][bold italic]Hub[/]: [italic cyan]UltraStudioLTD[/])"
__author_links__ = "[bold black on white]Git[/][bold italic]Hub[/]: https://www.github.com/UltraStudioLTD\n[bold black on white]Dev[/]: https://www.dev.to/ultrastudio"
progress = Progress(TextColumn("[{task.fields[response_code]}] <[bold yellow]{task.fields[content_type]}[/]> [bold blue]{task.fields[filename]}", justify="right"), BarColumn(bar_width=None), "[progress.percentage]{task.percentage:>3.1f}%", "•", DownloadColumn(), "•", TransferSpeedColumn(), "•", TimeRemainingColumn(), TimeElapsedColumn(), SpinnerColumn())
done_event = Event()


def handle_sigint():
    """HandleSigint"""
    done_event.set()


signal.signal(signal.SIGINT, handle_sigint)


def copy_url(task_id: TaskID, url: str, path: str) -> None:
    """
    Download URL
    :param task_id: task ID
    :param url: URL to Download
    :param path: Destination path
    """
    progress.console.log(f"Requesting {url}")
    response = requests.get(url, stream=True)
    meta = requests.head(url)
    if "Content-Length" in meta.headers:
        progress.update(task_id, total=int(meta.headers["Content-Length"]))
    else:
        progress.update(task_id, total=int(len(response.content)))
    with open(path, "wb") as destination_file:
        progress.start_task(task_id)
        for data in response.iter_content(32768):
            destination_file.write(data)
            progress.update(task_id, advance=len(data))
            if done_event.is_set():
                return
    progress.console.log(f"Downloaded {path}")


def downcli(urls: Iterable[str], destination_dir: str):
    """
    Runner for DownCLI
    :param urls: Links to download
    :param destination_dir: Download Directory
    """
    with progress:
        with ThreadPoolExecutor(max_workers=4) as pool:
            for url in urls:
                filename = url.split("/")[-1]
                response = requests.head(url)
                content_type = requests.head(url).headers['Content-Type'].split(';')[0]
                if content_type == "text/plain" and len(filename.split(".")) == 1:
                    filename += '.txt'
                destination_path = os.path.join(destination_dir, filename)
                response_code = f"[green]{str(response.status_code)}[/]" if response.status_code == requests.codes.ok else response_code = f"[red]{str(response.status_code)}[/]"
                task_id = progress.add_task("download", filename=filename, contenttype=content_type, responsecode=response_code, start=False)
                pool.submit(copy_url, task_id, url, destination_path)


def print_downcli_help_msg():
    """Prints Help Message for DownCLI Plugin"""
    description_panel = Panel.fit(f"{__description__}\n\tby: {__author__}",
                                  title="Package [italic purple]Description[/]", border_style="green")
    usage_panel = Panel.fit(
        "\tUsage: [bold blue]downcli[/] [[bold italic]-h, --help[/]] [[bold italic]-d, --directory[/] [purple]DOWNLOAD_DIRECTORY[/]] [bold italic red]URLs[/]",
        title="Package [italic yellow]Command Line Usage[/]", border_style="purple")
    help_table = Table(title="[bold italic yellow]Usage Help[/]")
    package = Table(title="[bold italic yellow]Package[/]")
    package.add_row(description_panel)
    package.add_row(usage_panel)
    help_table.add_column("Argument Type")
    help_table.add_column("Argument(s)")
    help_table.add_column("Argument(s)'s Description")
    help_table.add_row("Optional", "[yellow]-h[/], [yellow]--help[/]", "Prints [purple]help[/] message and [yellow]exits[/]")
    help_table.add_row("Optional", "[yellow]-v[/], [yellow]--version[/]", "Prints [red]version[/] of plugin and [yellow]exits[/]")
    help_table.add_row("Optional", "[yellow]-d[/], [yellow]--directory[/] [purple]DOWNLOAD_DIRECTORY[/]", "Changes [purple]download[/] directory")
    help_table.add_row("Positional", "[bold italic red]URLs[/]", "Downloads [bold italic red]URLs[/] ([bold italic blinking red]Required[/])")
    package_info = Table(title="Package Info")
    package_info.add_row(Panel.fit(f"{__package_link__}", title="Package Link", border_style="yellow"))
    package_info.add_row(Panel.fit(f"{__author_links__}", title="Author Links", border_style="cyan"))
    als_table = Table()
    als_table.add_row(package_info)
    als_table.add_row(help_table)
    console.print(Panel.fit(als_table, title=f"{__package__} v{__version__}", border_style="blue"))