using System;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;

using System.Web.Http;
using api.Models;




namespace api.Models
{

    public class StylesContext : DbContext
    {
            public StylesContext(DbContextOptions<StylesContext> options)
            : base(options)
            {
            }

        public DbSet<Styles> StylesItems { get; set; }
    
    }
}
