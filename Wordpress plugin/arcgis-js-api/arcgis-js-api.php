<?php
/**
 * @package   ArcGIS JavaScript API
 * @author    Mark Jagt
 * @license   GPL-2.0+
 * @link      https://www.esri.nl
 * @copyright 2021 Esri Nederland
 *
 * @wordpress-plugin
 * Plugin Name:       ArcGIS JavaScript API
 * Plugin URI:        https://www.esri.nl
 * Description:       Add an aplication written with the ArcGIS API for JavaScript 4.x to WordPress with a shortcode.
 * Version:           1.0.0
 * Author:            Mark Jagt
 * Author URI:        https://www.esri.nl
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {
	die;
}

/*----------------------------------------------------------------------------*
 * Public-Facing Functionality
 *----------------------------------------------------------------------------*/

 // load the arcgis javascript api
function load_arcgis() {
	wp_dequeue_script("jquery");
	//Add ArcGIS JavaScript API
	wp_register_script("arcgis_js_api", "https://js.arcgis.com/4.20/", NULL, NULL, true);
	wp_enqueue_script("arcgis_js_api");
}

add_action( 'wp_enqueue_scripts', 'load_arcgis' );

// register the arcgis styles
function register_styles(){
	wp_register_style( 'arcgis_style', 'https://js.arcgis.com/4.20/esri/themes/light/main.css' );
	wp_enqueue_style( 'arcgis_style');
}

add_action('wp_enqueue_scripts', 'register_styles' );

// add the custom js app defined in the file app.js
function load_app($atts) {
	$shortcodes = shortcode_atts( array(
		'webmapid' => '',
		'width' => '100%', // default 100% because most blogs will want this
		'height' => '',
		'apikey' => ''
	), $atts );

	$shortcodes = array_map( 'esc_attr', $shortcodes );

	wp_enqueue_script("customApp", plugins_url( '/app.js?webmapId='.$shortcodes['webmapid'].'&apiKey='.$shortcodes['apikey'] , __FILE__ ), NULL, NULL, true);

	return '<div id="viewDiv" style="width:'.$shortcodes['width'].';height:'.$shortcodes['height'].';max-width:100%"></div>';
}

add_shortcode( 'arcgis-js-app', 'load_app' );