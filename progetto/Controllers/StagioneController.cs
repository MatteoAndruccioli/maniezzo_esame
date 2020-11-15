using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using progetto.Models;


/*
  -nuovo controller
*/
namespace progetto.Controllers
{
  [ApiController]
  [Route("api/Stagione")] //il path da browser terminerà in "Stagione"
  public class StagioneController : ControllerBase
  {
    private readonly StagioneContext _context;
    public StagioneController(StagioneContext context)  
    { 
      //questo è il costruttore in cui istanzio il context con quello passato
      _context = context;
    }



    [HttpGet] //questo specifica che sarà una richiesta di tipo get, questa è select di tutte stagioni
    public ActionResult<List<Stagione>> GetAll() => _context.cronistoria.ToList();

    [HttpGet("{id}")] // GET by ID action, questa è la select di un elemento stagione con uno specifico id
    public async Task<ActionResult<Stagione>> GetStagione(int id)
    { var stagioneItem = await _context.cronistoria.FindAsync(id);
      if (stagioneItem == null)
      { return NotFound();
      }
      return stagioneItem;
    }

  // POST: api/Stagione/PostStagioneItem, permette di fare una insert di un item stagione
  [HttpPost]
  [Route("[action]")]
  public string PostStagioneItem([FromBody] Stagione item)
  { string res="Anno "+item.anno;
    try
    { _context.cronistoria.Add(item);
    _context.SaveChangesAsync();
    }
    catch(Exception ex)
    { Console.WriteLine("[ERROR] "+ex.Message);
    res = "Error";
    }
    Console.WriteLine(res);
    return res;
  }


  // PUT: api/Stagione/10
  [HttpPut("{id}")] //update di un elemento stagione nel db
  public async Task<IActionResult> PutStagione(int id,[FromBody] Stagione item)
  {
    if (id != item.id) return BadRequest();
    _context.Entry(item).State = EntityState.Modified;
    try
    { await _context.SaveChangesAsync();
    }
    catch (Exception ex)
    {
    if (!_context.cronistoria.Any(s => s.id == id))
    { return NotFound();
    }
    else
    { Console.WriteLine("[ERROR] "+ex.Message);;
    }
    }
    return Ok();
  }
    

  // DELETE: api/Stagione/10
  [HttpDelete("{id}")] //elimina un elemento stagione
  public async Task<ActionResult<Stagione>> DeleteTodoItem(int id)
  {
    var item = await _context.cronistoria.FindAsync(id);
    if (item == null)
    { return NotFound();
    }
    _context.cronistoria.Remove(item);
    await _context.SaveChangesAsync(); //sarebbe meglio metterlo in try catch come negli altri casi
    return item;
  }

  }
}