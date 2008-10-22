var ETNGrotator = function (data,nameIMG,width,height,interval){
 this.nameIMG = nameIMG || 'rotateIMG';
 this.width = width || 260;
 this.height = height || 175;
 this.data = data || [];
 this.interval = interval || 23;
 this.init();
}

ETNGrotator.prototype.init = function(){
  this.curID = 0;
  document.write('<img style="FILTER: revealTrans(duration=1, transition=23)" height="'+this.height+'" src="'+this.data[this.curID].imgSRC+'" width="'+this.width+'" border="0" name="'+this.nameIMG+'" id="'+this.nameIMG+'" />');
  this.oIMG = document.getElementById(this.nameIMG);
 }

ETNGrotator.prototype.loop = function(name, interval){
 this.curID++;
 this.curID = this.curID%(this.data.length);
 if(document.all) {
   this.oIMG.filters.revealTrans.Transition=23;
   this.oIMG.filters.item(0).apply();
   this.oIMG.filters.item(0).play();
 }
 this.oIMG.src = this.data[this.curID].imgSRC;
 this.interval = interval || 23;
 this.Timer = setTimeout(name+".loop('"+name+"')", this.interval*1000);
}

/* use it
var rotateDATA = [
  {imgSRC : 'images/topslip-01.jpg'},
  {imgSRC : 'images/topslip-02.jpg'},
  {imgSRC : 'images/topslip-03.jpg'},
  {imgSRC : 'images/topslip-04.jpg'},
  {imgSRC : 'images/topslip-05.jpg'}
];

var rotator = new ETNGrotator(rotateDATA,'rotateIMG', 729, 60);
rotator.loop('rotator');
*/
