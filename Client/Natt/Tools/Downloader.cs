using Azure.Storage.Blobs;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using System.Windows;

namespace Natt.Tools
{
    public class Downloader
    {
        public static async Task Download(string url, string localPath)
        {
            HttpClient httpClient = new HttpClient();
            HttpResponseMessage response = await httpClient.GetAsync(url);

            MessageBox.Show($"Status: {response.StatusCode} Response: {response.Content}");
            response.EnsureSuccessStatusCode();
            using (var fileStream = File.OpenWrite(localPath))
            {
                await response.Content.CopyToAsync(fileStream);
            }
            response.Dispose();
            httpClient.Dispose();
        }
    }
}
