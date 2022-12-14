from dataclasses import dataclass, field
from enums import PlayerClass


@dataclass
class Player:
    mmr: int = field(compare = False)
    main: PlayerClass = field(compare = False)
    current_class: PlayerClass = field(compare = True, init=False)
    secondary: PlayerClass = field(compare = False)
    igl: bool = field(compare = False)

    def __post_init__(self) -> None:
        self.current_class = self.main
