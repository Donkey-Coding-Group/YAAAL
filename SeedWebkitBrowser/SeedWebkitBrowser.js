#!/usr/bin/env seed

/**
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>. 
**/


start();

function start() {
	Gtk = imports.gi.Gtk;
	WebKit = imports.gi.WebKit;

	Gtk.init(Seed.argv);
	buildGui();
	Gtk.main();
}

function buildGui() {
	//Create Window
	var window = new Gtk.Window( {title:"Seed - JavaScript Browser"} );
	window.signal.hide.connect( Gtk.main_quit );
	window.set_default_size(980, 700);
	window.show_all();
	
	//Create WebView
	var scroll = new Gtk.ScrolledWindow();
	scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC);
	window.add(scroll);
	
	var webWidget = new WebKit.WebView;
	scroll.add(webWidget);
	webWidget.open("http://www.google.com");
	
	
	window.show_all();
}
