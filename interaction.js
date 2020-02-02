
// user selected fonts for merging/randomizing
var selectedFonts = []; 
// presetFonts that we made, but users can add their fonts to the list
var presetFonts = [{name:'jihwan-font', fileName:'./fonts/5240232123.ttf'}, {name: 'carolyn-font', fileName: './fonts/704312777.ttf'}, {name:'paris-font', fileName:'./fonts/8357429178.ttf'}, {name:'will-font', fileName: './fonts/1225762287.ttf'}, {name:'raleway', fileName:'.'}, {name: 'ai', fileName: "https://font-api.wls.ai/font/88888888.ttf"}, {name: 'animal', fileName: "https://font-api.wls.ai/font/3247351608.ttf"}];
    
var prevInput;

// Keep everything in anonymous function, called on window load.
var drawingMap = {} // make global so we can inspect it

window.onload = function () {

  const API_URL = 'https://font-api.wls.ai/svg2font';
  var currentIdx = 0;
  const targetLetters = 'abcdefghijklmnopqrstuvwxyz';
  const currentLtrEl = document.getElementById('current-ltr');
  
  var checkedBoxes = document.getElementsByClassName('customFont');

  for (i = 0; (i < checkedBoxes.length && i < presetFonts.length); i++){
    if (checkedBoxes[i].type === 'checkbox') {
      checkedBoxes[i].addEventListener('change', function(){
        if (this.checked){
          for (j = 0; j < checkedBoxes.length; j++){
            if (checkedBoxes[j] === this){
              selectedFonts.push(presetFonts[j].name);
              demo.style.fontFamily = (presetFonts[j].name);
            }
          }
          console.log(selectedFonts);
        }
        else {
          selectedFonts.splice(selectedFonts.indexOf(presetFonts[i]), 1);
          demo.style.fontFamily = 'Raleway';
          console.log(selectedFonts);
        }
      }); 
    }
  }
  
  function loadFont(newURL) {
    // var newURL = "https://font.wls.ai/fonts/${num}.ttf"; //url from backend
    
    //strip numbers using regex
    var re = /[0-9]/g;
  
    //turn the stripped numbers to string
    //create the new font for our document
      var newFont = newURL.match(re).join('').toString();
  
      var face = new FontFace(`"${newFont}"`, 'url(' + newURL + ')');
      return face
        .load()
        .then(function(loaded_face) {
          document.fonts.add(loaded_face);
          console.log(loaded_face);
          presetFonts.push({name: newURL.match(re).join('').toString(), fileName: newURL});
          console.log('Added to present fonts: ', presetFonts);
        })
        .then(function(){
          var ul = document.getElementById("lists");
          var newLi = document.createElement("li");
          newLi.appendChild(document.createTextNode(""));
          newLi.setAttribute("class","list-group-item");
          newLi.innerHTML='<input type="checkbox" class="list-group-item customFont" style="float: left;"><span class="fontChoices">the quick brown fox jumps over the lazy dog</span></li>';
          newLi.style.fontFamily = '"'+newFont+'"';
          ul.appendChild(newLi);

          //new listener
          console.log(presetFonts[this.presetFonts.length-1].name);

          var input = document.getElementsByTagName('input');
          input[input.length-1].addEventListener('change', function(){
            if (this.checked){
              demo.style.fontFamily = '"'+newFont+'"';
                  selectedFonts.push(newLi.style.fontFamily);
                  console.log(selectedFonts);
            }
            else {
              for (i = 0; i < presetFonts.length; i++){
                if (presetFonts[i].name == newURL.match(re).join('').toString()){
                  selectedFonts.splice(selectedFonts.indexOf(presetFonts[i]), 1);
                  demo.style.fontFamily = 'Raleway';
                  console.log(selectedFonts);
                }
              }
            }
          }); 
          console.log(newLi.style);
        })
        .catch(function(error) {
          console.error(error)
          // error occurred
        });
  
  }
 
  // canvas variables
  var canvas, clear;

  function insertAfter(newNode, referenceNode) {
      referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
  }

  function randomClass(numClasses) {
    return `customfont-${Math.floor(Math.random() * numClasses)}` 
  }
  function randomSpan(contents, classes) {
    const classNum = Math.floor(Math.random() * classes)
    return `<span class="customfont-${classNum}">${contents}</span>`
  }

  function init() {
    currentLtrEl.innerHTML = targetLetters[currentIdx];
    canvas = document.getElementById('imageView');
    paper.setup(canvas);
    clear = document.getElementById('clear');
    submit = document.getElementById('submit');
    demo = document.getElementById('demo');
    const createBtn = document.getElementById('create-btn');
    const mainForm = document.getElementById('ltr-form');

    paper.view.onMouseDown = function(evt) {
      myPath = new paper.Path();
      myPath.strokeColor = 'black';
      myPath.strokeWidth = 10;
    }
    paper.view.onMouseDrag = function (evt) {
      myPath.add(evt.point);
    }
    paper.view.onMouseUp = function onMouseUp(evt) {
    }

    //clear canvas
    clear.addEventListener('click', () => {
      console.log("clear");
      paper.project.activeLayer.removeChildren();
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
        .then(res => res.json())
        .then(data => {
          console.log('Got: ', data);
          let newURL = "https://font-api.wls.ai/font/" + data.fontId + '.ttf';

         if(window.confirm("Download your font by pressing 'OK'!")){
          window.location.href=newURL;
         }
          loadFont(newURL)
            .then(() => { console.log('Done loading new font!') });
        })
     
      }
    )

    for (let i = 0; i < presetFonts.length; i++) {
      let new_font = new FontFace(presetFonts[i].name, 'url(' + '"' + presetFonts[i].fileName + '")');
      new_font.load().then(function(loaded_face) {
        // use font here
        document.fonts.add(loaded_face);
    }).catch(function(error) {
    });
  }

  var fonts = document.querySelectorAll('.fontChoices');
  for (let i = 0; (i < presetFonts.length); i++){
    fonts[i].style.fontFamily = presetFonts[i].name;
    console.log(fonts[i].style.fontFamily);
  }


  const prefixReplaceRegex = /^[^<]+/gi;
  const NUM_FONTS = 4
  //const replaceRegex = /(?:^|\/span>)([^<>]+)(?:<span|$)/gi

  const rawArea = document.getElementById('raw-area')
  const outputArea = document.getElementById('output-area')
  rawArea.addEventListener('input', (evt) => {
    const content = rawArea.value
    outputArea.innerHTML = content.split('').map(c => {
      const randNum = Math.floor(Math.random() * selectedFonts.length)
      return `<span style="font-family: ${selectedFonts[randNum]}">${c}</span>`
    }).join('')
  })
  demo.addEventListener("input", function(event) {
    const demoEl = document.getElementById('demo')
    if (prefixReplaceRegex.test(demoEl.innerHTML)) {
      demoEl.innerHTML = demoEl.innerHTML.replace(prefixReplaceRegex, randomSpan('$&', NUM_FONTS))
      const range = document.createRange();
      const sel = window.getSelection();
      range.setStart(demoEl.childNodes[demoEl.childNodes.length-1], 1);
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
    }
    let newP = ""
    elementList = this.querySelectorAll("span");
    
    // console.log(elementList.length)
    // if (elementList.length == 0) {
    //   console.log('Nothin found')
    //   demoEl.innerText = ''
    //   demoEl.innerHTML = '<span>a</span>'
    //   return
    // }
    console.log(demoEl.innerText)
    elementList.forEach(el => {
      // console.log('Hwan Ji Kim', el)
      //console.log( elementList[i].innerText);
      let currentVal = el.innerText;
      let lastEl = el
      if (currentVal.length == 1) return;
      el.innerText = currentVal.length > 0 ? currentVal[0] : ''
      //console.log(currentVal);
      for(let j=1;j<currentVal.length;j++) {
        let newSpan = document.createElement("SPAN")
        newSpan.className = randomClass(NUM_FONTS)
        // newSpan.innerText = 
        newSpan.appendChild(document.createTextNode(currentVal[j]));
        insertAfter(newSpan, lastEl)
        lastEl = newSpan
        // newP.after(newSpan);
        // newP = newSpan;
      }
      const range = document.createRange();
      const sel = window.getSelection();
      try {
        range.setStart(lastEl, 1);
      } catch(err) {}
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
      
    })
    
    //console.log(newP)
    //this.innerHTML = newP;
  }, false);
  

  }

  init();

}



