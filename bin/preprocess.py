import io
import tokenize
import ast
import time
from rich.progress import Progress, SpinnerColumn, TextColumn

class SnippetNotEvaluated(Exception):
    pass

class Snippet:
    _model_loaded = False

    def __init__(self, code, file_name, start, end):
        self.code = code
        self.file = file_name
        self.pos = [start, end]
        self.vuln = []
        self.pred = []

    def preprocess(self):
        self.code = preprocess_snippet(self.code)

    def evaluate(self):
        if not Snippet._model_loaded:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient = True
            ) as progress:
                progress.add_task(description="Loading model...", total = None)
                from model import classify_snippet # lazy loading
                Snippet._classify_snippet = classify_snippet
                Snippet._model_loaded = True
            classify_snippet = Snippet._classify_snippet
        else:
            classify_snippet = Snippet._classify_snippet

        preds, vuln = classify_snippet(self.code)
        self.vuln = vuln
        self.pred = (preds if preds else ['none'])

    def getVuln(self):
        if not self.vuln:
            raise SnippetNotEvaluated()
        return self.vuln

    def getPred(self, stream = None):
        if not self.pred:
            raise SnippetNotEvaluated()
        return self.pred

    def isVulnerable(self) -> bool:
        if not self.pred:
            raise SnippetNotEvaluated()
        return 'none' not in self.pred

# Removes white-lines and comments from a snippet (string) of code
def preprocess_snippet(snippet: str) -> str:
	output_code = []
	io_obj = io.StringIO(snippet)

	prev_toktype = tokenize.INDENT
	last_lineno = -1
	last_col = 0

	for tok in tokenize.generate_tokens(io_obj.readline):
		token_type, token_string, start, end, line = tok
		start_line, start_col = start
		end_line, end_col = end

		if token_type == tokenize.COMMENT:
			continue #skips comments
		elif token_type == tokenize.NL or token_type == tokenize.NEWLINE:
			if output_code and not output_code[-1].endswith('\n'):
				output_code.append("\n")
			continue
		elif token_type == tokenize.STRING and prev_toktype == tokenize.INDENT:
			continue

		if start_line > last_lineno:
			last_col = 0

		if start_col > last_col:
			output_code.append(" " * (start_col - last_col))

		output_code.append(token_string)
		prev_toktype = token_type
		last_lineno = end_line
		last_col = end_col

	# Rimuove righe vuote finali
	cleaned = "".join(output_code)
	cleaned_lines = [line for line in cleaned.splitlines() if line.strip()]
	return "\n".join(cleaned_lines)

# Divides the snippet (string) into chunks
def preparse_python_code(snippet_code:str, file_name):
    try:
        tree = ast.parse(snippet_code)
    except (SyntaxError, IndentationError) as e:
        return []

    lines = snippet_code.splitlines(keepends = True)
    chunks = []
    occupate = set()

    def find_block_end(node):
        start = node.lineno - 1
        indent = len(lines[start]) - len(lines[start].lstrip())
        end = start + 1
        while end < len(lines):
            line = lines[end]
            if line.strip() == "":
                end += 1
                continue
            line_indent = len(line) - len(line.lstrip())
            if line_indent <= indent and not line.lstrip().startswith("@"):
                break
            end += 1
        return end

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = node.lineno - 1
            end = find_block_end(node)
            for i in range(start, end):
                occupate.add(i)
            chunk_code = "".join(lines[start:end])
            chunk = Snippet(code = chunk_code, file_name = file_name, start = start + 1, end = end - 1)
            chunks.append(chunk)

    top_blocks = []
    current_block = []

    for i, line in enumerate(lines):
        if i in occupate:
            if current_block:
                top_blocks.append(current_block)
                current_block = []
            continue
        if line.strip() == "":
            if current_block:
                top_blocks.append(current_block)
                current_block = []
            continue
        current_block.append((i, line))

    if current_block:
        top_blocks.append(current_block)

    for block in top_blocks:
        start = block[0][0]
        end = block[-1][0] + 1
        code = "".join(r for _, r in block)
        chunk = Snippet(code=code.rstrip(), file_name=file_name, start=start + 1, end = end - 1)
        chunks.append(chunk)

    chunks.sort(key=lambda s: s.pos[0])

    # Returns a list of Snippet
    return chunks

# 09/08/25