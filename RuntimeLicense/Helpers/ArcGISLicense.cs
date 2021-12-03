using Esri.ArcGISRuntime;
using Esri.ArcGISRuntime.Portal;
using Esri.ArcGISRuntime.Security;
using System;
using System.IO;
using System.Threading.Tasks;

namespace RuntimeLicense.Helpers
{
	public class ArcGISLicense
	{
        private const string LicenseFileName = "myapplicense.json";

        public static async Task GetLicense(string portalUrl)
        {
            try
            {
                // Try to load an existing license file on disk.
                if (File.Exists(LicenseFileName))
                {
                    // Read the existing license file from disk. 
                    string licenseJson = File.ReadAllText(LicenseFileName);
                    
                    // Create a license info from the json and load within the Runtime.
                    ArcGISRuntimeEnvironment.SetLicense(LicenseInfo.FromJson(licenseJson));
                }
                else
                {
                    // No license file found on disk, try to login and get a license from ArcGIS Portal.
                    
                    // Create a challenge request for portal credentials (OAuth credential request for arcgis.com)
                    CredentialRequestInfo loginInfo = new CredentialRequestInfo
                    {
                        // Use the OAuth authorization code workflow.
                        GenerateTokenOptions = new GenerateTokenOptions
                        {
                            TokenAuthenticationType = TokenAuthenticationType.OAuthAuthorizationCode
                        },

                        // Indicate the url (portal) to authenticate with (ArcGIS Online)
                        ServiceUri = new Uri(portalUrl)
                    };

                    // Call GetCredentialAsync on the AuthenticationManager to invoke the challenge handler
                    Credential cred = await AuthenticationManager.Current.GetCredentialAsync(loginInfo, false);

                    // Connect to the portal (ArcGIS Online, for example).
                    ArcGISPortal arcgisPortal = await ArcGISPortal.CreateAsync(new Uri(portalUrl), cred);

                    // Get LicenseInfo from the portal
                    LicenseInfo licenseInfo = await arcgisPortal.GetLicenseInfoAsync();

                    // Write the license string to a file.
                    File.WriteAllText(LicenseFileName, licenseInfo.ToJson());

                    // License the app using the license info
                    ArcGISRuntimeEnvironment.SetLicense(licenseInfo);
                }
            }
            catch (Exception ex)
            {
                // TODO: handle exceptions
            }
        }
	}
}