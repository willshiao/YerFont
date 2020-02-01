// var FileSaver = new FileSaver;


var ctx = new C2S(500,500);
let mySerializedSVG = ctx.getSerializedSvg(true); //true here, if you need to convert named to numbered entities.
//If you really need to you can access the shadow inline SVG created by calling:
let svg = ctx.getSvg();
// console.log(svg);


/* © 2009 ROBO Design
 * http://www.robodesign.ro
 */

// Keep everything in anonymous function, called on window load.
if(window.addEventListener) {
  window.addEventListener('load', function () {
    // canvas variables
    var canvas, clear, submit, context, tool;
    // svg variables
    // var svg, mySerializedSVG;
    function init () {
      // Find the canvas element.
      canvas = document.getElementById('imageView');
      clear = document.getElementById('clear');
      submit = document.getElementById('submit');
      if (!canvas) {
        alert('Error: I cannot find the canvas element!');
        return;
      }
  
      if (!canvas.getContext) {
        alert('Error: no canvas.getContext!');
        return;
      }
  
      // Get the 2D canvas context.
      context = canvas.getContext('2d');
      // ctx = canvas.getContext('2d');
      if (!context) {
        alert('Error: failed to getContext!');
        return;
      }
  
      // Pencil tool instance.
      tool = new tool_pencil();
  
      // Attach the mousedown, mousemove and mouseup event listeners.
      canvas.addEventListener('mousedown', ev_canvas, false);
      canvas.addEventListener('mousemove', ev_canvas, false);
      canvas.addEventListener('mouseup',   ev_canvas, false);
      canvas.addEventListener('touchstart',   ev_canvas, false);
      canvas.addEventListener('touchmove',   ev_canvas, false);
      canvas.addEventListener('touchend',   ev_canvas, false);

      //clear canvas
      clear.addEventListener('click', ()=> {
        console.log("clear");
        context.clearRect(0, 0, canvas.width, canvas.height);
        ctx.clearCanvas();
      }, false);

      submit.addEventListener('click', ()=>{
        console.log("submit");
        console.log(svg);
        // var blob = new Blob([svg], {type: "text/plain;charset=utf-8"});
        // saveAs(blob, "letter.svg");

      }, false);
    }
  
    // This painting tool works like a drawing pencil which tracks the mouse 
    // movements.
    function tool_pencil () {
      var tool = this;
      this.started = false;
  
      // This is called when you start holding down the mouse button.
      // This starts the pencil drawing.
      this.mousedown = function (ev) {
          
          context.beginPath();
          context.moveTo(ev._x, ev._y);
          ctx.beginPath();
          ctx.moveTo(ev._x, ev._y);
          tool.started = true;
      };
  
      // This function is called every time you move the mouse. Obviously, it only 
      // draws if the tool.started state is set to true (when you are holding down 
      // the mouse button).
      this.mousemove = function (ev) {
        if (tool.started) {
          context.lineTo(ev._x, ev._y);
          context.stroke();
          ctx.lineTo(ev._x, ev._y);
          ctx.stroke();
        }
      };
  
      // This is called when you release the mouse button.
      this.mouseup = function (ev) {
        if (tool.started) {
          tool.mousemove(ev);
          tool.started = false;
        }
      };

  

    }



  
    // The general-purpose event handler. This function just determines the mouse 
    // position relative to the canvas element.
    function ev_canvas (ev) {
      if (ev.layerX || ev.layerX == 0) { // Firefox
        ev._x = ev.layerX;
        ev._y = ev.layerY;
      } else if (ev.offsetX || ev.offsetX == 0) { // Opera
        ev._x = ev.offsetX;
        ev._y = ev.offsetY;
      }
  
      // Call the event handler of the tool.
      var func = tool[ev.type];
      if (func) {
        func(ev);
      }
    }
  
    init();
  
  }, false); }
  
 
  
