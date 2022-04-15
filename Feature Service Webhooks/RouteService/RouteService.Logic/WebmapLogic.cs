using ArcGIS.Net.API;
using ArcGIS.Net.API.Content;
using ArcGIS.Net.API.Data.Content;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using RouteService.Logic.Constants;

namespace RouteService.Logic
{
	public class WebmapLogic
	{
		public static void CreateWebMap(IArcGISClient client, ILogger log, string user, string email, int objectid)
		{
            log.LogInformation("Getting template webmap");

            string? username = Environment.GetEnvironmentVariable(Settings.ArcGISUserName);
            if (username == null)
            {
                log.LogError("ArcGIS Username not configured.");
                return;
            }

            Item webmap = new Item(client, "681b48ff9cb74ba39a5b9f66b1a4bca7");
            ItemInfoResponse webmapInfo = webmap.Info();
            ItemDataResponse webmapData = webmap.Data();

            log.LogInformation("getting folder id");
            string folderid = webmapInfo.OwnerFolder;

            log.LogInformation($"Creating webmap for {user}");
            OperationalLayer? layer = webmapData.OperationalLayers.FirstOrDefault(item => item.ItemId == "bd2cc0a4d9eb49d3968608f84985a197");
            if (layer != null)
            {
                layer.LayerDefinition = new LayerDefinition()
                {
                    DefinitionExpression = $"ObjectID={objectid}"
                };

                webmapInfo.Title = $"Generated webmap for {user}";
                webmapInfo.Tags = new List<string>() { "EGT22", "REST", "AutomateYourPlatform", "Demo", $"{ user }"};
                webmapInfo.Description = $"Hoi {user}, je route naar huis.";
                webmapInfo.Text = JsonConvert.SerializeObject(webmapData);

				AddItemResponse? addResult = webmap.Add(username, webmapInfo, folderid);
                if (addResult != null && addResult.Success)
                {
                    log.LogInformation("Webmap created.");
                }
                else
                {
                    log.LogWarning("Failed to create the new webmap. ");
                }
            }
        }
	}
}
