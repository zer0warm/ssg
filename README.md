# Static site generator

This is my third [Boot](boot.dev)'s project. It is a static site generator written in Python.

The generator currently supports a small subset of Markdown, with some quirks.

## Container blocks

- Paragraphs
- Headings: `<h1> -> <h6>`
- Unordered lists
- Ordered lists
- Block quotes
- Code: `<pre><code>`

In addition, blocks must be separated by blank lines for the generator to recognize. If they stick to each other, the result is a paragraph.

Because of this, unordered lists with `*` markers that stick to (e.g. a heading) might make the text in between `*` becomes *italic*.

Blocks of text are stripped (trimming white spaces from start and end) while splitting, so as a consequence, code blocks are currently dedented.

Block's inner text is generated in HTML exactly like how they appear in Markdown. Newlines are newlines, not spaces. To the browser this makes no differences.

## Leaf blocks

- Text
- **Bold**
- *Italic*
- `Code`
- Image link: with `![alt](src)`
- Link: with `[text](src)`

Currently, HTML entities in text are not escaped.
