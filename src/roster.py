from dataclasses import dataclass

@dataclass
class NinjaCharacter:
    id: int
    name: str
    element: str
    description: str
    sprite_file: str

ROSTER = [
    NinjaCharacter(1, "Naruto Uzumaki", "Wind", "A hyperactive ninja containing the Nine-Tails. Master of Rasengan.", "player_naruto.png"),
    NinjaCharacter(2, "Sasuke Uchiha", "Lightning", "A rogue ninja seeking power. Master of Chidori and Sharingan.", "player_sasuke.png"),
    NinjaCharacter(3, "Itachi Uchiha", "Darkness", "A genius rogue ninja of Akatsuki. Master of genjutsu.", "player_itachi.png"),
    NinjaCharacter(4, "Kakashi Hatake", "Storm", "The Copy Ninja of Team 7. Master of Chidori and Sharingan.", "player_kakashi.png"),
    NinjaCharacter(5, "Sakura Haruno", "Earth", "A medical ninja with monstrous strength and chakra control.", "player_sakura.png"),
    NinjaCharacter(6, "Gaara", "Sand", "The Kazekage of the Sand. Master of absolute sand defense.", "player_gaara.png"),
    NinjaCharacter(7, "Rock Lee", "Beast", "A taijutsu specialist who can open the Eight Inner Gates.", "player_lee.png"),
    NinjaCharacter(8, "Hinata Hyuga", "Light", "A gentle fist practitioner possessing the Byakugan eyes.", "player_hinata.png"),
    NinjaCharacter(9, "Pain (Nagato)", "Void", "The god-like leader of Akatsuki. Master of Almighty Push.", "player_pain.png"),
    NinjaCharacter(10, "Minato Namikaze", "Solar", "The Fourth Hokage known as the Yellow Flash of the Leaf.", "player_minato.png"),
]
