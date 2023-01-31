# Chips and Circuits
Chips zijn overal te vinden zoals in je lapotop of telefoon die veel verschillende functies kunnen uitvoeren. Chips bestaan uit 'gates' en een lijst met verbindingen die de gates met elkaar verbinden (een zogenaamde netlist). Chips werken sneller en zijn goedkoper als de verbinding van de gates zo klein mogelijk is.\
\
In deze case is het de bedoeling om van de gegeven gates en netlist een optimale oplossing te vinden. Dit lijkt misschien makkelijk echter is het een zeer complex probleem. Met behulp van algoritmes en heuristieken proberen we de beste oplossingen te vinden voor de chips. 

## Vereisten

De gebruikte versie van Python voor deze codebase is Python 3.7. In het bestand requirements.txt staan benodigde libraries, met bijbehorende versies, die geïnstalleerd moeten worden. Dit is nodig om de code zonder problemen te laten draaien. Het installeren van de libraries kunnen via de volgende pip commando uitgevoerd worden.

```bash
Pip install -r requirements.txt
```
## Gebruik 

Je kan kiezen tussen onopgeloste voorbeelden van chips (0 tot 2) met verschillende netlist moeilijkheids graad (1 tot 3). 
Je kan de main functie aanroepen met:

```bash
python main.py
```
Voor gebruik van main.py kan je kiezen uit verschillende algoritmes. Dit verander je in config.py
##### config.py
```python
"""Welk algoritme wil je gebruiken?"""
Astar = True 
Hillclimber = True 
SimulatedAnnealing = True
Random = True

"""Wil je het visualiseren?"""
Visualize = True
experiment = True
iterations = 10

"""Voor welke chip en netlist wil je experimenteren?"""
chip_nr = 0 # loopt van 0 tot en met 2
netlist_nr = 2 # loopt van 1 tot en met 3
netlist_file = f"data/chip_{chip_nr}/netlist_{netlist_nr + 3 * chip_nr}.csv"
print_file = f"data/chip_{chip_nr}/print_{chip_nr}.csv"
Astar_netlist = netlist.Netlist(netlist_file, print_file)
```
## Structuur

Hier volgt een lijst met mappen en files met een beschrijving van de inhoud, en hoe je je kan navigeren:
- **/code**: map met alle code van dit project
    - **/code/algorithms**: map met algoritmes voor het project
    - **/code/classes**: map bevat classes gates en netlist
    - **/code/visualisation**: bevat functie voor 3d visualisatie van oplossing
- **/data**: bevat alle databestanden van elke chip die nodig zijn om oplossing te genereren en te visualiseren

## Testen

template aanroep van main.py

## aanpassingen

config.py / command line arguments

## Dankbetuiging
thx

## Auteurs

Hidde Brenninkmeijer\
Deniz Mermer\
Julius Knops