using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Natt.Models
{
    public class AnimeModel
    {
        public string Title { get; set; }
        public string Link { get; set; }
        public string Thumbnail { get; set; }
        public string Description { get; set; }
        public List<News> Update { get; set; }
        public bool Whitelisted { get; set; }
    }

    public class News
    {
        public string Episode { get; set; }
        public string Season { get; set; }
    }
}
