function show_menu_define(){
	var swich = elt('menu');
	swich.checked = false;
	swich.onchange = function(){
		if(swich.checked){
			if(elts('menu').className.search('close_') != -1)
				elts('menu').className = elts('menu').className.replace('close_','open_');
			else
				elts('menu').className += " open_";
			if(elts('menu_flop').className.search('close_') != -1)
				elts('menu_flop').className = elts('menu_flop').className.replace('r_close_','r_open_');
			else
				elts('menu_flop').className += " r_open_";
		}else{
			elts('menu').className = elts('menu').className.replace('open_','close_');
			elts('menu_flop').className = elts('menu_flop').className.replace('r_open_','r_close_');
		}
	}
}
