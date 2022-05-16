# Adaptiv rendszerek modellezése - HF
Honti Kristóf, Tatai Mihály

## Modell
A feladat megoldására a megerősítéses tanulást választottuk, pontosabban a policy gradient módszert. A módszer lényege, hogy a neurális háló modell kimenete az egyes akciókhoz köthető valószínüséget adja vissza. A háló bemenete pedig az ágens látómezeje (néhány modellünk esetén a pozíció). A célfüggvény pedig a reward-okkal súlyozott logloss. Direkt módon a célfüggvény maximalizálása nem adja meg az optimális policy-t, de a gradiense mindig a megfelelő irányba mutat.

### Neurális háló

A megvalósításhoz pytorch-ot használtunk. A legjobb eredményeket produkáló háló az alább felsorol szélességű dense rétegekből és aktivációs függvényekből áll.
* Bemeneti: 81 
* H1: 256 + ReLU
* H2: 128 + ReLU
* H3: 32 + ReLU
* Kimenet: 9 + Softmax

Tehát három rejtett réteget tartalmaz a modellünk.

Az optimalizációs algoritmus: Adam 

### Jutalmak

A tanítás során több különböző jutalmazási rendszert alkalmaztunk, különböző együtthatókkal.
* Élelem, bekebelezés esetén: a méret növekedés értéke közvetlenül volt a reward.
* Halál esetén egy megfelelő méretű büntetés.
* Pozíció és mozgás alapú jutalmak:
    * Annak érdekében, hogy az ágens mozogjon, jutalmaztuk a mozgást. Ezzel jutalmazva azt is, hogy ha fal elött álva nem neki megy.
    * Annak érdekében, hogy az ágens ne csak oda-vissza lépkedjen két mező között vagy korlátozott területen belül, egy mozgóátlagos megoldással jutalmaztuk a haladást.
    * Bizonyos futtatások esetén jutalmaztuk, ha az ágens a térkép centruma felé halad. 

## Training

A modell a példatérképek közül a "04_mirror" térképen kezdett tanulni. A módszerünk az volt, hogy rövidebb játékokat játszattunk, ameddig "rá nem szokott" az evésre és közledésre. Ezután növeltük a tick számot, hogy komplexeb szituációkkal is megismerkedhessen az ágens. 

Az ágens az olyan térképeken teljesít jobban, amelyeken vannak akadályok.

### Reward discounting & normalization

Alkalmaztuk a reward discounting-ot, aminek segítségével összegezzük a reward-okat, ezáltal a megelőző akciók is jutalmazva vannak, egy exponenciálisan "lecsengő" súlyozással.

Továbbá a stabilabb tanulás érdekében, normalizáltuk a rewardokat.

### Továbbfejlesztett ágensek

Honteszka

### Napló
* Scenario 1
    * Háló: 4 rejtett réteg
    * 50 ticks: rátanult egy csak balra menésre -> az esetek többségében ez egész jó
* Scenario 3.
    * 50 ticks
    * reward ha mozog -> csak egy irányba megy
* Scenario 4.
    * 300 tick
    * Szintén csak egy irányba megy.
* Scenario 5.
    * 50 tick
    * kisebb háló
* Scenario 6.
    * kisebb háló: 
        * 81 - 256 - 128 - 32 - 9
    * kisebb learning rate: 1e-4
    * updated discounting
    * 50 tick 
    * 1000 játék -> nem tanult túl sok mindent
* Scenario 7.
    * Scenario 6 tovább edzése
    * kisebb háló: 
        * 81 - 256 - 128 - 32 - 9
    * kisebb learning rate: 1e-4
    * 50 ticks
    * 3500 játék után -> randomba tolta
* Scenario 8.
    * háló: 
        * 81 - 256 - 128 - 32 - 9
    * 50 ticks
    * learning_rate: 1e-3
    * 3000 játék után: nem teljesen egysíkú stratégia, nem teljesít túl rosszul és úgy tűnik, hogy egyértelmű döntést hoz
* Scenario 9.
    * model_8 további edzése
    * learning_rate: 1e-3
    * 100 ticks
    * háló: marad
    * 3000 játék után: nem teljesít túl rosszul, egyértlemű döntéseket hoz
* Scenario 10.
    * model_9 fejlesztése
    * 200 ticks
    * háló: marad
    * nincs reward, ha mozog
    * 3000 játék: -> ellustult
* Scenario 11.
    * model_9 fejlesztése
    * háló marad
    * van plusz reward, ha a pozíciók mozgóátlagából kivonva a kezdő pozíciót
        * move reward: 0.05
        * pos reward: 0.01
        * past_win: 10
        * kaja reward: kaja value
        * death reward: -99
    * vision update:
        * ha nem megehető kolléga van: -1
        * Ha megehető kolléga: érték
        * Ha nagy kolléga: -érték
    * 200 ticks
    * probléma: ha meghal akkor minden körben megkapja a negatív reward-ot -> nem is tanult jól
* Scenario 12.
    * mode_9 továbbedzése
    * háló marad
    * reward: marad
    * vision update: marad
    * 200 ticks
    * halál utáni tanulás fixed
    * 400 játék: -> 
    * Probléma: ha meghal akkor nem kerül be a -99
* Scenario 13.
    * model_12 tovább
    * háló marad
    * reward: 
        * move reward: 0.025
        * pos reward: 0.01
        * past_win: 10
        * kaja reward: kaja value
        * death reward: -99
    * vision update: marad
    * 200 ticks
    * halál nincs bűntetve: fixed! mégse
    * 500 játék -> sajnos a halálból nem tanult, de jól fejlődött a rewardok miatt
* Scenario 14.
    * model_13 tovább
    * háló marad
    * reward: marad
    * vision update: marad
    * 200 ticks
    * halál nincs bűntetve: fixed!
    * map: random choice from the three current maps: túltanulta a mirror map-et
* Scenario 15.
    * háló: 83- 256 - 256 - 128 - 32 - 9
    * reward: 
        * move reward: 0.01
        * pos reward: 0.005
        * past_win: 10
        * center_reward: 0.01
        * kaja reward: kaja value
        * death reward: -50
    * vision update: marad
    * 200 ticks
    * map: random choice from the three current maps
    * 800 játék után teljesen random akciók
* Scenraio 16.
    * mint scenario 15. csak nagyob learning rate -> rátanult a jobbrahaladásra
    * learning rate: 5e-3
* Scenraio 17.
    * learning rate: 5e-3
    * mint scenario 16, csak nagyobb move reward, és kisebb halál büntetése
    * rewards: 
        * move reward: 0.05
        * pos reward: 0.005
        * past_win: 10
        * center_reward: 0.01
        * kaja reward: 2*(kaja value)
        * death reward: -30
    * 1300 játék után: -> csak felfelé megy, teljesen egyértelmű döntés
* Scenario 18
    * learning rate: 1e-3
    * 50 ticks
    * rewards: 
        * move reward: 0.05
        * pos reward: 0.005
        * past_win: 10
        * center_reward: 0.01
        * kaja reward: 2*(kaja value)
        * death reward: -30
    * 1350 játék -> nem ügyes. inkább marad a sarokban gyakran
* Sceario 19
    * learning rate, model: marad
    * 50 ticks
    * rewards:
        * rewards: 
        * move reward: 0.05
        * pos reward: 0
        * past_win: 10
        * center_reward: 0.01
        * kaja reward: kaja value
        * death reward: -5
    * 2000 játék: elindul a center felé, de egy kicsit határozatlan
* Scenraio 21:
    * bemenetként megkapja a pozíciót is
    * rewards:
        * move reward: 0
        * pos reward: 0.1
        * past_win: 5
        * center_reward: 0.1 (if steps<10), 0.2 (if steps<5) 
        * kaja reward: kaja value
        * death reward: -5
    * pos_reward túl nagy. csak egy irányba megy
* Scenario 22:
    * bemenetként megkapja a pozíciót is
    * rewards:
        * move reward: 0.05
        * pos reward: 0.01
        * past_win: 5
        * center_reward: 0.1 (if steps<10), 0.2 (if steps<5) 
        * kaja reward: kaja value
        * death reward: -5
    * 50 tick
    * nagyon rátanult a haladás reward-ra
* Scenario 23:
    * bemenetként megkapja a pozíciót is
    * rewards:
        * move reward: 0.02
        * pos reward: 0.01
        * past_win: 5
        * center_reward: 0.1 (if steps<10), 0.2 (if steps<5) 
        * kaja reward: kaja value
        * death reward: -5
    * normalizálni a rewardot az egész batch-re
    * 50 tick
    * Csak keresztbe megy
* Scenario 24
    * Csak base_map
* Scenario 25
    * model_13 folytatása
    * rewards:
        * move reward: 0.02
        * pos reward: 0.01
        * past_win: 10
        * kaja reward: kaja value
        * death reward: -5
    * 200 ticks
    * batch_size 20
    * batch std norm
    * random maps
    * check rewards