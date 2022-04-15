using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using RouteService.Logic.Constants;
using RouteService.Logic.Data;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http.Headers;
using System.Text;
using System.Threading.Tasks;

namespace RouteService.Logic
{
	public class MailLogic
	{
        /// <summary>
        /// Send a mail with the Microsoft Graph Api and use a token from the settings.
        /// </summary>
        /// <param name="log"></param>
        /// <param name="message"></param>
        /// <returns></returns>
		public bool SendMail(ILogger log, MailMessage message)
        {
            // Get a token from the settings.
            string token = GetAccessToken(log);
            if (!string.IsNullOrWhiteSpace(token))
            {
                // Send mail. 
                return SendMail(log, token, message);
            }
            else
            {
                log.LogError("Failed to request a token from Microsoft Graph using settings.");
                return false;
            }
        }

        /// <summary>
        /// Send a mail with the Microsoft Graph Api.
        /// </summary>
        /// <param name="log"></param>
        /// <param name="token"></param>
        /// <param name="message"></param>
        /// <returns></returns>
        private bool SendMail(ILogger log, string token, MailMessage message)
        {
            try
            {
                log.LogInformation($"Start sending email using graph.");

                string fromMailUser = Environment.GetEnvironmentVariable(Settings.TeamsFromMailUser);
                if (string.IsNullOrWhiteSpace(fromMailUser))
                {
                    log.LogError("Mail from user not configured, please check configuration.");
                    return false;
                }

                // Create the HTTP Client and Authentication
                string url = $"https://graph.microsoft.com/v1.0/users/{fromMailUser}/sendMail";
                HttpClient client = new HttpClient();
                HttpRequestMessage request = new HttpRequestMessage(HttpMethod.Post, url);
                client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

                // Create the mail request.
                string stringmessage = JsonConvert.SerializeObject(message);
                request.Content = new StringContent(stringmessage, Encoding.UTF8, "application/json");

                log.LogInformation($"Sending message {stringmessage} to graph {url}.");
                // Send the mail message to the API. 
                HttpResponseMessage response = client.SendAsync(request).Result;
                if (response != null && response.IsSuccessStatusCode)
                {
                    log.LogInformation($"Successful sended email using graph.");
                    return response.StatusCode == System.Net.HttpStatusCode.Accepted;
                }
                else
                {
                    log.LogError($"Error sending mail to {url} with error {response.ReasonPhrase}");
                }
            }
            catch (Exception ex)
            {
                log.LogError($"Error sending data to office365 with {ex.Message}", ex);
            }
            return false;
        }

        /// <summary>
        /// Get an access token from Azure AD. 
        /// </summary>
        /// <param name="log"></param>
        /// <returns></returns>
        public static string GetAccessToken(ILogger log)
        {
            //Documentation: https://docs.microsoft.com/en-us/graph/auth-v2-service
            log.LogInformation($"GetAccessToken started");

            string clientid = Environment.GetEnvironmentVariable(Settings.TeamsClientID);
            string clientsecret = Environment.GetEnvironmentVariable(Settings.TeamsClientSecret);
            string tenant = Environment.GetEnvironmentVariable(Settings.TeamsTenant);
            log.LogInformation($"Environment: {clientid} {clientsecret} {tenant}");
            //Create form-data
            List<KeyValuePair<string, string>> kvp = new List<KeyValuePair<string, string>>
            {
                new KeyValuePair<string, string>("grant_type", "client_credentials"),
                new KeyValuePair<string, string>("client_id", clientid),
                new KeyValuePair<string, string>("scope", "https://graph.microsoft.com/.default"),
                new KeyValuePair<string, string>("client_secret", clientsecret)
            };
            var formContent = new FormUrlEncodedContent(kvp);

            //send request for token
            var myHttpClient = new HttpClient();
            var url = string.Format("https://login.microsoftonline.com/{0}/oauth2/v2.0/token", tenant);
            var response = myHttpClient.PostAsync(url, formContent).Result;
            if (response != null && response.IsSuccessStatusCode)
            {
                string ret = response.Content.ReadAsStringAsync().Result;
                AccessToken accesstoken = JsonConvert.DeserializeObject<AccessToken>(ret);
                log.LogInformation($"Token retrieved successfully");
                return accesstoken.access_token;
            }
            else
            {
                log.LogError($"Error retrieving token: {response.ReasonPhrase}");
                return "";
            }
        }
    }
}
