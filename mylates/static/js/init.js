window.onload = function(){
	show_menu_define();
	window.onresize = function(){
		try{
			if(elts('form').clientHeight < window.innerHeight-(elts('header').clientHeight + elts('footer'.clientHeight))){
				elts('form').style.marginTop = ((window.innerHeight - elts('form').clientHeight)/2 - (elts('header').clientHeight+elts('footer').clientHeight)/2)+"px";
				elts('form').style.marginBottom = ((window.innerHeight - elts('form').clientHeight)/2 - (elts('header').clientHeight+elts('footer').clientHeight)/2)+"px";
			}
		}catch(err){}
	};
	window.onresize();
	var pr = elt('pass_rest');
	pr.onclick = function(){
		//pr.innerHTML = "<form action=\"/restore\"><input class=\"entry\" type=\"email\" placeholder=\"E-mail\" required><input class=\"button center gray_blue\" type=\"submit\" value=\"enviar\"></form>";
		//pr.className = "form center";
		pr.className = "ghost";
		elt('rp').className="center dark_blue";
	}
}
