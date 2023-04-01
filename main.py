from model import Configuration
from model import DirectoryScanner

# Auslesen der Kunfigurationsdatei
Config = Configuration.Configuration()
Config.load()

# Prüfen, ob Konfiguration geladen werden konnte/gefüllt ist
if Config.bol_is_configuration_needed :
    print("Bitte öffnen Sie die Konfiguration, tragen die notwendigen Daten ein und speichern diese.")
    exit(1010)

# Objekt vom Verzeichnis-Scanner erzeugen
dirScanner = DirectoryScanner.DirectoryScanner(Config)

# Scan starten
dirScanner.startScan()



