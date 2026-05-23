# Internals

Developer documentation for the project's architecture and implementation.

## Documentation pipeline

Morpha's documentation tree mixes hand-written prose and Sphinx-generated API
reference. The two are kept structurally separate:

| Subtree | Authorship | Build participation |
| --- | --- | --- |
| `docs/index.md`, `docs/guide/`, `docs/internals/`, `docs/adr/` | Hand-written Markdown | Not part of the Sphinx build |
| `docs/src/` | Hand-written Sphinx input (`automodule` stubs + toctree) | Sphinx source root |
| `docs/api/` | Generated Markdown | Sphinx output (committed for GitHub browsing) |
| `docs/_build/` | Sphinx doctree cache | Gitignored |

### Why this split

Sphinx requires every file it processes to be reachable via a `{toctree}`
directive. Those directives do not render on GitHub — they appear as literal
fenced code blocks. Restricting Sphinx to `docs/src/` (which Sphinx never
publishes on GitHub) keeps `{toctree}` out of every user-facing file.

The prose tree is plain Markdown that GitHub renders natively. Cross-links
between prose and API are plain Markdown links (`[name](api/components.md)`).

### Trade-offs

- **Gained**: every file under `docs/` (except `docs/src/`) is readable directly
  on GitHub. No `{toctree}` source code in user-facing files.
- **Given up**: Sphinx's `:ref:` / `:doc:` cross-reference validation no longer
  applies to the prose. Broken Markdown links in prose are caught by review,
  not by the build.

## Rebuilding the API

Run from `docs/`:

```bash
make api      # regenerate docs/api/*.md from docstrings
make html     # build an HTML preview into docs/_build/html/
make clean    # remove generated API docs and the build cache
```

The API regeneration is deterministic: every `make api` produces byte-identical
output for unchanged source. Commit the regenerated `docs/api/*.md` files
alongside any docstring changes that produced them.

## Configuration

The Sphinx configuration lives at `docs/src/conf.py`. Key choices:

- `sphinx_markdown_builder` is the active builder for `docs/api/`.
- `sphinx.ext.napoleon` translates NumPy-style docstrings into reStructuredText
  before autodoc processes them. NumPy docstrings are the project standard.
- `napoleon_custom_sections = [("Class Attributes", "params_style")]` registers
  the project's custom `Class Attributes` docstring section so it renders as a
  parameter-style list instead of being folded into the preceding `Parameters`
  section.
- `visit_seealso` is monkey-patched in `setup()` to render `See Also` docstring
  sections as Markdown blockquote admonitions (`> **See also**`) instead of the
  builder's default `#### SEE ALSO` H4 heading.
