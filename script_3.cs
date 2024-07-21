using Newtonsoft.Json.Linq;

namespace ConsoleApp1
{
    class TopSellersRF
    {
        static async Task Main(string[] args)
        {
            string steamTopSellersUrl = "https://store.steampowered.com/api/featuredcategories/?cc=RU";

            using (HttpClient client = new HttpClient())
            {
                try
                {
                    HttpResponseMessage response = await client.GetAsync(steamTopSellersUrl);
                    response.EnsureSuccessStatusCode();
                    string responseBody = await response.Content.ReadAsStringAsync();

                    JObject json = JObject.Parse(responseBody);

                    var topSellers = json["top_sellers"]?["items"];
                    if (topSellers != null)
                    {
                        for (int i = 0; i < Math.Min(topSellers.Count(), 10); i++)
                        {
                            var item = topSellers[i];
                            string name = item["name"]?.ToString() ?? "N/A";
                            string finalPrice = item["final_price"]?.ToString() ?? "N/A";
                            string currency = item["currency"]?.ToString() ?? "N/A";
                            string price = finalPrice != "N/A" && currency != "N/A" ? $"{finalPrice} {currency}" : "N/A";
                            Console.WriteLine($"{i + 1}. {name} - {price}");
                        }
                    }
                    else
                    {
                        Console.WriteLine("Could not find top sellers");
                    }
                }
                catch (HttpRequestException e)
                {
                    Console.WriteLine($"Request error: {e.Message}");
                }
                catch (Exception e)
                {
                    Console.WriteLine($"Error: {e.Message}");
                }
            }
        }
    }
}
