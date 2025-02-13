"""Console script for folin_v1."""
import folin_v1

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for folin_v1."""
    console.print("Replace this message by putting your code into "
               "folin_v1.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
