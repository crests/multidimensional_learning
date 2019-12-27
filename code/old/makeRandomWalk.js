function makeRandomWalkArray(nTrial){
  var ret = [];
  ret.push(Math.floor(Math.random()*100));
  for(var i=1; i<nTrial; i++){
    ret[i] = ret[i-1] + Math.floor(Math.random()*13 - 6); //-1 or 0 or 1
    ret[i] = Math.min(Math.max(ret[i], 10),90);
  }
  return ret;
}

function makeRandomWalkArrays(nTrial, cols){
  var ret = [];
  for(var i=0; i<cols; i++){
    ret.push(makeRandomWalkArray(nTrial));
  }
  return ret;
}

function writeRandomWalkArrays(n,nTrial,cols){
  var i=0; var j =i;
  for(i; i<j+n; i++){
    (new CSV(makeRandomWalkArrays(nTrial, cols))).save('randomArr_' + i +'.csv');
  }
  return;
}

writeRandomWalkArrays(10,100,4);
