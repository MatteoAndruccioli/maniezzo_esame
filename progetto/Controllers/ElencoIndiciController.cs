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
      string result = ("idSerie non valido!@specificare un idSerie valido, ovvero appartenente all'intervallo [0,8]@" +
      "0=>id;@1=>Data;@2=>SP_500;@3=>FTSE_MIB_;@4=>GOLD_SPOT;@5=>MSCI_EM;@6=>MSCI_EURO;@7=>All_Bonds;@8=>US_Treasury");//.Replace("@", System.Environment.NewLine);
      
      try //int.Parse(idSerie) tira errori in caso idSerie non sia un numero
      {
        //mi faccio restituire questa stringa in caso di errore; NON deve essere un possibile risultato della query
        string errorString = "-1_columnNumber_error";
        string queryResult = P.GetColumnFromIndiciDB(int.Parse(idSerie), errorString);
        if (queryResult != errorString){
          result = queryResult;
        }
      } catch {
        Console.WriteLine("!!! probabilmente idSerie non è un numero. idSerie= " + idSerie);
      }
      return result;
    } 
  }
}