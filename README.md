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

## Telepítés

### Függőségek

A program **python 3.7** verzióval készült. <br>
A futtatáshoz az alábbi python packagekre lesz szükség:
- numpy
- pygame

### Indítás

`GameMaster.py` futtatása: <br>
Elindítja a játékot. Minden szükséges paraméter a Config.py fileban található, indítás előtt
a paraméterek módosíthatóak.

`Main_Client.py` futtatésa: <br>
Csatlakozó kliens játékos. Ez a file ad mintát az elkészítendő játékos kódjához. A játékosok
saját gépről tudnak majd futni socket kapcsolaton keresztül bejelentkezve.

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

## Útmutató

**Config.py**

| **Paraméter**         | **Default érték**             | **Magyarázat**                                         |
|-----------------------|-------------------------------|--------------------------------------------------------|
| **#GameMaster**       |                               |                                                        |
| GAMEMASTER_NAME       | "master"                      | Game master név                                        |
| IP                    | "localhost"                   | A játék IP címe                                        |
| PORT                  | 42069                         | A játék által nyitott port                             |
| DEFAULT_TICK_LENGTH_S | 0.3                           | Egy TICK lefutási ideje                                |
| DISPLAY_ON            | True                          | Kijelző bekapcsolása                                   |     
| WAIT_FOR_JOIN         | 20                            | Indítás utáni várakozás a játékosok bejelntkezéséhez   |    
| LOG                   | True                          | Logolás be/kikapcsolása                                |           
| LOG_PATH              | './log'                       | Logfileok mentési helye                                |  
| **#Engine**           |                               |                                                        |           
| MAPPATH               | "./maps/02_base.txt"          | Játék térkép elérési útja                              |
| FIELDUPDATE_PATH      | "./fieldupdate/01_corner.txt" | Kaja termelődés valószínűségi térképének elérési útja  |
| STARTING_SIZE         | 5                             | Kezdő játékos méret                                    |
| MIN_RATIO             | 1.1                           | Bekebelezési arány (a kisebb játékos méretét tekintve) |
| STRATEGY_DICT         | {}                            | Játékos stratégiák                                     |
| VISION_RANGE          | 5                             | Játékosok látási távolsága                             |
| UPDATE_MODE           | "statistical"                 | Kaja újratermelődés módja (static - nincs termelődés)  |
| DIFF_FROM_SIDE        | 1                             | Kezdő pozíciók távolsága a pálya szélétől (4 sarok)    |
| FOODGEN_COOLDOWN      | 10                            | Kaja termelődés ciklusideje tickekben                  |
| FOODGEN_OFFSET        | 10                            | Kaja termelődés először ebben a Tickben                |
| FOODGEN_SCALER        | 0.3                           | Kaja termelődés valószínűségi térképének módosítója.   |
| MAXTICKS              | 100                           | Játék maximális Tick száma                             |
| SOLO_ENABLED          | True                          | A játék futásának engedélyezése solo módba             |

## Credits
Gyöngyösi Natabara (natabara@gyongyossy.hu) <br>
Nagy Balázs (nagybalazs@mogi.bme.hu)