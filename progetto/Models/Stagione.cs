using System;
namespace progetto
{
  /* 
    è una classe che rappresenta le info contenute nel db:
    abbiamo un attributo per ogni colonna contenuta nel db 

    l'idea è lavorare sugli oggetti di questa classe per lavorare sul db
    noi non ci renderemo praticamente conto di lavorare su db

    questa è l'interfaccia lato codice, ci sarà l'interfaccia lato db (StagioneContext.cs)
  */
  public class Stagione
    {
      public int id { get; set; }
      public int anno { get; set; }
      public string serie { get; set; }
    }
}