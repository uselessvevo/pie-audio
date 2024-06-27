from __future__ import annotations

import dataclasses as dt


@dt.dataclass(frozen=True, slots=True, eq=False)
class Index:
    Start = 0
    End = -1
