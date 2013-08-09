
console.log("Event Flairs utils loaded");

var delete_mode = false;

function flairFactory(url)
{
	var img = document.createElement("img");
	img.setAttribute("src",url);
	img.setAttribute("width",16);
	img.setAttribute("height",16);
	img.setAttribute("style","cursor:pointer;padding-left:3px;");
	img.setAttribute("onclick","setIcon(this)");
	return img;
}

function splitRootIcon(url)
{
	var surl = url.split("/");
	var icon = surl[surl.length-1];
	var root = url.replace(icon,"");
	return {'root' : root, 'icon' : icon};
}

function toggleDeleteFlair()
{
	if(delete_mode)
	{
		document.getElementById("delete").style.backgroundColor = "transparent";
		delete_mode = false;
	}
	else
	{
		document.getElementById("delete").style.backgroundColor = "lightgrey";
		delete_mode = true;
	}
	console.log("Will delete icon ? ",delete_mode);
}

