import Configuration

Config = Configuration.Configuration()

Config.load()

if Config.isConfigurationNeeded :
    print("Bitte öffnen Sie die Konfiguration, tragen die notwendigen Daten ein und speichern diese.")
    exit(1010)

print( "Ok, melden wir uns am Server "+ Config.db_server + " an..")


