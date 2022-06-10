using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace RouteService.Logic.Data
{
    public class Body
    {
        [JsonProperty("contentType")]
        public string ContentType { get; set; }

        [JsonProperty("content")]
        public string Content { get; set; }
    }

    public class EmailAddress
    {
        [JsonProperty("address")]
        public string Address { get; set; }
    }

    public class Recipient
    {
        [JsonProperty("emailAddress", NullValueHandling = NullValueHandling.Ignore)]
        public EmailAddress EmailAddress { get; set; }
    }

    public class Message
    {
        [JsonProperty("subject")]
        public string Subject { get; set; }

        [JsonProperty("body")]
        public Body Body { get; set; }

        [JsonProperty("toRecipients", NullValueHandling = NullValueHandling.Ignore)]
        public List<Recipient> ToRecipients { get; set; }

        [JsonProperty("ccRecipients", NullValueHandling = NullValueHandling.Ignore)]
        public List<Recipient> CcRecipients { get; set; }

        [JsonProperty("bccRecipients", NullValueHandling = NullValueHandling.Ignore)]
        public List<Recipient> BccRecipients { get; set; }
    }

    public class MailMessage
    {
        [JsonProperty("message")]
        public Message Message { get; set; }

        [JsonProperty("saveToSentItems")]
        public string SaveToSentItems { get; set; } = "false";
    }
}