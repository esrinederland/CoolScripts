using ArcGIS.WebHookListener.Constants;
using Microsoft.Extensions.Logging;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Queue;
using System;
using System.Threading.Tasks;

namespace ArcGIS.WebHookListener.Logic
{
	public static class QueueLogic
	{
		public static async Task<CloudQueue> GetOrCreateQueue(ILogger log, string queueName)
		{
			// Get the storage url.
			string azureStoragePath = Environment.GetEnvironmentVariable(Settings.AzureWebJobsStorage);

			// Get the storage account with the path.
			CloudStorageAccount storageAccount = CloudStorageAccount.Parse(azureStoragePath);

			// Create a queue client.
			CloudQueueClient queueClient = storageAccount.CreateCloudQueueClient();

			// Retrieve a reference to a queue.
			CloudQueue queue = queueClient.GetQueueReference(queueName.ToLower());

			// Create the queue if it does not exist.
			await queue.CreateIfNotExistsAsync();

			// Check if the queue is available.
			if (await queue.ExistsAsync())
			{
				return queue;
			}
			else
			{
				// Log message
				log.LogError("Queue not found or can't create a queue. Check the settings.");
				return null;
			}
		}
	}
}
