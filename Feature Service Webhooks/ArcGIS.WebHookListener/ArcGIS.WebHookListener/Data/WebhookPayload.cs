using Newtonsoft.Json;
using System.Collections.Generic;

namespace ArcGIS.WebHookListener.Data
{
	class WebhookPayload
	{
        [JsonProperty("layerId")]
        public int LayerId { get; set; }

        [JsonProperty("serviceName")]
        public string ServiceName { get; set; }

        [JsonProperty("changeType")]
        public string ChangeType { get; set; }

        [JsonProperty("orgId")]
        public string OrgId { get; set; }

        [JsonProperty("changesUrl")]
        public string ChangesUrl { get; set; }

        [JsonProperty("events")]
        public List<string> Events { get; set; }
    }
}