from dataclasses import dataclass
from dataclasses import field


@dataclass
class GameDetails:

    shape: int = 4
    board_size: int = 0
    positions_to_click: list[str] = field(default_factory=list)
