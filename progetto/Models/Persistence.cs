using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using progetto.Models;
using System.Text;
using System.IO;
namespace progetto
{
  public class Persistence
  {
    private readonly ElencoIndiciContext _context;
    public Persistence(ElencoIndiciContext context)
    { 
      _context = context;
    }
    /*
      questa funzione permette di estrarre i valori contenuti 
      in una colonna del db indici specificata attraverso indice 0-based

      errorString è una stringa di errore che viene restituita in caso query
      non vada a buon fine
    */
    public string GetColumnFromIndiciDB(int columnNumber, string errorString)
    { 
      //risultato di default che segnala un errore
      string result = errorString;
      //nomi delle colonne contenute nel db indici
      string[] colNames = new string[]{"id", "Data", "SP_500", "FTSE_MIB_", "GOLD_SPOT", "MSCI_EM", "MSCI_EURO", "All_Bonds", "US_Treasury"};

      if(0<=columnNumber && columnNumber<=8)
      {      
        string selectedCol = colNames[columnNumber]; //determino il nome della colonna
        List<string> serie = new List<string>(); //lista che conterrà la serie di dati
        serie.Add(selectedCol); //il primo elemento della lista sarà il nome della colonna

        using (var command = _context.Database.GetDbConnection().CreateCommand())
        {
          command.CommandText = $"SELECT {selectedCol} From indici";
          _context.Database.OpenConnection();
          using (var reader = command.ExecuteReader())
          {
            while(reader.Read())
            {
              serie.Add(reader[selectedCol].ToString());
            }
          }
        }
        //metto in result una stringa contenente su ogni riga un valore della colonna nel db
        result = string.Join("@", serie.ToArray()).Replace("@", System.Environment.NewLine);
        //stampo a video n° valori trovati (il primo elemento della lista è il nome della colonna)
        Console.WriteLine("trovati: " + (serie.Count()-1));  
        //memorizzo i dati raccolti in un csv nella cartella risultati su desktop
        StringListToCsv(serie, "risultati", selectedCol);
      }
      return result;
    }

    /*
      questa funzione genera un csv con il nome specificato 
      nella cartella con il nome indicato contenuta nel desktop;
      il file contiene una riga per ogni valore della lista
    */
    public void StringListToCsv(List<string> myList, string folderName, string fileName){
        //genero il path per la cartella indicata 
        string folderPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop) + "/" + folderName;
        //se la cartella non esiste la creo altrimenti non accade nulla
        System.IO.Directory.CreateDirectory(folderPath);
        //StreamWriter (string path, bool append)
        using (StreamWriter fout = new StreamWriter( folderPath+ "/" + fileName+".csv", false))
        {
            foreach(var arg in myList)
            {
              fout.WriteLine(arg);
            }
        }
    }
  }

}