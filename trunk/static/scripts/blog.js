function DeletePost(postid){
	if(confirm("Really delete this post?")){
		window.location = "/blog/deletepost?postid=" + postid;
	}
}

function DeleteComment(commentid){
	if(confirm("Really delete this comment?")){
		window.location = "/blog/deletecomment?commentid=" + commentid;
	}
}

function EditPost(postid){
	window.location = "/blog/editpost/" + postid;
}

$(document).ready(function(){
		});
