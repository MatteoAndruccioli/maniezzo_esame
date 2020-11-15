using Microsoft.EntityFrameworkCore;

namespace progetto.Models
{
  public class ElencoIndiciContext : DbContext
  {
    public ElencoIndiciContext(DbContextOptions<ElencoIndiciContext> options)
      : base(options)
    {
    }

    public DbSet<ElencoIndici> indici { get; set; }
  }
}