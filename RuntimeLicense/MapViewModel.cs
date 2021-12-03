using Esri.ArcGISRuntime.Mapping;
using RuntimeLicense.Helpers;
using System;
using System.ComponentModel;
using System.Runtime.CompilerServices;
using System.Windows;

namespace RuntimeLicense
{
	/// <summary>
	/// Provides map data to an application
	/// </summary>
	public class MapViewModel : INotifyPropertyChanged
	{
		private Map _map = new Map(Basemap.CreateStreetsVector());

		// Constants for OAuth-related values.
		// The URL of the portal to authenticate with
		private const string ServerUrl = "https://www.arcgis.com/sharing/rest";

		public MapViewModel()
		{
			Initialize();
		}

		private async void Initialize()
		{
			try
			{
				// Set up the AuthenticationManager to use OAuth for secure ArcGIS Online requests.
				ArcGISLoginPrompt.SetChallengeHandler();

				// Gets a exisiting license from file or a new one from the ArcGIS Portal/Online.
				await ArcGISLicense.GetLicense(ServerUrl);
			}
			catch (Exception ex)
			{
				MessageBox.Show(ex.Message, "Error");
			}
		}

		/// <summary>
		/// Gets or sets the map
		/// </summary>
		public Map Map
		{
			get { return _map; }
			set { _map = value; OnPropertyChanged(); }
		}

		/// <summary>
		/// Raises the <see cref="MapViewModel.PropertyChanged" /> event
		/// </summary>
		/// <param name="propertyName">The name of the property that has changed</param>
		protected void OnPropertyChanged([CallerMemberName] string propertyName = null)
		{
			var propertyChangedHandler = PropertyChanged;
			if (propertyChangedHandler != null)
				propertyChangedHandler(this, new PropertyChangedEventArgs(propertyName));
		}

		public event PropertyChangedEventHandler PropertyChanged;
	}
}