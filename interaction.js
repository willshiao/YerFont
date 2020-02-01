// var FileSaver = new FileSaver;


// var ctx = new C2S(500,500);
// let mySerializedSVG = ctx.getSerializedSvg(true); //true here, if you need to convert named to numbered entities.
// //If you really need to you can access the shadow inline SVG created by calling:
// let svg = ctx.getSvg();
// console.log(svg);


// Keep everything in anonymous function, called on window load.
var drawingMap = {} // make global so we can inspect it

window.onload = function () {
  const API_URL = 'http://localhost:5000/svg2font'
  var currentIdx = 0
  const targetLetters = 'abcdefghijklmnopqrstuvwxyz'
  const currentLtrEl = document.getElementById('current-ltr')
  var drawPath;

  // canvas variables
  var canvas, clear, submit, context, tool;
  // svg variables
  // var svg, mySerializedSVG;
  function init() {
    currentLtrEl.innerHTML = targetLetters[currentIdx]
    canvas = document.getElementById('imageView');
    paper.setup(canvas)
    clear = document.getElementById('clear');
    submit = document.getElementById('submit');
    const createBtn = document.getElementById('create-btn');
    const mainForm = document.getElementById('ltr-form')

    // Get the 2D canvas context.
    context = canvas.getContext('2d');

    paper.setup(canvas);
    paper.view.onMouseDown = function(evt) {
      myPath = new paper.Path();
      myPath.strokeColor = 'black';
    }
    paper.view.onMouseDrag = function (evt) {
      myPath.add(evt.point);
    }
    paper.view.onMouseUp = function onMouseUp(evt) {
    }

    //clear canvas
    clear.addEventListener('click', () => {
      console.log("clear");
      // context.clearRect(0, 0, canvas.width, canvas.height);
      paper.project.activeLayer.removeChildren();
      // context.clearCanvas();
    }, false);
      
    mainForm.addEventListener('submit', (evt) => {
      evt.preventDefault()
      // console.log('submit')
      svg = paper.project.exportSVG({asString:true})
      console.log(svg)
      drawingMap[targetLetters[currentIdx]] = svg
      currentLtrEl.innerHTML = targetLetters[++currentIdx]
      paper.project.activeLayer.removeChildren();
    })

    createBtn.addEventListener('click', () => {
      console.log('Sending data:', drawingMap)
      fetch(API_URL, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: "POST",
        body: JSON.stringify(drawingMap)
      })
        .then(res => res.json)
        .then(data => {
          console.log('Got: ', data)
        })
    })
  }

  init();

}



