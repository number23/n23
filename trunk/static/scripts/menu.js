var showtags    = new Array();
var timeoutids  = new Array();
var spans_width = new Array();
var divs_width  = new Array();
var spans_left  = new Array();
function showmenu(a)
{
  showtags[a] = true;
  if (isset(timeoutids[a]))
  {
	  window.clearTimeout(timeoutids[a]);
  }
  var e=$('#'+a);
  if (e.css("display")=="none"){e.fadeIn('fast')};
}
function hidemenu(a)
{
	showtags[a] = false;
	timeoutids[a] = setTimeout('hid("'+a+'")',1000);
}
function hid(a)
{
	var e=$('#'+a)
	if (e.css("display")=="block" && showtags[a]==false){e.fadeOut('fast')}
	showtags[a] = true;
}

$(menuinit);
$(checksize);
window.onresize = checksize;

function menuinit()
{
	$("div.menucontent").css(
	{
		"display":"none",
		"position":"absolute",
		"z-index":"100",
		"text-align":"left"
	});
}

function checksize()
{
	body_width  = $("body").width();	
	
	$("span.menuhead").each(
		function(i)
		{
  			spans_width[i] = $(this)[0].offsetWidth;
			spans_left[i] = fetchOffset(this)['left'];
		});
	$("div.menucontent").each(
		function(i)
		{
			divs_width[i] = $(this).width();
		if ((spans_left[i]+divs_width[i]+15)>body_width)
		{
			this.style.left = (spans_left[i]+spans_width[i]-divs_width[i])-15+"px";
		}
		else
		{
			this.style.left = spans_left[i]+"px";
		}

		});

}

var _st = window.setTimeout;
window.setTimeout = function(fRef, mDelay)
{
 if(typeof fRef == 'function'){
  var argu = Array.prototype.slice.call(arguments,2);
  var f = (function(){ fRef.apply(null, argu); });
  return _st(f, mDelay);
 }
 return _st(fRef,mDelay);
}

function isset(variable)
{
	return typeof variable == 'undefined' ? false : true;
}

function getid(id)
{
	return document.getElementById(id);
}

function in_array(needle, haystack)
{
	if(typeof needle == 'string')
	{
		for(var i in haystack)
		{
			if(haystack[i] == needle)
			{
				return true;
			}
		}
	}
	return false;
}
function fetchOffset(obj)
{
	var left_offset = obj.offsetLeft;
	var top_offset = obj.offsetTop;
	while((obj = obj.offsetParent) != null)
	{
	  left_offset += obj.offsetLeft;
	  top_offset += obj.offsetTop;
	}
	return { 'left' :left_offset,'top':top_offset};
}

function getsize(obj)
{
	var w = obj.offsetWidth;
	var h = obj.offsetHeight;
	return {"width":w,"height":h};
}
