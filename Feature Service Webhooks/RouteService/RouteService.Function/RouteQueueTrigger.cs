using System;
using ArcGIS.Net.API;
using Microsoft.Azure.WebJobs;
using Microsoft.Extensions.Logging;
using RouteService.Logic;
using RouteService.Logic.Constants;

namespace RouteService.Function
{
    public class RouteQueueTrigger
    {
        /// <summary>
        /// Listen to webhook messages from a Azure Storage Queue
        /// </summary>
        /// <param name="webhookPayload"></param>
        /// <param name="log"></param>
        [FunctionName("RouteQueueTrigger")]
        public void Run([QueueTrigger("locatiesegt22", Connection = "AzureWebHookStorage")] string webhookPayload, ILogger log)
        {
            log.LogInformation($"Start creating a route with: {webhookPayload}");

            // Get ArcGIS username and password from settings
            string username = Environment.GetEnvironmentVariable(Settings.ArcGISUserName);
            string password = Environment.GetEnvironmentVariable(Settings.ArcGISPassword);

            // Create a ArcGIS .NET Client
            IArcGISClient client = new ArcGISPortal(username, password);

            // Create a routelogic class and create and save a route in ArcGIS.
            RouteLogic logic = new RouteLogic();
            logic.CreateRoute(log, client, webhookPayload);

            log.LogInformation($"Route created succesful.");
        }
    }
}
