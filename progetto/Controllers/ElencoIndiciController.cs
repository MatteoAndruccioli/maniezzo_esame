using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using progetto.Models;

namespace progetto.Controllers
{
  [ApiController]
  [Route("api/ElencoIndici")]
  public class ElencoIndiciController : ControllerBase
  {
    private readonly ElencoIndiciContext _context;
    Persistence P;
    public ElencoIndiciController(ElencoIndiciContext context)
    { 
      _context = context;
      P = new Persistence(context);
    }

    [HttpGet] //ottenere tutti gli indici
    public ActionResult<List<ElencoIndici>> GetAll() => _context.indici.ToList();

    [HttpGet("{idSerie}", Name = "GetSerie")] // GET by ID action
    public String GetSerie(string idSerie)
    {
      //risultato di default, restituito in caso di errore
      string result = ("idSerie non valido!@specificare un idSerie valido, ovvero appartenente all'intervallo [0,6]@" +
      "@0=>SP_500;@1=>FTSE_MIB_;@2=>GOLD_SPOT;@3=>MSCI_EM;@4=>MSCI_EURO;@5=>All_Bonds;@6=>US_Treasury");//.Replace("@", System.Environment.NewLine);
      
      //nomi delle colonne contenute nel db indici
      string[] colNames = new string[]{"SP_500", "FTSE_MIB_", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO", "All_Bonds", "US_Treasury"};

      try //int.Parse(idSerie) tira errori in caso idSerie non sia un numero
      {
        //mi faccio restituire questa stringa in caso di errore; NON deve essere un possibile risultato della query
        string errorString = "-1_columnNumber_error";
        int columnNumber = int.Parse(idSerie); 
        if(0<=columnNumber && columnNumber<=6)
        { 
          string selectedCol = colNames[columnNumber]; //contiene il nome dell'indice i cui valori dovranno esser restituiti
          string queryResult = P.GetColumnFromIndiciDB(selectedCol, errorString);
          if (queryResult != errorString){
            //la query su db dovrebbe aver funzionato => dovrei aver creato csv correttamente
            result = "{";
            Forecast forecast = new Forecast();
            result += forecast.forecastSARIMAindex(selectedCol);
            result += "}";
          } else {
            //qualcosa è andato storto nell'interrogazione sqlite per la creazione del file csv
          }
        } else {
          //il numero indicato non è comprenso nell'intervallo corretto
        }
      } catch {
        Console.WriteLine("!!! probabilmente idSerie non è un numero. idSerie= " + idSerie);
      }
      return result;
      // guarda lezione giorno 20/11/2020
    } 
  }
}