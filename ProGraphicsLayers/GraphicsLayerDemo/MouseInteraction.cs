using ArcGIS.Core.CIM;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Editing;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Mapping;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Input;

namespace GraphicsLayerDemo
{
	internal class MouseInteraction : MapTool
	{
		public MouseInteraction()
		{
			IsSketchTool = false;
			
		}

		protected override void OnToolMouseDown(MapViewMouseButtonEventArgs e)
		{
			switch (e.ChangedButton)
			{
				case MouseButton.Right:
				case MouseButton.Left:
				case MouseButton.Middle:
					e.Handled = true;
					break;
			}
		}

		protected override Task HandleMouseDownAsync(MapViewMouseButtonEventArgs e)
		{
			// Check if the current map is available and a 2D map.
			Map map = MapView.Active.Map;
			if (map.MapType != MapType.Map)
			{
				// Map isn't a 2d map.
				return null;
			}

			// Create a grapics layer
			GraphicsLayerCreationParams gl_param = new GraphicsLayerCreationParams { Name = "Graphics Demo Layer" };
			return QueuedTask.Run(() =>
			{
				// Get the mouse click point
				MapPoint location = MapView.Active.ClientToMap(e.ClientPoint);

				GraphicsLayer graphicsLayer = map.Layers.FirstOrDefault(item => item.GetType() == typeof(GraphicsLayer)) as GraphicsLayer;
				if (graphicsLayer == null)
				{
					// By default will be added to the top of the TOC
					graphicsLayer = LayerFactory.Instance.CreateLayer<GraphicsLayer>(gl_param, map);
				}

				// Create a symbol based on the mouse button.
				CIMPointSymbol pointSymbol = null;
				if (e.ChangedButton == MouseButton.Left)
				{
					// Specify a symbol
					pointSymbol = SymbolFactory.Instance.ConstructPointSymbol(ColorFactory.Instance.CreateRGBColor(255, 0, 255), 40, SimpleMarkerStyle.Circle);
				}
				else if (e.ChangedButton == MouseButton.Right)
				{
					// Specify a symbol
					pointSymbol = SymbolFactory.Instance.ConstructPointSymbol(ColorFactory.Instance.CreateRGBColor(255, 0, 255), 40, SimpleMarkerStyle.Cross);
				}
				else
				{
					// Specify a symbol
					pointSymbol = SymbolFactory.Instance.ConstructPointSymbol(ColorFactory.Instance.CreateRGBColor(255, 0, 255), 30, SimpleMarkerStyle.Pushpin);
				}

				// Create a CIMGraphic to show the symbol on the map in the grapicslayer. 
				var graphic = new CIMPointGraphic()
				{
					Symbol = pointSymbol.MakeSymbolReference(),
					Location = location
				};

				// Add the graphic to the grapicslayer. 
				graphicsLayer.AddElement(graphic);

				// By default all items are selected, deselect all items
				graphicsLayer.UnSelectElements();
			});
		}
	}
}