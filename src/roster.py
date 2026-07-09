from dataclasses import dataclass

@dataclass
class NinjaDuo:
    id: int
    name: str
    ninja_1: str
    ninja_2: str
    element: str
    description: str

ROSTER = [
    NinjaDuo(1, "Shadow Strikers", "Kage", "Yoru", "Darkness", "Masters of stealth and assassination."),
    NinjaDuo(2, "Blazing Fists", "Aki", "Homura", "Fire", "Aggressive attackers with high burst damage."),
    NinjaDuo(3, "Frostbite", "Yuki", "Hyoga", "Ice", "They freeze enemies in their tracks."),
    NinjaDuo(4, "Tempest Twins", "Sora", "Kaze", "Wind", "Incredibly fast and agile fighters."),
    NinjaDuo(5, "Earth Shakers", "Iwa", "Daichi", "Earth", "Heavy hitters with impenetrable defense."),
    NinjaDuo(6, "Aqua Dancers", "Mizu", "Umi", "Water", "Fluid movements and healing abilities."),
    NinjaDuo(7, "Thunder Claps", "Rai", "Kaminari", "Lightning", "Stunning strikes and paralyzing shocks."),
    NinjaDuo(8, "Venomous Vipers", "Hebi", "Doku", "Poison", "Masters of damage over time."),
    NinjaDuo(9, "Light Bringers", "Hikari", "Taiyo", "Light", "Blinding speed and holy attacks."),
    NinjaDuo(10, "Steel Forged", "Hagane", "Tetsu", "Metal", "Weapons experts with razor-sharp blades."),
    NinjaDuo(11, "Phantom Veil", "Rei", "Yurei", "Spirit", "Ethereal fighters who pass through attacks."),
    NinjaDuo(12, "Crimson Lotus", "Aka", "Bara", "Blood", "They draw power from their own life force."),
    NinjaDuo(13, "Silent Owls", "Fukuro", "Mori", "Wood", "Nature aligned assassins."),
    NinjaDuo(14, "Iron Claws", "Tora", "Kuma", "Beast", "Feral fighting styles and immense strength."),
    NinjaDuo(15, "Sand Vipers", "Suna", "Sabaku", "Sand", "Mirage creators and desert wanderers."),
    NinjaDuo(16, "Moonlight Blades", "Tsuki", "Hoshi", "Lunar", "Powerful under the night sky."),
    NinjaDuo(17, "Sun Flares", "Natsu", "Hi", "Solar", "Burn with the intensity of the sun."),
    NinjaDuo(18, "Gravity Benders", "Juryoku", "Inryoku", "Gravity", "Control the weight of objects and foes."),
    NinjaDuo(19, "Time Weavers", "Toki", "Jikan", "Time", "Manipulate the flow of combat."),
    NinjaDuo(20, "Space Drifters", "Kukan", "Sora", "Void", "Teleportation and spatial distortions."),
    NinjaDuo(21, "Sonic Booms", "Oto", "Hibiki", "Sound", "Deafening attacks and echolocation."),
    NinjaDuo(22, "Crystal Shards", "Kessho", "Ishi", "Crystal", "Reflective defense and sharp projectiles."),
    NinjaDuo(23, "Magma Cores", "Yogan", "Kazai", "Magma", "Melt through any obstacle."),
    NinjaDuo(24, "Storm Callers", "Arashi", "Kumo", "Storm", "Unpredictable weather manipulation."),
    NinjaDuo(25, "Dream Walkers", "Yume", "Maboroshi", "Illusion", "Confuse enemies with false realities."),
    NinjaDuo(26, "Bone Crushers", "Hone", "Gaikotsu", "Bone", "Macabre warriors with skeletal armor."),
    NinjaDuo(27, "Soul Reapers", "Tamashii", "Shin", "Death", "Steal the essence of their targets."),
    NinjaDuo(28, "Mind Benders", "Seishin", "Noha", "Psychic", "Telekinesis and mental assaults."),
    NinjaDuo(29, "Plasma Sparks", "Purazuma", "Senko", "Plasma", "Superheated energy beams."),
    NinjaDuo(30, "Mirror Images", "Kagami", "H反射", "Mirror", "Reflect attacks back at the sender."),
    NinjaDuo(31, "Smoke Screens", "Kemuri", "Kiri", "Smoke", "Choke out enemies and disappear."),
    NinjaDuo(32, "Ash Fallers", "Hai", "Sumi", "Ash", "Remnants of destruction."),
]
