using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;

namespace GraphicsLayerDemo
{
	internal class GLDemo : Module
	{
		private static GLDemo _this = null;

		/// <summary>
		/// Retrieve the singleton instance to this module here
		/// </summary>
		public static GLDemo Current
		{
			get
			{
				return _this ?? (_this = (GLDemo)FrameworkApplication.FindModule("GraphicsLayerDemo_Module"));
			}
		}

		#region Overrides
		/// <summary>
		/// Called by Framework when ArcGIS Pro is closing
		/// </summary>
		/// <returns>False to prevent Pro from closing, otherwise True</returns>
		protected override bool CanUnload()
		{
			//TODO - add your business logic
			//return false to ~cancel~ Application close
			return true;
		}

		#endregion Overrides

	}
}
