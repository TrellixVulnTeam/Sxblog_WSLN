//全选
function select(){
	for(var $i=0;$i<checkall.length;$i++){  
		checkall[$i].checked=true;  
	}  
};
//反选
function reverse(){
	for(var $i=0;$i<checkall.length;$i++){  
		if(checkall[$i].checked){  
			checkall[$i].checked=false;  
		}else{  
			checkall[$i].checked=true;  
		}  
	}  
}     
//全不选     
function noselect(){ 
	for(var $i=0;$i<checkall.length;$i++){  
		checkall[$i].checked=false;  
	}  
} 
