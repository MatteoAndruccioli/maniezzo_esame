using Microsoft.EntityFrameworkCore;
namespace progetto.Models
{
  /*
    - sta classe è l'interfaccia lato DB,  
    - corrisponde a Stagione.cs che è l'interfaccia lato codice
  */
  public class StagioneContext : DbContext
  {
    public StagioneContext(DbContextOptions<StagioneContext> options)
      : base(options)
    {
    }

    /*
      - questo determina il mapping tra questa classe e la classe Stagione.cs
      - quindi qua diciamo che alla classe Stagione.cs corrisponde cronistoria nel db
    */
    public DbSet<Stagione> cronistoria { get; set; }
  }
}