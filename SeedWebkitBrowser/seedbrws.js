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


//Try importing everything
try {
	Gio = imports.gi.Gio;
	GLib = imports.gi.GLib;
	Gtk = imports.gi.Gtk;
	WebKit = imports.gi.WebKit;
}
catch(e) {
	Seed.print("You need to have the following installed:");
	Seed.print("\t - Gio");
	Seed.print("\t - GLib");
	Seed.print("\t - Gtk");
	Seed.print("\t - WebKit");
	Seed.print("\n");
	Seed.quit(1);
}

var FILEURL = Seed.argv[2];


/**Test if given URL is valid**/
if (FILEURL.length>7 && FILEURL.slice(0,7) == "http://")  {
	//Seed.print("Protocol = \"http\"");
	main();
}
else if (FILEURL.length>8 && FILEURL.slice(0,8) == "https://")  {
	//Seed.print("Protocol = \"https\"");
	main();
}
else if (FILEURL.length>7 && FILEURL.slice(0,7) == "file://") {
	//Seed.print("Protocol = \"file\"");
	main();
}
else {
	Seed.print("The given url is not valid");
	Seed.print("FILEURL[0,7] != http://");
	Seed.print("FILEURL[0,8] != https://");
	Seed.print("FILEURL[0,7] != file://");
}



function main() {
	Gtk.init(Seed.argv);
	buildGui();
	Gtk.main();
}

function buildGui(url) {
	//Create Window
	window = new Gtk.Window( {title:"Seed - JavaScript Browser"} );
	window.signal.hide.connect( Gtk.main_quit );
	window.set_default_size(980, 700);
	window.show_all();
	
	//Create WebView
	scroll = new Gtk.ScrolledWindow();
	scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC);
	window.add(scroll);
	
	webWidget = new WebKit.WebView;
	scroll.add(webWidget);
	
	/**If URI == file:// make URI an URL**/
	if (FILEURL.slice(0,7) == "file://") {
		webWidget.open(FILEURL.slice(6));
	}
	else {
		webWidget.open(FILEURL);
	}
	
	
	window.show_all();
}
