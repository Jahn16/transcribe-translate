import abc
import math

from faster_whisper.transcribe import Segment


class BaseFormatter(abc.ABC):
    @abc.abstractmethod
    def format(self, segments: list[Segment]) -> str:
        raise NotImplementedError


class SRTFormatter(BaseFormatter):
    def format(self, segments: list[Segment]) -> str:
        subtitle = ""
        for index, segment in enumerate(segments, start=1):
            print(segment.start)
            segment_start = self._format_time(segment.start)
            segment_end = self._format_time(segment.end)
            subtitle += f"{index} \n"
            subtitle += f"{segment_start} --> {segment_end} \n"
            subtitle += f"{segment.text} \n"
            subtitle += "\n"
        return subtitle

    def _format_time(self, total_seconds: float) -> str:
        seconds = total_seconds
        hours = math.floor(seconds / 3600)
        seconds %= 3600
        minutes = math.floor(seconds / 60)
        seconds %= 60
        milliseconds = round((seconds - math.floor(seconds)) * 1000)
        seconds = math.floor(seconds)
        return f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
