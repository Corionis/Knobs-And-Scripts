from typing import Any, Dict

from github.GithubObject import NonCompletableGithubObject

class CheckRunAnnotation(NonCompletableGithubObject):
    def __repr__(self) -> str: ...
    def _initAttributes(self) -> None: ...
    def _useAttributes(self, attributes: Dict[str, Any]) -> None: ...
    @property
    def annotation_level(self) -> str: ...
    @property
    def end_column(self) -> int: ...
    @property
    def end_line(self) -> int: ...
    @property
    def message(self) -> str: ...
    @property
    def path(self) -> str: ...
    @property
    def raw_details(self) -> str: ...
    @property
    def start_column(self) -> int: ...
    @property
    def start_line(self) -> int: ...
    @property
    def title(self) -> str: ...
