function newFile(){
	showdiv();
};

function showdiv(){
  $('#my_dialog').dialog({
	  modal:true,
	  width:"600",
  	});
};


function create_paper_cancel(){
	alert("cancel");
	$('#my_dialog').dialog("close");
};

function create_paper_save(){
	$('#my_dialog').dialog("close");
	var create_name = $("#create_name").val(); 
	var create_author = $("#create_author").val(); 
	alert("save！");
};

