using Natt.Bases;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ServiceModel.Syndication;
using System.Windows.Controls;
using System.Windows;
using System.Xml;
using System.Collections.ObjectModel;
using Natt.Models;
using System.Xml.Linq;
using System.Globalization;
using System.Windows.Data;
using System.IO;
using Azure.Storage.Blobs;

namespace Natt.ViewModels
{
    public class MainViewModel : BaseClass
    {
        private ObservableCollection<AnimeModel> _items;
        public ObservableCollection<AnimeModel> Items
        {
            get { return _items; }
            set { SetProperty(ref _items, value); }
        }

        private ObservableCollection<string> _whitelist;
        public ObservableCollection<string> Whitelist
        {
            get { return _whitelist; }
            set { SetProperty(ref _whitelist, value); }
        }

        private int _whitelistCount;
        public int WhitelistCount
        {
            get { return _whitelistCount; }
            set { SetProperty(ref _whitelistCount, value); }
        }

        public MainViewModel()
        {
            Items = new ObservableCollection<AnimeModel>();
            Whitelist = new ObservableCollection<string>();
            WhitelistCount = 0;

            InitWhitelist();

            LoadRSSFeed();
            Download();
        }

        private async Task Download()
        {
            await Tools.Downloader.Download(
                "blob:https://static.crunchyroll.com/3f89bff9-97bb-4327-bcf4-0767666edbb8",
                "out.mp4"
            );
        }

        private void InitWhitelist()
        {
            string path = "whitelist.txt";
            string[] buffer = null;

            if (File.Exists(path) == false)
            {
                File.Create(path).Close();
            } else
            {
                buffer = File.ReadAllLines(path);
                foreach (string line in buffer)
                {
                    Whitelist.Add(line);
                }
            }
        }

        private AnimeModel FindAnime(string name)
        {
            foreach (AnimeModel anime in Items)
            {
                if (anime.Title == name)
                    return (anime);
            }

            return (new AnimeModel());
        }

        private bool IsWhitelisted(string name)
        {
            foreach (string anime in Whitelist)
            {
                if (name.ToLower().Contains(anime.ToLower()) == true)
                    return (true);
            }

            return (false);
        }

        private void Format(SyndicationItem item)
        {
            XElement season = Extractor("season", item);
            string title = Extractor("seriesTitle", item).Value;
            AnimeModel anime = FindAnime(title);
            News news = new News();
            bool create = (anime.Title == null) ? true : false;

            anime.Title = title;
            anime.Whitelisted = IsWhitelisted(title);
            anime.Link = item.Id;
            anime.Thumbnail = Extractor("thumbnail", item).Attribute("url")?.Value;

            if (anime.Update == null)
            {
                anime.Update = new List<News>();
            }

            news.Episode = Extractor("episodeNumber", item).Value;

            if (season == null)
            {
                news.Season = "1";
            } else
            {
                news.Season = season.Value;
            }

            if (AlreadyAddedNews(anime.Update, news) == false)
                anime.Update.Add(news);

            if (create == true)
            {
                Items.Add(anime);
                if (anime.Whitelisted == true)
                    WhitelistCount += 1;

            }
        }

        private bool AlreadyAddedNews(List<News> update, News added)
        {
            foreach (News news in update)
            {
                if (news.Episode == added.Episode && news.Season == added.Season)
                    return (true);
            }

            return (false);
        }

        private XElement Extractor(string field, SyndicationItem item)
        {
            foreach (var extension in item.ElementExtensions)
            {
                if (extension.OuterName == field)
                {
                    return (extension.GetObject<XElement>());
                }
            }

            return (null);
        }

        private async void LoadRSSFeed()
        {
            string feedUrl = "http://feeds.feedburner.com/crunchyroll/rss/anime?lang=enUS";
            XmlReader reader = XmlReader.Create(feedUrl);
            SyndicationFeed feed = null;

            try
            {
                feed = await Task.Run(() => SyndicationFeed.Load(reader));

                foreach (SyndicationItem item in feed.Items)
                {
                    Format(item);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading RSS feed: " + ex.Message);
            }
        }
    }
}
