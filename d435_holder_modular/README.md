# D435 houder in drie delen

Print eenmaal base.stl, left_panel.stl en right_panel.stl. Alle STL's staan met hun vlakke onderzijde op Z=0. De panelen liggen met hun markeruitsparing omhoog. De voet staat met de twee open sleuven omhoog. De camera staat aan de voorzijde (negatieve Y in de assembly).

## Verbinding

Schuif de 20 mm lange tong van ieder paneel van bovenaf in de bijbehorende sleuf, tot de onderkant de vloer raakt. De panelen staan op +/-30 graden ten opzichte van de lensrichting. Links en rechts zijn gespiegeld, de tong zit bij de binnenrand.

Dit ontwerp gebruikt een schuifpassing met 0.2 mm nominale speling per zijde. Er is geen verende klikhaak. De eerste print bepaalt of de passing strak genoeg is. Voor een permanente, stijve meetopstelling kunnen de tongen na een proefpassing met kunststofgeschikte lijm worden vastgezet. Kalibreer pas na definitieve montage. Demontage en terugplaatsen vereisen controle van de tagpositie. Vermijd gebruik van een merkbaar wiebelende passing voor posemeting.

## Printen

Start met 0.2 mm lagen, vier wanden, 25% infill. Panelen vlak en voet rechtop. Grote overhangende vlakken zijn verwijderd. De horizontale schroeftunnels in de voet hebben maximaal 6.4 mm overspanning en moeten door de slicer als korte bruggen worden behandeld. Controleer deze lagen in de slicer. Supportvrij printen is een ontwerpdoel, geen gemeten printresultaat.

## Tags en schroeven

Tags zijn 60 x 60 x 1 mm, uitsparingen 60.4 x 60.4 x 1.1 mm. Gebruik een dunne lijmlaag. De zwarte markermaat is volgens opgave 50 mm. Twee M3-gaten op 45 mm hartafstand. De diepe toegangsgaten achteraan zijn voor schroefkop en gereedschap; bij de camera blijft 4 mm materiaal over. M3 x 6 mm zonder ring geeft nominaal 2 mm indringing. Controleer daadwerkelijk maximaal 3 mm indringing in de camera. Monteer de voet vóór het inschuiven van de panelen.

## Controle

Drie geldige, verbonden solids. Drie gesloten STL-meshes met consistente winding. Nul volumetrische interferentie tussen panelen en voet bij eindpositie. Onderste aanslag Z=14 mm en paneelonderrand Z=34 mm. Geometrische passing gecontroleerd, fysieke passing, printbaarheid en stijfheid nog niet getest. De montagepositie en lensoffset moeten worden gekalibreerd.

De assembly is bedoeld voor inspectie. Print de drie losse STL-bestanden.

## Tag-ID’s in deze repository

Gebruik de D435-tags 4 en 5 uit `../d435_tags_id4_id5/`. Tags 0 en 1 zijn voor de robotvoet. De uitsparing is ontworpen voor een 1 mm plaatje. De repository-tags hebben een witte basis van 1 mm met een zwart patroon van 0.2 mm erboven. De zwarte bovenzijde steekt daardoor circa 0.1 mm boven de 1.1 mm uitsparing uit, plus de lijmlaag. Neem de uiteindelijke tagdikte en lijmlaag mee in de optische kalibratie.
