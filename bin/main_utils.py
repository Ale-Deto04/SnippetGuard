import subprocess
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

main_console = Console()

def isPythonFile(path: Path) -> bool:
    result = subprocess.run(["file", str(path)], capture_output = True, text = True)
    return "Python script" in result.stdout

def getSize(path: Path) -> str:
    size_kb = path.stat().st_size / 1024
    return f"{size_kb:.1f} KB" if size_kb >= 1 else f"{path.stat().st_size} B"

def print_message(message: str, msg_type, console = main_console):
    timestamp = datetime.now().strftime("%H:%M:%S")
    match msg_type:
        case "info":
            console.print(f"[white not bold]{timestamp}[/white not bold] [bold cyan][INFO][/bold cyan]: {message}")
        case "warn":
            console.print(f"[white not bold]{timestamp}[/white not bold] [bold #FFA500][WARN][/bold #FFA500]: {message}")
        case "err":
            console.print(Panel.fit(f"[white not bold]{timestamp}[/white not bold] {message}", border_style = "red", title = "[bold red]Error[/bold red]"))
        case _:
            console.print(f"[white not bold ]{timestamp}[/white not bold] {message}")

# 09/08/25