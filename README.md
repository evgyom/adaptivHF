<img src="/pics/GPK_BME_MOGI.png">

# AdaptIO

Az AdaptIO az "Adaptív rendszerek modellezése" tárgyhoz készült játék felület. A tárgy sikeres teljesítéséhez 
szükséges házi feladat egy agent elkészítése, mely elboldogul az AdaptIO játékban. A cél az életben maradás.

A feladat sikeres teljesítésének feltétele az agent kódjának beadása, illetve egy rövid prezentáció a szemeszter
végén, melyen az agent logikájának kialakítását és betanításának főbb lépéseit mutatják be a csapatok. Az agenteket
ez után természetesen egymással is megversenyeztetjük!

A feladat elkészítése során a tárgyban tanult genetikus, bakteriális vagy neurális háló alapú megoldásokat preferáljuk.
Nem tiltott tovább lépni se és a tárgyban esetlegesen nem érintett technikákat alkalmazni. A feladat elkészítése során
a környezet szabadon átalakítható, viszont a bemutatás egységesen a master branchen elérhető verziót fogjuk használni.

<img src="/pics/displayy.png">

## Telepítés

Repository letöltése vagy clonozása.

    git clone www.....

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

A játékban minden agent egy kockányi mezőt foglal el. Végrehajtható akcióként egy iterációban 9 választási lehetősége van.
Vagy helyben marad vagy a 8 szomszédos mező valamelyikére mozog.

Az agentek rendelkeznek mérettel, mely a játék kezdetén egy alap paraméter (5). Az agentek mérete a játék során növelhető táplálkozással.
A játéktéren találhatók kaja mezők különböző intenzitással (1, 2, 3). Ha az agent kaját tartalmazó mezőre lép
a bekebelezés automatikusan megtörténik és az agent mérete a kaja méretével növekszik. A pályán továbbá találhatóak falak, melyek nem elmozdíthatóak, nem termelődik rajtük kaja
és rálépni se lehet. Az agentek átlátnak a falakon.

Ha több játokos azonos időben ugyan arra a mezőre lépne:
- először ellenőrizzük, hogy a legnagyobb játékos meg tudja-e enni a második legnagyobbat.
- ha igen, mindenkit megeszik.
- ha nem a játékosok korábbi helyükön maradnak, mintha nem léptek volna.

A bekebelezés (egyik játékos megeszi a másikat) akkor jön létre, ha a kisebb játékos méretét felszorozzuk
a Config.py fileban található MIN_RATIO paraméterrel és még így is kisebb, mint a nagyobb játékos.
Minden más esetben a játékosok közti méretkülönbség túl kicsi, így csak lepattanak egymésról és korábbi helyükön maradnak.
 
### Pálya elemek:

<img src="/pics/map.png"> <br>

| Érték |  Jelentés   |   Szín |
|-------|:-----------:|-------:|
| 0     |  üres mező  | szürke |
| 1     |  kaja LOW   |   zöld |
| 2     | kaja MEDIUM |   zöld |
| 3     |  kaja HIGH  |   zöld |
| 9     |     fal     | fekete |

Előre generált pályák a maps mappában találhatóak, de további pályák is generálhatóak a feladat minél jobb
megoldása érdekében. Pályageneráláshoz hasznos lehet a maps.xlsx fájl. 

### Kaja frissítési térkép

<img src="/pics/foodupdate.png">

Minden mezőhöz a pályán tartozik egy kaja termelődési valószínűség, mely segítségével a játék
lefutása során a kaják térképen való elhelyezkedése jelentősen megváltozhat. A Config.py fileban
rögzített paraméterek szerint bizonyos tickenként valamilyen térkép elosztás szerint random helyeken
1 értékű kaják jelennek meg, melyek a tickek során felhalmozódhatnak 2 vagy 3 szintig. 

## Útmutató

### Paraméterek

**Config.py** <br>
Ez a file tartalmazza a játék főbb beállításait, melyeket a készülés során is lehet állítani. Illetve
itt vannak meghatározva a játékszabályok és a kijelző színpalettája.

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

### Játékos stratégiák

**Player.py** <br>
Ez a file tartalmaz pár előre megírt botot, melyekkel tesztelhető a rendszer és az új fejlesztésű játékos teljesítménye.

**RemotePlayerStrategy:**<br>
A távoli csatlakozású játékos. Erre a beállításra lesz szükség a saját játékosunk futtatásához.
A `Main_Client.py`-ban kódolt 'hunter' így tud csatlakozni a GameMasterhez.

**DummyStrategy:** <br>
Indítás után meghaló játékos.

**RandBotStrategy:** <br>
Random akciókat választó játékos.

**NaiveStrategy:** <br>
Legközelebbi legnagyobb értékű kaja felé haladó játékos.

**NaiveHunterStrategy:** <br>
Legközelebbi legnagyobb értékű kaja felé haladó játékos, de ha másik játékost lát és nagyobb
nála, akkor vadászk rá.

## Credits
Gyöngyösi Natabara (natabara@gyongyossy.hu) <br>
Nagy Balázs (nagybalazs@mogi.bme.hu)