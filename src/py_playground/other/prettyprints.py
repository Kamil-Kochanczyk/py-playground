import logging
import time

from colorama import Back, Fore, Style
from pydantic import field_serializer
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print as rprint
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
    track,
)
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import install


class MySettings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=False)
    path: str

    @field_serializer("path", mode="plain")
    def path_as_list(self, value: str) -> list[str]:
        return value.split(";")


def colorama_examples() -> None:
    print(f"{Fore.RED}Error: something went wrong.{Style.RESET_ALL}")
    print("Normal text")
    print(f"{Fore.GREEN}Success: everything went good.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Warning: watch out...{Style.RESET_ALL}")
    print(f"{Fore.BLUE}Info: did you know that...{Style.RESET_ALL}")
    print(f"{Style.DIM}{Fore.RED}Not so serious error!!!{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{Fore.BLACK}{Back.WHITE}Highlighted text{Style.RESET_ALL}")


def rich_examples() -> None:
    console = Console()
    console.print("Hello world :smiley:")
    console.print(
        "[bold red]- Whatcha doin?[/bold red], [italic underline green]- Wasting time.[/italic underline green]"
    )
    console.print()

    my_settings = MySettings()  # type: ignore[]
    print(my_settings.model_dump())
    rprint(my_settings.model_dump())
    rprint()

    table = Table(
        title="My Table",
        caption="Caption",
        title_justify="left",
        caption_justify="right",
        width=100,
        show_footer=True,
        footer_style="red",
    )
    table.add_column("Col 1", footer="Foot1", justify="center", style="green")
    table.add_column("Col 2", footer="Foot2", justify="center", style="green")
    table.add_column("Col 3", footer="Foot3", justify="center", style="green")
    table.add_row("[blue]Row 11[/blue]", "Row 12", "Row 13")
    table.add_section()
    table.add_row("Row 21", "Row 22", "Row 23")
    table.add_row("Row 31", "Row 32", "Row 33")
    console.print(table)

    for _ in track(range(10), description="Processing..."):
        time.sleep(0.5)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        SpinnerColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TransferSpeedColumn(),
        DownloadColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task1 = progress.add_task("[cyan]Downloading...", total=200 * 1e6)  # 200 MB
        task2 = progress.add_task("[magenta]Waiting...", total=1e9)  # 1 GB

        while not progress.finished:
            if not progress.tasks[task1].finished:
                progress.update(task_id=task1, advance=500 * 1e3)  # 500 KB
            if not progress.tasks[task2].finished:
                progress.update(task_id=task2, advance=2000 * 1e3)  # 2000 KB

            # 512 KB * 0.01^-1 s^-1 = 512KB * 100 s^-1 = 51200 KB/s = 51,2 MB/s
            # 2048 KB * 0.01^-1 s^-1 = ... = 51,2 MB/s * 4 = 204,8 MB/s
            time.sleep(0.01)

    # print(10 / 0)

    code = """
    def hello():
        print('Hello!')
    """
    syntax = Syntax(code=code, lexer="python", theme="github-dark")
    console.print(syntax)
    console.print()

    logger = logging.getLogger("prettyprints")
    logger.addHandler(RichHandler())
    logger.setLevel(logging.INFO)
    logger.info("Application started")
    logger.warning("Something might be wrong")
    logger.error("Something went wrong")


def main() -> None:
    install()  # install rich traceback output
    colorama_examples()
    print()
    rich_examples()


if __name__ == "__main__":
    main()
