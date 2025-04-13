import argparse

from reports.handlers import HandlersReport
from utils import validate_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('log_files', nargs='+')
    parser.add_argument('--report', required=True)
    args = parser.parse_args()

    if args.report != 'handlers':
        raise ValueError("Поддерживает только отчет handlers")

    validate_files(args.log_files)
    report = HandlersReport.process_files(args.log_files)
    print(report.generate_output())


if __name__ == '__main__':
    main()
