var Name = "";
var Filename = "file:///Users/arataNonami/research/feature-learning/code/goodTable/rateTable_size20_300trials_0004.csv";
var History;
function initHistory(){
  History.left = []; //左側の選択肢。[0,0,0]など1次元配列
  History.middle = [];
  History.right = [];

  History.probLeft = [];
  History.probMiddle = [];
  History.probRight = [];

  History.choice = [];
  History.result = [];
  History.score =[0];

  History.rt = [];
}
initHistory();

var Start=0;
var End = 0;
var N_trial = 300;
var FeatureProb = getCSV();
console.log(FeatureProb);

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

function startGame(){
  initHistory();
  startTrial();
}

function startTrial(){
  // make options (and save options)
  makeOptions();
  // show options
  showOptions();
  // show option object
  showObj('.cards');
  // set start time
  Start = performance.now();
  // get option prob (and save to History)
  getProb();
  //console
  console.log(getHistoryArray());
}

function showOptions(){
  left = History.left[History.left.length-1];
  middle = History.middle[History.middle.length-1];
  right = History.right[History.right.length-1];

  document.getElementsByClassName('left-card')[0].style.backgroundImage
    = 'url("img/stimuli_' + option2str(left) + '.svg")';
  document.getElementsByClassName('middle-card')[0].style.backgroundImage
    = 'url("img/stimuli_' + option2str(middle) + '.svg")';
  document.getElementsByClassName('right-card')[0].style.backgroundImage
    = 'url("img/stimuli_' + option2str(right) + '.svg")';
}
function option2str(option){
  return "" + option[0] + option[1] + option[2];
}
function makeOptions(){
  var comparableRate = 0.9;
  var comparable_or_not = false;
  if (Math.random() < comparableRate)
    comparable_or_not = true;
  console.log("comparable_or_not = "+comparable_or_not);

  var options = makeOptions0();
  while(if_comparable(options[0], options[1], options[2]) != comparable_or_not){
    options = makeOptions0();
  }
  console.log(if_comparable(options[0], options[1], options[2]));
  console.log([compare(options[0], options[1]),compare(options[1], options[2]),compare(options[2], options[0])]);
  History.left.push(options[0]);
  History.middle.push(options[1]);
  History.right.push(options[2]);
  return options;
}
function makeOptions0(){
  var left = get3random(2);
  var middle = get3random(2);
  var right = get3random(2);
  while (ifsame(left, middle)){
    middle = get3random(2);
  }
  while (ifsame(left, right) || ifsame(middle, right)){
    right = get3random(2);
  }
  return [left, middle, right];
}
function ifsame(a, b){
  return a[0]===b[0] && a[1]===b[1] && a[2]===b[2];
}
function get3random(n){
  return a = [Math.floor(Math.random()*n),
          Math.floor(Math.random()*n),
          Math.floor(Math.random()*n)];
}
function getProb(){
  left = History.left[History.left.length-1];
  middle = History.middle[History.middle.length-1];
  right = History.right[History.right.length-1];

  History.probLeft.push(getProb0(left));
  History.probMiddle.push(getProb0(middle));
  History.probRight.push(getProb0(right));
  console.log([getProb0(left), getProb0(middle) , getProb0(right) ]);
  return;
}
function getProb0(option){
  //fprob = FeatureProb[History.left.length - 1];
  n = History.left.length;
  return FeatureProb[0][n]*option[0] + FeatureProb[1][n]*option[1] + FeatureProb[2][n]*option[2];
}
function choosed(className, position){
  //時間を計測して保存する
  End = performance.now();
  History.rt.push(End - Start);
  // カードを隠す
  hideObj(".cards");
  //選択を記録する
  History.choice.push(position);
  // 結果の計算
  hit_or_blow = get_ifHit(position);
  //結果を点数に反映。結果の画像を表示する。そして、History.scoreに反映
  showResult(hit_or_blow);
  console.log(hit_or_blow);
  // 結果の画像をhide -> show
  showObj(".result");
  // 数秒待つ
  var timer = setInterval(function(){
    // 空白にする
    hideObj(".result");
    // 0.3秒待つ
    var timer2 = setInterval(function(){
      // 次のgameか、次のtrialか。
      if(N_trial == History.choice.length){
        endGame(className);
      } else {
        startTrial();
      }
      clearInterval(timer2);
    }, 250 + 100*Math.random());
    clearInterval(timer);
  }, 700 + 500*Math.random());
}
function compare(a,b){
  var diff = [a[0]-b[0], a[1]-b[1], a[2]-b[2]];
  if (diff[0]>=0 && diff[1]>=0 && diff[2]>=0){
    return "left_is_bigger";
  }
  if (diff[0]<=0 && diff[1]<=0 && diff[2]<=0){
    return "right_is_bigger";
  }
  return "these_are_comparable"
}
function if_comparable(a,b,c){
  if(compare(a,b)== "these_are_comparable"){
    if(compare(a,c)=="right_is_bigger" && compare(b,c)=="right_is_bigger"){
      return false;
    } else{
      return true;
    }
  }
  if(compare(a,b) == "right_is_bigger"){
    if(compare(b,c)=="these_are_comparable"){
      return true;
    } else {
      return false;
    }
  }
  if(compare(a,b) == "left_is_bigger"){
    if(compare(a,c)=="these_are_comparable"){
      return true;
    } else {
      return false;
    }
  }
}


function get_ifHit(position){
  var prob;
  if (position == 'left'){
    prob = History.probLeft[History.probLeft.length - 1];
  } else if(position == 'middle') {
    prob = History.probMiddle[History.probMiddle.length - 1];
  } else if(position == 'right') {
    prob = History.probRight[History.probRight.length - 1];
  }
  var hb = Math.random()*100 <= prob;
  History.result.push(hb);
  return hb;
}

function showResult(hit_or_blow){
  var score = History.score[History.score.length - 1];
  console.log(score);
  if(History.choice.length == 1){History.score = [];}
  console.log(score);
  if(hit_or_blow){
    document.getElementsByClassName('result')[0].style.backgroundImage = 'url("img/txt_hit.svg")';
    score += 10;
    History.score.push(score);
  } else {
    document.getElementsByClassName('result')[0].style.backgroundImage = 'url("img/txt_blow.svg")';
    History.score.push(score);
  }
  //結果を文字列で表示
  document.getElementsByClassName('score-txt')[0].innerHTML = "今の得点：   "+ ( '00000' + score ).slice( -4 );
}
function endGame(className){
  (new CSV(getHistoryArray())).save(Name +"_"+ className + '.csv');
}

function saveName(){
  Name = document.getElementsByTagName('textarea')[0].value;
}
function getCSV(){
  var txt = new XMLHttpRequest();
  txt.open('get', Filename, false); //同期リクエスト
  txt.send();
  return setCSV(txt.responseText);
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
function sleep(waitMsec) {
  var startMsec = new Date();
  // 指定ミリ秒間だけループさせる（CPUは常にビジー状態）
  while (new Date() - startMsec < waitMsec);
}
function getHistoryArray(){
  return [History.left, History.middle, History.right,
          History.probLeft, History.probMiddle, History.probRight,
          History.choice, History.result, History.score, History.rt];
}


//消したい
function showPage(className){
  hideObj(".show");
  showObj('.' + className);
}
