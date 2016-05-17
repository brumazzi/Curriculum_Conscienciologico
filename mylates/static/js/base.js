var elt = function(id){
	return document.getElementById(id);
}
var elts = function(class_name){
	var el = document.getElementsByClassName(class_name);
	if(el.length == 0)
		return null;
	else if(el.length == 1)
		return el[0];
	else
		return el;
}
var load_form = function(form){
	/*xmlf = new XMLHttpRequest();
	xmlf.open("GET",url, true);
	xmlf.onreadystatechange = function(){
		if(xmlf.readyState == 4){
			elts('form_load').innerHTML = xmlf.responseText;
			elts('form_load').style.display = 'block';
		}
	};
	xmlf.send();*/
	location.href="/curriculum?form="+form;
}
