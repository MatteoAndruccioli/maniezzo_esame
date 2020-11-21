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

## Info sull'implementazione
- Dentro Models, **PythonRunner.cs** usa **System.Drawing** per poter avere la classe Bitmap
questa libreria necessita di essere importata lanciando il seguente comando:
`dotnet add package System.Drawing.Common` 
- Di base quando Python legge numeri decimali vuole come delimitatore il . (punto) e non la virgola; quindi i file csv che noi andiamo a scrivere in risposta alle get devono esser scritti secondo la cultura inglese: con . come delimitatore tra parte intera e decimale, e non all'italiana (ovvero con una ,). Di default dotnet core stabilisce la cultura con cui runnare il programma sulla base del pc che runna l'applicazione, siccome il mio è in italiano metterebbe come delimitatore le virgole. Per fare override delle info di cultura: nel file **Startup.cs**, nel metodo pubblico **Configure** aggiungo le seguenti righe di codice:
```csharp
  var cultureInfo = new CultureInfo("en-US");
  cultureInfo.NumberFormat.CurrencySymbol = "€";

  CultureInfo.DefaultThreadCurrentCulture = cultureInfo;
  CultureInfo.DefaultThreadCurrentUICulture = cultureInfo;
``` 