import re
from typing import Dict, List

LOG_PATTERN = re.compile(
    r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) (\w+) (.+): (.*) ((\/[\w\-]+\/?)+) (.*)$'
)


class BaseReport:
    @classmethod
    def process_files(cls, file_paths: List[str]) -> 'BaseReport':
        report = cls()
        for path in file_paths:
            report._process_file(path)
        return report

    def _process_file(self, path: str) -> None:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                self.process_line(line.strip())

    def process_line(self, line: str) -> None:
        parsed = self.parse_line(line)
        if parsed:
            self._handle_parsed_line(parsed)

    def parse_line(self, line: str) -> Dict[str, str]:
        match = LOG_PATTERN.match(line)
        return {
            'timestamp': match.group(1),
            'level': match.group(2),
            'logger': match.group(3),
            'handler': match.group(5)
        } if match else {}

    def _handle_parsed_line(self, parsed_line: Dict[str, str]) -> None:
        raise NotImplementedError()
