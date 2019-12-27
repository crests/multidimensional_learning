var Name = "";

var History;
function initHistory(){
  History.left = []; //左側の選択肢。[0,0,0]など1次元配列
  History.right = [];
  History.probLeft = [];
  History.probRight = [];
  History.choice = [];
  History.result = [];
  History.score =[0];
  showScore();
}
initHistory();

var Enum = [];
Enum['test-number'] = 0;
Enum['test-shape'] = 1;
Enum['test-color'] = 2;

var NextPage = [];
NextPage['test-number'] ='test-shape';
NextPage['test-shape'] = 'test-color';
NextPage['test-color'] = 'trial';
NextPage['trial']      = 'end';


var TestTime = 4;
var TrialTime = 30;
var FeatureParam = getCSV();



function showObj(selector){
  $(selector).removeClass('hide');
  $(selector).addClass('show');
}
function hideObj(selector){
  $(selector).addClass('hide');
  $(selector).removeClass('show');
}

function showPage(className){
  hideObj(".show");
  showObj('.' + className);

  initRandomImg(className);
}

function saveName(){
  Name = document.getElementsByTagName('textarea')[0].value;
}


function initRandomImg(className){
  var n = 2;
  var leftArr = get3random(n);
  var rightArr = get3random(n);
  var left = arr2string(leftArr);
  var right = arr2string(rightArr);
  while(checkIfSame(left,right,className)){
    var rightArr = get3random(n);
    var right = arr2string(rightArr);
  }
  History.left.push(leftArr);
  History.right.push(rightArr);
  changeImg(className, left, right);
  return;
}

function checkIfSame(left,right,className){
  return false ||
         left === right ||
         left.charAt(Enum[className]) === right.charAt(Enum[className]);
}


function getRandomImg(className, choice){
  History.choice.push(choice);
  clearImg(className);
  showFixation(className);
  var result = getResult(className)
  History.result.push(result);
  History.score.push(History.score[History.score.length - 1] + 10*result);
  showResponse(result);
  var timer = setInterval(function(){
    initRandomImg(className);
    hideResponse();
    clearFixation(className);
    if(ifEndTest()){
      (new CSV(getHistoryArray())).save(Name + '-' +className + '.csv')
      initHistory();
      showPage(NextPage[className]);
    }
    clearInterval(timer);
  }, 1500*(0.3*Math.random()+1.0));
  return;
}
function getRandomImg4trial(className, choice){
  History.choice.push(choice);
  clearImg(className);
  showFixation(className);
  var result = getResult(className)
  History.result.push(result);
  History.score.push(History.score[History.score.length - 1] + 10*result);
  showResponse(result);
  var timer = setInterval(function(){
    initRandomImg(className);
    hideResponse();
    clearFixation(className);
    if(ifEndTrial()){
      (new CSV(getTrialHistoryArray())).save(Name + '-' +className + '.csv')
      initHistory();
      showPage(NextPage[className]);
    }
    clearInterval(timer);
  }, 1800*(0.3*Math.random()+1.0));
  return;
}
function get3random(n){
  return [Math.floor(Math.random()*n),
          Math.floor(Math.random()*n),
          Math.floor(Math.random()*n)];
}

function arr2string(arr){
  var txt = "";
  for(var i=0; i<arr.length; i++){
    txt += arr[i].toString();
  }
  return txt;
}

function changeImg(className, left,right){
  document.getElementById(className+'-left').style.backgroundImage = 'url("img/stimuli_'+ left +'.svg")';
  document.getElementById(className+'-right').style.backgroundImage = 'url("img/stimuli_'+ right +'.svg")';
  return;
}
function clearImg(className){
  changeImg(className, "-", "-");
}

function changeFixation(className, show_or_hide){
  if (show_or_hide === "showFixation"){
    showFixation(className);
  } else {
    clearFixation(className);
  }
  return;
}

function showFixation(className){
  document.getElementById(className+'-middle').style.backgroundImage = 'url("img/fixation.svg")';
}
function clearFixation(className){
  document.getElementById(className+'-middle').style.backgroundImage = '';
}


function showResponse(hit_or_blow){
  var resultTxt;
  if (hit_or_blow == true){
    document.getElementById('result').style.backgroundImage = 'url("img/txt_hit.svg")';
  } else {
    document.getElementById('result').style.backgroundImage = 'url("img/txt_miss.svg")';
  }
  shoObj('.result');
  showScore();
}
function showScore(){
  var scorePtag = document.getElementsByClassName('score');
  for (var i=0; i<scorePtag.length; i++){
    scorePtag[i].innerHTML = "今の得点：  0" + History.score[History.score.length - 1].toString();
  }
}
function hideResponse(){
  var resultPtag = document.getElementsByClassName('result');
  for (var i=0; i<resultPtag.length; i++){
    resultPtag[i].innerHTML = "";
  }
}


function getResult(state){
  var left = History.left[History.left.length - 1];
  var right = History.right[History.right.length - 1];
  var choice = History.choice[History.choice.length - 1];

  if (state == 'trial'){
    var prob = getProbability();
    if(choice == 'left'){
      if(Math.random() < prob[0]){
        return true;
      }
      return false;
    }
    if (Math.random() < prob[1]){ // if right was choiced
      return true;
    }
    return false;
  }
  //if
  if(choice == 'left'){
    return (left[Enum[state]] - right[Enum[state]]) > 0;
  } else {
    return (right[Enum[state]] - left[Enum[state]]) > 0;
  }
}

function ifEndTest(){ // test trial. 4回連続で正解すると終了
  if (History.result.length < TestTime){
    return false;
  }
  for (var i=0; i<TestTime; i++){
    if(History.result[History.result.length - 1 - i] === false){
      return false;
    }
  }
  return true;
}
function ifEndTrial(){ // test trial
   if (History.result.length == TrialTime){
     return true;
   }
   return false;
}

function getHistoryArray(){
  return [History.left, History.middle, History.right, History.choice, History.result, History.score];
}

function getTrialHistoryArray(){
  return [History.left, History.middle, History.right,History.choice, History.result, History.score];
}





function setCSV(str) {
  var data = [];
  var dataArr;
  var r = document.getElementById('r');
  var tmp = str.split('\n');
  tmp.forEach(x => {
    dataArr = x.split(',');
    if (dataArr[0]) {
      data.push(dataArr.map(x => x.trim()));
    }
  });
  //CSV = data;
  return data;
}

function getCSV(){
  var txt = new XMLHttpRequest();
  txt.open('get', "file:///Users/arataNonami/research/feature-learning/code/rateTable_size20_300trials_001.csv", false); //同期リクエスト
  txt.send();
  return setCSV(txt.responseText);
}
