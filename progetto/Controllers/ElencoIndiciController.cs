using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using progetto.Models;
using System.Text;
using System.IO;

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
    public String GetSerie(int idSerie)
    {
      //risultato di default, restituito in caso di errore
      string result = ("idSerie non valido!@specificare un idSerie valido, ovvero appartenente all'intervallo [0,8]@" +
      "0=>id;@1=>Data;@2=>SP_500;@3=>FTSE_MIB_;@4=>GOLD_SPOT;@5=>MSCI_EM;@6=>MSCI_EURO;@7=>All_Bonds;@8=>US_Treasury").Replace("@", System.Environment.NewLine);
      //mi faccio restituire questa stringa in caso di errore; NON deve essere un possibile risultato della query
      string errorString = "-1_columnNumber_error";
      string queryResult = P.GetColumnFromIndiciDB(idSerie, errorString);
      if (queryResult != errorString){
        result = queryResult;
      }
      return result;
    } 
  }
}