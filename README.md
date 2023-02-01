# Chips and Circuits
Chips zijn overal te vinden zoals in je lapotop of telefoon die veel verschillende functies kunnen uitvoeren. Chips bestaan uit 'gates' en een lijst met verbindingen die de gates met elkaar verbinden (een zogenaamde netlist). Chips werken sneller en zijn goedkoper als de verbinding van de gates zo klein mogelijk is.\
\
In deze case is het de bedoeling om van de gegeven gates en netlist een optimale oplossing te vinden. Dit lijkt misschien makkelijk echter is het een zeer complex probleem. Met behulp van algoritmes en heuristieken proberen we de beste oplossingen te vinden voor de chips. 
## Voorbeeld oplossing
![This is an image](/docs/Example_visualisation.png)
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
###
# Chip and netlist number to solve for
###
chip_nr: int = 0 # loopt van 0 tot en met 2
netlist_nr: int = 1 # loopt van 1 tot en met 3
netlist_file = None
print_file = None
Astar_netlist = None

"""
Choose which Heuristic / Algorithm you want to use to solve the problem
[Astar, Hillclimber, SimulatedAnnealing, Random]

Visualize is 3D plot .png-file of solution
experiment calls multiple solutions to calculate average, std dev
iterations is number of iterations used in experiment
"""

# A* parameters
Astar_full_implementation: bool = False 
Astar_sample_generate_count: int = 10
Astar_sample: int = 0

# Hillclimber parameters
Hillclimber: bool = False
hc_generate_count: int = 25
hc_iterations: int = 250

### More options in config.py available ###
```
## Random netlist en oplossingen
Je kunt in config.py kiezen om een willekeurige netlist te genereren.

Let op!: De naam van de file waar het resultaat in wordt opgeslagen is gelijk
aan de gebruikte chip nummer en netlist. Als je bijvoorbeeld chip nummer 0 en 
netlist 1 gebruikt, deze variable in config.py niet wijzigt en daarna main.py
draait met random_netlist True dan wordt de file waar de resultaten van chip
nummer 0 en netlist 1 in zijn overschreven.

Willekeurige netlisten waarbij de connecties dicht bij elkaar zijn, lijken
makkelijker oplosbaar. Waneer ze ver van elkaar zijn en er gates met connections
tussen zitten krijg je meer crossings en dus een slechter resultaat.
Willekeurige netlisten waar connection of gates er uiteindelijk voor zorgt dat 
een gate "ingeboxt" is zijn onoplosbaar.     

## Structuur

Hier volgt een lijst met mappen en files met een beschrijving van de inhoud, en hoe je je kan navigeren:
- **/code**: map met alle code van dit project
    - **/code/algorithms**: map met algoritmes voor het project
    - **/code/classes**: map bevat classes gates en netlist
    - **/code/visualisation**: bevat functie voor 3d visualisatie van oplossing
- **/data**: bevat alle databestanden van elke chip die nodig zijn om oplossing te genereren en te visualiseren

## Algoritmes
-   **Dijkstra algoritme**: Gebruikt de huidige kosten om het kortste en meest belovend pad te vinden. In deze case eigenlijk een breadth-first search omdat elke afstand tussen 2 punten van de grid een eenheid van 1 heeft.
-   **Astar**: Hetzelfde als dijkstra, maar de euclidean afstand van het huidige punt naar de eindbestemming wordt als heuristic gebruikt.
-   **Genetic**: algoritme dat nieuwe generaties van oplossingen genereerd doormiddel van kruisingen en mutaties. 
-   **Hillclimber**: Zoekt de beste oplossing door te kijken of een buur oplossing beter is. Zo ja, dan is dat de nieuwe oplossing en wordt dit een x keer herhaald.
-   **Random**: algoritme dat random pad kiest voor oplossing
-   **Simulated Annealing**: Identiek aan hillclimber, maar wordt de oplossing gekozen gebaseerd op een acceptatiekans.

## Auteurs

Hidde Brenninkmeijer\
Deniz Mermer\
Julius Knops