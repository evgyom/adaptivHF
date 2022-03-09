<img src="/pics/GPK_BME_MOGI.png">

game master játék indítás <br>
client csatlakozás <br>
configba futtatási paraméterek <br>
playerbe random botok <br>

# AdaptIO

Az AdaptIO az "Adaptív rendszerek modellezése" tárgyhoz készült játék felület. A tárgy sikeres teljesítéséhez 
szükséges házi feladat egy agent elkészítése, mely elboldogul az AdaptIO játékban. A cél az életben maradás.

A feladat sikeres teljesítésének feltétele az agent kódjának beadása, illetve egy rövid prezentáció a szemeszter
végén, melyen az agent logikájának kialakítását és betanításának főbb lépéseit mutatják be a csapatok. Az agenteket
ez után természetesen egymással is megversenyeztetjük!

A feladat elkészítése során a tárgyban tanult genetikus, bakteriális vagy neurális háló alapú megoldásokat preferáljuk.
Nem tiltott tovább lépni se és a tárgyban esetlegesen nem érintett teknikákat alkalmazni. A feladat elkészítése során
a környezet szabadon átalakítható, viszont a bemutatás egységesen a master branchen elérhető verziót fogjuk használni.

<img src="/pics/display.png">

## Szabályok

A játékban minden agent egy kockát foglal el. Végrehajtható akcióként egy iterációban 9 választási lehetősége van.
Vagy helyben marad vagy a 8 szomszédos mező valamelyikére mozog.

Az agentek rendelkeznek mérettel, mely a játék kezdetén egy alap paraméter (5). Az agentek mérete a játék során növelhető táplálkozással.
A játéktéren található kaja mezők különböző intenzitással (1, 2, 3). Ha az agent kaját tartalmazó mezőre lép
a bekebelezés automatikusan megtörténik és az agent mérete a kaja méretével növekszik. A pályán továbbá találhatóak falak, melyek nem elmozdíthatóak, nem termelődik rajtük kaja
és rálépni se lehet. Az agentek azonban átlátnak a falakon.

A térképen fellelhető pálya elemek:

<img src="/pics/map.png"> <br>

| Érték |  Jelentés   |   Szín |
|-------|:-----------:|-------:|
| 0     |  üres mező  | szürke |
| 1     |  kaja LOW   |   zöld |
| 2     | kaja MEDIUM |   zöld |
| 3     |  kaja HIGH  |   zöld |
| 9     |     fal     | fekete |


Az agentek egymást is bekebelezhetik, amennyiben az agentek közötti méretkülönbség százalékos formában meghaladja
a 10%-ot.

<img src="/pics/foodupdate.png">

## Credits
Gyöngyösi Natabara (natabara@gyongyossy.hu) <br>
Nagy Balázs (nagybalazs@mogi.bme.hu)