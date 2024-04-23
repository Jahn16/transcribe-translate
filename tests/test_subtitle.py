from unittest.mock import MagicMock

import pytest
from faster_whisper.transcribe import Segment

from app.utils.subtitle_formatter import SRTFormatter


@pytest.fixture
def segments() -> list[MagicMock]:
    segments = [
        MagicMock(spec=Segment),
        MagicMock(spec=Segment),
        MagicMock(spec=Segment),
    ]
    current_time = 0
    for segment in segments:
        segment.start = current_time
        current_time += 1810
        segment.end = current_time

    segments[0].text = "Hello world"
    segments[1].text = "Hello, how are you?"
    segments[2].text = "Goodbye"
    return segments


def test_str_formatter(segments: list[Segment]) -> None:
    expected_result = """1 
00:00:0,000 --> 00:30:10,000 
Hello world 

2 
00:30:10,000 --> 01:00:20,000 
Hello, how are you? 

3 
01:00:20,000 --> 01:30:30,000 
Goodbye 

"""

    formatter = SRTFormatter()
    result = formatter.format(segments)
    assert result == expected_result
