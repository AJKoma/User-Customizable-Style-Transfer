using System;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;
using System.Linq;
using api.Models;
using System.Web.Http;
using Microsoft.EntityFrameworkCore;
using System.Web;
using Microsoft.AspNetCore.Cors;
using RouteAttribute = Microsoft.AspNetCore.Mvc.RouteAttribute;
using HttpGetAttribute = Microsoft.AspNetCore.Mvc.HttpGetAttribute;




namespace api.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [EnableCors("AllowSpecificOrigin")]
    public class StyleController : ControllerBase 
    {
        Styles[] info = new Styles[]{
            new Styles { ID = 1, Artist="Fujishima-Takeji", Filepath="img/fujishima-takeji-sunrise-over-the-eastern-sea.jpg", Style = "sunrise-over-the-eastern-sea" },
            new Styles { ID = 2, Artist="Georges-Barque", Filepath="img/georges-barque-bottle-and-fishes.jpg", Style = "bottle-and-fishes" },
            new Styles { ID = 3, Artist="Georges-Barque", Filepath="img/georges-barque-glass-on-a-table.jpg", Style = "glass-on-a-table" },
            new Styles { ID = 4, Artist="Katsushika-Hokusai", Filepath="img/katsushika-hokusai-fuji-mountains-in-clear-weather.jpg", Style = "fuji-mountains-in-clear-weather" },
            new Styles { ID = 5, Artist="Katsushika-Hokusai", Filepath="img/katsushika-hokusai-the-wave.jpg", Style = "the-wave" },
            new Styles { ID = 6, Artist="Claude-Monet", Filepath="img/monet-sunset-in-venice.jpg", Style = "sunset-in-venice" },
            new Styles { ID = 7, Artist="Claude-Monet", Filepath="img/monet-the-poppy-field.jpg", Style = "the-poppy-field" },
            new Styles { ID = 8, Artist="Pablo-Picasso", Filepath="img/picasso-blue-nude.jpg", Style = "blue-nude" },
            new Styles { ID = 9, Artist="Pablo-Picasso", Filepath="img/picasso-crucifixion.jpg", Style = "crucifixion" },
            new Styles { ID = 10, Artist="Pablo-Picasso", Filepath="img/picasso-guernica.jpg", Style = "guernica" },
            new Styles { ID = 11, Artist="Takashi-Murakami", Filepath="img/takashi-murakami-lineage-of-eccentrics.jpg", Style = "lineage-of-eccentric" },
            new Styles { ID = 12, Artist="Takashi-Murakami", Filepath="img/takashi-murakami-727.jpg", Style = "727" },
            new Styles { ID = 13, Artist="Van-Gogh", Filepath="img/vangogh-starry-night.jpg", Style = "starry-night" },
            new Styles { ID = 14, Artist="Van-Gogh", Filepath="img/vangogh-the-starry-night-over-the-rhone.jpg", Style = "the-starry-night-over-the-rhone" },
            new Styles { ID = 15, Artist="Van-Gogh", Filepath="img/vangogh-tree-roots.jpg", Style = "tree-roots" },

        };



        [HttpGet]
        [EnableCors("AllowSpecificOrigin")]
        public IEnumerable<Styles> Get()
        {
            return info;
        }

        [HttpGet]
        [EnableCors("AllowSpecificOrigin")]
        [Route("{id}/pic")]
        // [HttpGet("{id}", Name ="get style")]
        public IActionResult Get(int id)
        {
            var s = info.FirstOrDefault((p) => p.ID == id);
            var file_path = s.Filepath;
           // var file_path = "/Users/ajkoma/Documents/GitHub/Web-Application-Development/User Customizable Style Transfer /Web Api/api/api" + s.Filepath;
            Byte[] b = System.IO.File.ReadAllBytes(file_path);   // You can use your own method over here.         
            return File(b, "image/jpg");


        }

        [HttpGet]
        [EnableCors("AllowSpecificOrigin")]
        [Route("{id}/info")]
        public IActionResult Get(long id)
        {
            var s = info.FirstOrDefault((p) => p.ID == id);
            return Ok(s);
        }


    }
}

   





