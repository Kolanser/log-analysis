from collections import defaultdict
from typing import Dict
from reports.base import BaseReport

LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class HandlersReport(BaseReport):
    def __init__(self) -> None:
        self.handlers = defaultdict(lambda: defaultdict(int))
        self.totals = defaultdict(int)

    def _handle_parsed_line(self, parsed_line: Dict[str, str]) -> None:
        if parsed_line['logger'] != 'django.request':
            return
        handler = parsed_line['handler']
        level = parsed_line['level']
        self.handlers[handler][level] += 1
        self.totals[level] += 1

    def generate_output(self) -> str:
        sorted_handlers = sorted(self.handlers.items())
        total = sum(self.totals.values())
        header = "HANDLER                \t" + "\t".join(f"{level:8}" for level in LEVELS)
        lines = [
            f"Total requests: {total}\n",
            header,
            *[f"{h:20}\t" + "\t".join(f"{counts.get(level,0):8}" for level in LEVELS)
              for h, counts in sorted_handlers],
            f"{'':20}\t" + "\t".join(f"{self.totals.get(level,0):8}" for level in LEVELS)
        ]
        return "\n".join(lines)
