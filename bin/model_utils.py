from pathlib import Path
from preprocess import preprocess_snippet, preparse_python_code, Snippet, SnippetNotEvaluated
from main_utils import getSize, print_message

class VulnerableFile:
    def __init__(self, file_name: Path, code):
        self.file_name = file_name
        self.size = getSize(self.file_name)
        self.snippets = preparse_python_code(code, file_name)
        self.vulnSnippets = []
        for snippet in self.snippets:
            snippet.preprocess()
        self.__clean()

    # Removes empty Snippets after pre-processing
    def __clean(self):
        self.snippets = [snippet for snippet in self.snippets if snippet.code]

    # Init the vulnSnippet list after evaluation and according to `select` parameter
    def __findVuln(self, select=None):
        self.vulnSnippets = []
        not_evaluated_found = False
        if select:
            print_message(f"Filtering for chosen vulnerability: {select}", msg_type = "info")
        for snippet in self.snippets:
            try:
                if snippet.isVulnerable() and (select is None or select in snippet.getPred()):
                    self.vulnSnippets.append(snippet)
            except SnippetNotEvaluated:
                not_evaluated_found = True
        if not_evaluated_found:
            raise SnippetNotEvaluated(f"Some snippets from {self.file_name} may not have been evaluated at __findVuln() time")


    def evaluate(self, select = None):
        if not self.snippets:
            raise SnippetNotEvaluated(f"Failed to pre-parse {self.file_name}: it may contain syntax errors")
        for snippet in self.snippets:
            snippet.evaluate()
        try:
            self.__findVuln(select)
        except SnippetNotEvaluated as e:
            print_message(f"{e}", msg_type = "warn")
        print_message(f"File {self.file_name} successfully evaluated", msg_type = "info")

def init_vulnFile_from_path(path: Path) -> VulnerableFile:
    print_message(f"Parsing and preprocessing file {path}...", msg_type = "info")
    with open(path, "r", encoding="utf-8") as file:
        string_file = file.read()
    return VulnerableFile(path, string_file)
    print_message(f"File {path} successfully parsed and preprocessed.", msg_type = "info")

# 09/08/25