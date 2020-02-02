

var selectedFonts = []; 
var presetFonts = [{name:'jihwan-font', fileName:'./fonts/5240232123.ttf'}, {name: 'carolyn-font', fileName: './fonts/704312777.ttf'}, {name:'paris-font', fileName:'./fonts/8357429178.ttf'}, {name:'will-font', fileName: './fonts/1225762287.ttf'}];
  


// Keep everything in anonymous function, called on window load.
var drawingMap = {} // make global so we can inspect it

window.onload = function () {

  const API_URL = 'http://localhost:5000/svg2font';
  var currentIdx = 0;
  const targetLetters = 'abcdefghijklmnopqrstuvwxyz';
  const currentLtrEl = document.getElementById('current-ltr');
  
  //preset fonts, user can add their own to this.
 

  
  // moved to oninit()
  // for (let i = 0; i < presetFonts.length; i++) {
  //     let new_font = new FontFace(presetFonts[i].name, 'url(' + '"' + presetFonts[i].fileName + '")');
  //     new_font.load().then(function(loaded_face) {
  //       // use font here
  //       document.fonts.add(loaded_face);
  //   }).catch(function(error) {
  //   });
  // }

  // var fonts = document.querySelectorAll('.fontChoices');
  // for (let i = 0; (i < presetFonts.length && i < fonts.length); i++){
  //   fonts[i].style.fontFamily = presetFonts[i].name;
  //   fonts[i].innerHTML = '<input type="checkbox" class="list-group-item customFont" style="float: left;">'+previewPhrase;
  // }
  
  // user selected custom fonts, hold the name of the font
  

  var checkedBoxes = document.getElementsByClassName('customFont');

  for (i = 0; (i < checkedBoxes.length && i < presetFonts.length); i++){
    if (checkedBoxes[i].type === 'checkbox') {
      checkedBoxes[i].addEventListener('change', function(){
        if (this.checked){
          for (j = 0; j < checkedBoxes.length; j++){
            if (checkedBoxes[j] === this){
              selectedFonts.push(presetFonts[j].name);
            }
          }
          console.log(selectedFonts);
        }
        else {
          selectedFonts.splice(selectedFonts.indexOf(presetFonts[i]), 1);
          console.log(selectedFonts);
        }
      }); 
    }
  }
  
 
 
  // canvas variables
  var canvas, clear;

  function init() {
    currentLtrEl.innerHTML = targetLetters[currentIdx];
    canvas = document.getElementById('imageView');
    paper.setup(canvas);
    clear = document.getElementById('clear');
    submit = document.getElementById('submit');
    const createBtn = document.getElementById('create-btn');
    const mainForm = document.getElementById('ltr-form');

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
      svg = paper.project.exportSVG({asString:true})
      console.log(svg)
      drawingMap[targetLetters[currentIdx]] = svg
      currentLtrEl.innerHTML = targetLetters[++currentIdx]
      paper.project.activeLayer.removeChildren();
      if (currentIdx >= targetLetters.length){
        document.getElementById('prompt').innerHTML = "Please click 'Create Font'";
        document.getElementById('submit').disabled = true;
        document.getElementById('imageView').style.background = "none";
        clear.disabled = true;
      }
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

    for (let i = 0; i < presetFonts.length; i++) {
      let new_font = new FontFace(presetFonts[i].name, 'url(' + '"' + presetFonts[i].fileName + '")');
      new_font.load().then(function(loaded_face) {
        // use font here
        document.fonts.add(loaded_face);
    }).catch(function(error) {
    });
  }

  var fonts = document.querySelectorAll('.fontChoices');
  for (let i = 0; (i < presetFonts.length && i < fonts.length); i++){
    fonts[i].style.fontFamily = presetFonts[i].name;
  }



  }

  init();

}



