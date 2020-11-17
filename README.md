# maniezzo_esame

### Buildare il progetto su vsCode:
ctrl+shift+b > click su build 

### Avvio server (progetto):
- spostati nella cartella progetto con un terminale
- lancia comando: `dotnet run` 

## Consentire comunicazione con il server
- la prima volta avvia chrome e vai a https://localhost:5001/api/ElencoIndici
- ti darà un errore legato al certificato tu clicka su avanzate e dì di continuare, da quel momento potrai interrogare il server

# Server
## Directories:

- apri browser al link http://localhost:5000/api/ElencoIndici: otterrai l'elenco di tutti gli indici
- apri browser al link http://localhost:5000/api/ElencoIndici/idSerie: sostituisci nel link "idSerie" con un numero compreso tra 0 e 8, otterrai un elenco di indici relativo alla colonna corrispondente nella tabella indici di finindex.sqlite

