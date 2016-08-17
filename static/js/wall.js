num_magnets=1;
movable=false;
use_grid=false;

$(function(){
	load_magnets();
});

function free_magnet(num){
	$('#magnet-'+num).draggable({ handle: ".panel-heading",snap: true, stack: ".dragmagnet" });
	$('#magnet-'+num).resizable({minHeight: 200, minWidth: 200});
	if(use_grid){
		$('#magnet-'+num).draggable("option", "grid", [50,50]);
		$('#magnet-'+num).resizable("option", "grid", [50,50]);
	}
	$('#pushpin-'+num).removeClass("active");
}

function free_magnet_all(){
	$('.dragmagnet').draggable({ handle: ".panel-heading",snap: true, stack: ".dragmagnet" });
	$('.dragmagnet').resizable({minHeight: 200, minWidth: 200});
	if(use_grid){
		$('.dragmagnet').draggable("option", "grid", [50,50]);
		$('.dragmagnet').resizable("option", "grid", [50,50]);
	}
	$('#pushpin').removeClass("active");
}

function stick_magnet(num){
	$('#magnet-'+num).draggable("destroy").resizable("destroy");
	$('#pushpin-'+num).addClass("active");
}

function stick_magnet_all(){
	$('.dragmagnet').draggable("destroy").resizable("destroy");
	$('#pushpin').addClass("active");
}

function toggle_stick(num){
	if($('#magnet-'+num).data('uiDraggable')){
		stick_magnet(num);
	}else{
		free_magnet(num);
	}
}

function toggle_stick_all(num){
	if(movable){
		stick_magnet_all();
		movable=false;
	}else{
		free_magnet_all();
		
		movable=true;
	}
}

function toggle_grid(){
	if(use_grid){
		if(movable){
			$('.dragmagnet').draggable("option", "grid", false);
			$('.dragmagnet').resizable("option", "grid", false);
		}
		use_grid=false;
		$('#gridtoggle').removeClass("active");
	}else{
		if(movable){
			$('.dragmagnet').draggable("option", "grid", [50,50]);
			$('.dragmagnet').resizable("option", "grid", [50,50]);
		}
		use_grid=true;
		$('#gridtoggle').addClass("active");
	}
}

function toggle_edit(num){
	$('#edit-'+num).toggleClass("active");
  var $div=$('#body-'+num), isEditable=$div.is('.editable');
  $div.prop('contenteditable',!isEditable).toggleClass('editable');
}

function create_magnet(title="Magnet",text="Body",top=200,left=200,height=250,width=250){
	$('#walldiv').append('<div class="panel panel-default dragmagnet" id="magnet-'+num_magnets+'"></div>');
	$('#magnet-'+num_magnets).append('<div class="panel-heading"><div class="row"><div class="col-md-9">'+title+'</div><div class="col-md-3 text-right"><a href="javascript:;" class="btn btn-default btn-xs" id="edit-'+num_magnets+'" onclick="toggle_edit('+num_magnets+')"><span class="glyphicon glyphicon-edit"></span></a></div></div></div>');
	$('#magnet-'+num_magnets).append('<div class="panel-body magnetbody"><p id="body-'+num_magnets+'">'+text+'</p></div>');
	$('#magnet-'+num_magnets).css("z-index",num_magnets);
	$('#magnet-'+num_magnets).css("top",top);
	$('#magnet-'+num_magnets).css("left",left);
	$('#magnet-'+num_magnets).css("height",height);
	$('#magnet-'+num_magnets).css("width",width);
	if(movable){
		free_magnet(num_magnets);
	}
	num_magnets++;
}

function load_magnets(){
	$.ajax({
		dataType: "json",
		url: "/magnets",
		async: false,
		success: function(data){
			$(data).each(function(key,value){
				create_magnet(value['title'],value['text'],value['top'],value['left'],value['height'],value['width']);
			});
		}
	});
}

function save_magnet(num){
	leftValue = $("#magnet-"+num).css("left");
	topValue = $("#magnet-"+num).css("top");
	heightValue = $("#magnet-"+num).css("height");
	widthValue = $("#magnet-"+num).css("width");
	data = {id:num, left:leftValue, top: topValue, height: heightValue, width: widthValue}
	console.log(num);
	console.log(data);
	$.ajax({
		dataType: "html",
		url: "/magnet/"+num+"/edit",
		async: false,
		type: "POST",
		data: data,
		success: function(data){
				console.log(data);
		},error: function(data){
			console.log(data);
		}
	});
}