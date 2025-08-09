import pyfiglet
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.tree import Tree
from rich.syntax import Syntax
from model_utils import Snippet, VulnerableFile
from main_utils import print_message
from config import APP_NAME, MODEL_PATH, LABELS_PATH, THRESHOLD, VERSION, AUTHOR

main_console = Console()

def print_banner():
    ascii_banner = pyfiglet.figlet_format(APP_NAME, font = "double_blocky") # double_blocky calvin_s dos_rebel
    banner_text = Text(ascii_banner)
    subtitle = Text(f"by {AUTHOR}", style = "italic dim white", justify="center")

    group = Group(Align.center(banner_text), Align.center(subtitle))
    panel = Panel(
        group,
        title = "[bold white]Welcome[/bold white]",
        border_style = "bold #b8860b",
        padding = (1, 4)
        )
    main_console.print(panel)

def print_program_info(select = None):
    main_console.print("")
    table = Table(title="[bold]Program Information[/bold]", title_justify = "left", show_header = False, box = None, show_lines = False)
    table.add_column(style="bold yellow", justify="left")
    table.add_column(style = "white", justify="left")
    table.add_row("Version", VERSION)
    table.add_row("Model path", str(MODEL_PATH))
    table.add_row("Labels path", str(LABELS_PATH))
    table.add_row("Threshold", str(THRESHOLD))
    table.add_row("Search for", select if select else "any")

    main_console.print(table)
    main_console.print("")

def print_tree(root_path, files: list):
    root_tree = Tree(f"[bold green]{root_path}[/bold green]")
    for f in files:
        root_tree.add(f.name)
    main_console.print("")    
    main_console.print(root_tree)
    main_console.print("")

def get_console(stream = None):
    if stream:
        return Console(file = open(stream, "a", encoding = "utf-8"))
    return main_console

def print_snippet(snippet: Snippet, console, show_all = False):
    try:
        header = f"[red]Snippet[/red]  lines {snippet.pos[0]}-{snippet.pos[1]} | [yellow]{' '.join(snippet.getPred())}[/yellow]"
    except SnippetNotEvaluated as e:
        header = f"[red]Snippet[/red]  lines {snippet.pos[0]}-{snippet.pos[1]} | [red]Unknown[/red]"
        print_message("Snippet not evaluated yet", msg_type = "err", console = console)
    console.print(Panel.fit(header, style = "bold", border_style = "red"))

    syntax = Syntax(snippet.code, "python", theme = "monokai", line_numbers = True)
    console.print(syntax)
    console.print("")

    if show_all:
        try:
            table = Table(title = "Output Metrics", show_lines = True, border_style = "white", header_style = "bold magenta")
            table.add_column("Label", style = "bold", justify = "left")
            table.add_column("Probability", style = "white", justify = "right")

            for label, prob in snippet.getVuln():
                table.add_row(label, f"{prob:.3f}")

            console.print(table)
            console.print("")

        except SnippetNotEvaluated as e:
            pass

def print_file_header(file: VulnerableFile, console, select = None):
    console.rule(f"[bold]Summary for file: {file.file_name}[/bold]")

    info = Table(show_header = False, box = None)
    info.add_row("[bold]Size[/bold]", file.size)
    info.add_row("[bold]Chunks[/bold]", str(len(file.snippets)))
    info.add_row("[bold]Searched Vulnerability[/bold]", f"{select or 'any'}")
    info.add_row("[bold]Vulnerable Chunks[/bold]", f"{len(file.vulnSnippets)}")
    console.print(info)
    console.print("")

def print_summary(file: VulnerableFile, stream = None, show_all = False, select = None):
    console = get_console(stream)
    print_file_header(file, console, select)

    if file.vulnSnippets:
        for snippet in file.vulnSnippets:
            print_snippet(snippet, console, show_all)
    else:
        console.print(Panel.fit(f"safe according to searched vulnerability ({select})", border_style = "green", title = "[bold green]Safe[/bold green]"))
    console.print("")

    if stream:
        console.file.close()

# Display chunk segmentation
def print_debug_info(file: VulnerableFile):

    main_console.rule(f"[bold]Debug info for file: {file.file_name}[/bold]")

    info = Table(show_header = False, box = None)
    info.add_row("[bold]Size[/bold]", f"{file.size}")
    info.add_row("[bold]Chunks[/bold]", str(len(file.snippets)))
    main_console.print(info)

    if file.snippets:
        for index, snippet in enumerate(file.snippets):
            main_console.print(Panel.fit(f"[green]Snippet[/green] {index + 1} | lines {snippet.pos[0]}-{snippet.pos[1]}", style = "bold", border_style = "green"))
            syntax = Syntax(snippet.code, "python", theme = "monokai", line_numbers = True)
            main_console.print(syntax)
            main_console.print("")
    else:
        print_message("Could not parse the file", msg_type = "err")

def print_labels(labels):
    table = Table(title = "[bold magenta] Labels[/bold magenta]", show_lines = False, show_header = False, title_justify = "left")
    table.add_column(justify = "let")

    for label in labels:
        table.add_row(label)

    main_console.print("")
    main_console.print(table)




