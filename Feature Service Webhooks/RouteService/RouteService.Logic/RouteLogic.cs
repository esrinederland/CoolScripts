using ArcGIS.Net.API;
using ArcGIS.Net.API.Data;
using ArcGIS.Net.API.Data.FeatureLayer;
using ArcGIS.Net.API.Data.FeatureService;
using ArcGIS.Net.API.Data.Routing;
using ArcGIS.Net.API.Geometry;
using ArcGIS.Net.API.Routing;
using Microsoft.Extensions.Logging;
using RouteService.Logic.Constants;
using RouteService.Logic.Data;
using System;
using System.Text.RegularExpressions;

namespace RouteService.Logic
{
	public class RouteLogic
	{
		// Location of the postillion den haag
		private readonly Point StartLocation = new() { X = 4.323803070468983, Y = 52.069516329432126 };

		/// <summary>
		/// Create and store a route in ArcGIS.
		/// </summary>
		/// <param name="log"></param>
		/// <param name="client"></param>
		/// <param name="webhookPayload"></param>
		public void CreateRoute(ILogger log, IArcGISClient client, string webhookPayload)
		{
			// Get route featurelayer setting.
			string? routeFeatureLayerSetting = Environment.GetEnvironmentVariable(Settings.RouteFeatureLayerUrl);
			if (routeFeatureLayerSetting == null)
			{
				log.LogError($"{Settings.RouteFeatureLayerUrl} setting not found.");
				return;
			}

			// Convert the webhook payload.
			WebhookPayload payload = WebhookPayload.Create(webhookPayload);
			log.LogInformation("Payload converted.");

			if (payload == null)
			{
				log.LogWarning("Paylaod is empty, can't get the changes.");
				return;
			}

			if (payload.ChangesUrl == null)
			{
				log.LogWarning("Payload url is empty, can't get the changes.");
				return;
			}

			// Get the featureservice url based on the webhook payload.
			Match match = Regex.Match(payload.ChangesUrl, @"(.*)(\/FeatureServer\/)(.*)");
			log.LogInformation("Match featureserice url");
			
			string featureServiceUrl = match.Groups[1].ToString();
			log.LogInformation($"Featureservice url {featureServiceUrl} found.");

			// Create a ArcGIS .NET FeatureService
			RestFeatureService locatieService = new RestFeatureService(client, new Uri(featureServiceUrl));
			log.LogInformation("Featureservice created.");

			// Get the changes from the ArcGIS FeatureService with the webhook.
			ChangesResponse changes = locatieService.GetChanges(new Uri(payload.ChangesUrl));

			// Create a new list with route features.
			List<Feature> routeFeatures = new List<Feature>();

			// Store all routes and emails in memory to send a email. 
			Dictionary<Guid, string> emailEnabledroutes = new Dictionary<Guid, string>();

			// For every change/edit, get the given end location and create a route from the postillion den haag to the endpoint. 
			if (changes != null)
			{
				foreach (Edit edit in changes.Edits)
				{
					foreach (Feature feature in edit.Features.Adds)
					{
						if (feature.Geometry is Point endPoint)
						{
							// Create the route. 
							SolveResponse route = Route.Solve(client, new List<Point>() { StartLocation, endPoint});
							if (route == null || route.Routes == null)
							{
								log.LogWarning($"No routes found to point x:{endPoint.X} y:{endPoint.Y}");
								return;
							}
							
							// Get the line feature from the route and store i as a new route feature. 
							foreach (Feature routeFeature in route.Routes.Features)
							{
								Feature personalRouteFeature = new Feature()
								{
									Geometry = routeFeature.Geometry,
									Attributes = new Dictionary<string, object>()
								};

								// Copy the data. 
								if (feature.Attributes.ContainsKey("Opmerking"))
								{
									personalRouteFeature.Attributes.Add("Opmerking", feature.Attributes["Opmerking"]);
								}
								if (feature.Attributes.ContainsKey("Naam"))
								{
									personalRouteFeature.Attributes.Add("Naam", feature.Attributes["Naam"]);
								}

								Guid routeGuid = Guid.NewGuid();
								if (feature.Attributes.ContainsKey("Email"))
								{
									if (feature.Attributes["Email"] != null)
									{
										string? email = feature.Attributes["Email"].ToString();
										if (!string.IsNullOrWhiteSpace(email))
										{
											emailEnabledroutes.Add(routeGuid, email);
										}
									}
								}
								personalRouteFeature.Attributes.Add("RouteId", $"{{{routeGuid}}}");
								routeFeatures.Add(personalRouteFeature);
							}
						}
						else
						{
							log.LogWarning($"Feature not a point.");
						}
					}
				}
			}

			// Store all the new create route features to the route featurelayer. 
			RestFeatureLayer routeFeatureLayer = new RestFeatureLayer(client, new Uri(routeFeatureLayerSetting));
			AddResultResponse result = routeFeatureLayer.AddFeatures(routeFeatures);
			if(result.IsSucces)
			{
				log.LogInformation("Route features added.");
				if (result.AddResults == null)
				{
					log.LogWarning("No add's returned.");
					return;
				}

				foreach (AddResult item in result.AddResults)
				{
					RestQueryParameters queryParameters = new RestQueryParameters()
					{
						Where = $"ObjectId = {item.ObjectId}",
						OutFields = "*"
					};

					FeaturesResponse routeQueryResponse = routeFeatureLayer.Query(queryParameters);
					Feature? routeFeature = routeQueryResponse?.Features?.FirstOrDefault();
					if (routeFeature == null)
					{
						log.LogWarning($"Can't find the route feature with {item.ObjectId}.");
						return;
					}

					if (routeFeature.Attributes.ContainsKey("RouteId"))
					{
						string? routeGuidString = routeFeature.Attributes["RouteId"]?.ToString();
						if (routeGuidString != null)
						{
							Guid routeGuid = Guid.Parse(routeGuidString);
							string name = string.Empty;

							if (routeFeature.Attributes.ContainsKey("Naam"))
							{
								name = routeFeature.Attributes["Naam"]?.ToString();
							}

							if (emailEnabledroutes.ContainsKey(routeGuid))
							{
								string email = emailEnabledroutes[routeGuid];

								SendEmail(log, email, name, item.ObjectId);
							}
						}
					}
				}
			}
			else
			{
				log.LogInformation("Failed to save the route features.");
			}
		}

		private static void SendEmail(ILogger log, string email, string name, int objectId)
		{
			log.LogInformation("Start sending a email.");
			MailMessage message = new MailMessage()
			{
				SaveToSentItems = "false",
				Message = new Message()
				{
					Subject = "Automate you platform",
					Body = new Body()
					{
						ContentType = "HTML",
						Content = $"<p>Hoi {name}</p><p>Leuk dat je een route hebt gemaakt op de Automate Your Platform sessie</p><p> Je kan je eigen route terug vinden op:<br/>" +
						$" webmapurl{objectId} </p>"
					},
					ToRecipients = new List<Recipient>() { new Recipient() { EmailAddress = new EmailAddress() { Address = email } } },
					BccRecipients = new List<Recipient>() { new Recipient() { EmailAddress = new EmailAddress() { Address = "developers@esri.nl" } } },
				}
			};

			MailLogic mailLogic = new MailLogic();
			if (mailLogic.SendMail(log, message))
			{
				log.LogInformation("Succesfull send a email.");
			}
			else
			{
				log.LogWarning("Failed to send a email.");
			}
		}
	}
}