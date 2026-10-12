"""Restore proven original prose without reserializing HTML or executable data."""
import html
import re
from html.parser import HTMLParser

from scripts.site_translation_catalog import normalize

VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
SKIP = {'script', 'style', 'code', 'pre', 'textarea'}
ATTRIBUTES = re.compile(r'''(?P<name>[^\s/>=]+)(?:\s*=\s*(?:"(?P<double>[^"]*)"|'(?P<single>[^']*)'|(?P<bare>[^\s>]+)))?''')
DISPLAY_ATTRIBUTES = {'title', 'aria-label', 'placeholder', 'alt'}


class OriginalRestorer(HTMLParser):
    def __init__(self, source, replacements, label):
        super().__init__(convert_charrefs=False)
        self.source = source
        self.replacements = replacements
        self.label = label
        self.stack = []
        self.pending = None
        self.edits = []
        self.lines = [0]
        self.lines.extend(match.end() for match in re.finditer('\n', source))

    def absolute_position(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def blocked(self):
        return bool(self.stack and self.stack[-1][1])

    def flush(self, end):
        if self.pending is not None:
            start, self.pending = self.pending, None
            raw = self.source[start:end]
            original = None if self.blocked() else self.replacements.get(normalize(html.unescape(raw)))
            if original is not None and not self.blocked():
                text = html.escape(original, quote=False)
                if (not self.stack or self.stack[-1][0] not in {'title', 'option'}) and not any(tag == 'svg' for tag, _ in self.stack):
                    text = ('<span class="translation-original-fragment" lang="en" data-original-source '
                            f'data-label="{html.escape(self.label, quote=True)}">{text}</span>')
                leading = raw[:len(raw) - len(raw.lstrip())]
                trailing = raw[len(raw.rstrip()):]
                self.edits.append((start, end, leading + text + trailing))

    def handle_data(self, data):
        if self.pending is None:
            self.pending = self.absolute_position()

    def handle_entityref(self, name):
        self.handle_data(name)

    def handle_charref(self, name):
        self.handle_data(name)

    def start(self, tag, attrs, closed):
        position = self.absolute_position()
        self.flush(position)
        blocked = self.blocked() or tag in SKIP or 'data-original-source' in dict(attrs)
        if not blocked:
            raw = self.get_starttag_text()
            tag_end = re.match(r'<\s*[^\s/>]+', raw).end()
            for match in ATTRIBUTES.finditer(raw, tag_end):
                if match['name'].lower() not in DISPLAY_ATTRIBUTES:
                    continue
                group = next((key for key in ('double', 'single', 'bare') if match[key] is not None), None)
                if group is None:
                    continue
                original = self.replacements.get(normalize(html.unescape(match[group])))
                if original is not None:
                    value = html.escape(original, quote=True)
                    if group == 'bare':
                        value = '"' + value + '"'
                    self.edits.append((position + match.start(group), position + match.end(group), value))
        if not closed and tag not in VOID:
            self.stack.append((tag, blocked))

    def handle_starttag(self, tag, attrs):
        self.start(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self.start(tag, attrs, True)

    def handle_endtag(self, tag):
        self.flush(self.absolute_position())
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_comment(self, data):
        self.flush(self.absolute_position())

    def handle_decl(self, decl):
        self.flush(self.absolute_position())

    def handle_pi(self, data):
        self.flush(self.absolute_position())


def restore_original_fragments(source, replacements, label):
    parser = OriginalRestorer(source, replacements, label)
    parser.feed(source)
    parser.close()
    parser.flush(len(source))
    result = source
    boundary = len(source)
    for start, end, value in sorted(parser.edits, reverse=True):
        if end > boundary:
            raise ValueError('Original-prose replacements overlap')
        result = result[:start] + value + result[end:]
        boundary = start
    return result, len(parser.edits)
