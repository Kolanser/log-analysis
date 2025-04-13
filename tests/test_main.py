import pytest
from reports.handlers import HandlersReport, LEVELS
import sys

SAMPLE_LOGS = [
    "2025-03-28 12:44:46,000 INFO django.request: GET /api/v1/reviews/ 204 OK [192.168.1.59]",
    "2025-03-28 12:21:51,000 INFO django.request: GET /admin/dashboard/ 200 OK [192.168.1.68]",
    "2025-03-28 12:40:47,000 CRITICAL django.core.management: DatabaseError: Deadlock detected",
    "2025-03-28 12:25:45,000 DEBUG django.db.backends: (0.41) SELECT * FROM 'products' WHERE id = 4;",
    "2025-03-28 12:03:09,000 DEBUG django.db.backends: (0.19) SELECT * FROM 'users' WHERE id = 32;",
    "2025-03-28 12:05:13,000 INFO django.request: GET /api/v1/reviews/ 201 OK [192.168.1.97]",
    (
        "2025-03-28 12:11:57,000 ERROR django.request: Internal Server Error: /admin/dashboard/ [192.168.1.29] - "
        "ValueError: Invalid input data"
    )
]


@pytest.fixture
def sample_log(tmp_path):
    log_file = tmp_path / "test.log"
    log_file.write_text("\n".join(SAMPLE_LOGS))
    return str(log_file)


def test_handler_report(sample_log):
    report = HandlersReport.process_files([sample_log])
    output = report.generate_output()

    assert "Total requests: 4" in output
    assert "/api/v1/reviews/" in output
    assert "INFO" in output
    assert "DEBUG" in output


def test_invalid_report_type():
    with pytest.raises(ValueError):
        sys.argv = ['main.py', 'file.log', '--report=invalid']
        import main
        main.main()


def test_file_validation():
    with pytest.raises(FileNotFoundError):
        HandlersReport.process_files(["non_existent.log"])


def test_output_formatting(sample_log):
    report = HandlersReport.process_files([sample_log])
    output = report.generate_output().split('\n')

    assert len(output) == 6
    assert all(level in output[2] for level in LEVELS)
