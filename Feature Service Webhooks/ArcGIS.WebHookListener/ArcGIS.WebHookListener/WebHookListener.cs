using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using ArcGIS.WebHookListener.Logic;
using Microsoft.WindowsAzure.Storage.Queue;
using ArcGIS.WebHookListener.Data;
using System.Collections.Generic;
using System.Linq;

namespace ArcGIS.WebHookListener
{
	public static class WebHookListener
	{
		[FunctionName("WebHookListener")]
		public static async Task<IActionResult> Run([HttpTrigger(AuthorizationLevel.Function, "get", "post", Route = null)] HttpRequest req, ILogger log)
		{
			// Startup logs and read the request.
			log.LogInformation("Start webhook function.");
			string requestBody = await req.ReadAsStringAsync();
			log.LogInformation($"Webhook body: {requestBody}");

			// Convert the request body to a .net object. 
			List<WebhookPayload> data = JsonConvert.DeserializeObject<List<WebhookPayload>>(requestBody);

			// Null and data checks. 
			if (data != null && data.Any())
			{
				// For every data element get the payload and read the servicename
				foreach (WebhookPayload payload in data)
				{
					if (!string.IsNullOrEmpty(payload.ServiceName))
					{
						// Get or create the queue based on the service name.
						CloudQueue queue = await QueueLogic.GetOrCreateQueue(log, payload.ServiceName);

						// Check if the queue is available.
						if (queue != null)
						{
							// Log message
							log.LogInformation("Queue find, set the notify item on the queue.");

							// Create a message and add it to the queue.
							CloudQueueMessage message = new CloudQueueMessage(requestBody);
							await queue.AddMessageAsync(message);

							// Log message
							log.LogInformation("NotifyItem set succesfully on the queue.");

							// Send item succes response
							return new OkObjectResult("Item in progress.");
						}
						else
						{
							// Write a log warning in case the script can't create the queue
							log.LogWarning($"Queue not found or unable to create the queue {payload.ServiceName}");
						}
					}
					else
					{
						// Write a log warning in case the script can't create the queue
						log.LogWarning($"Service name is empty, can't create a queue.");
					}
				}
			}
			else
			{
				// No data 
				return new EmptyResult();
			}

			// Function failed.
			return new BadRequestResult();
		}
	}
}
