var BIG={'headliners':1,'kirillevans':1,'romantomera':1,'problockchain':1,'forklog':1,'doubletop':1,'gerchik':1,'cryptology':1,'cryptofateev':1,
  'cryptoinside':1,'nikitaanufriev':1,'headlinersru':1,'cryptofalcon':1,'tomaskralov':1,'wyckoff':1,'prometheusbtc':1,
  'slezysatoshi':1,'rdeni':1,'sercrypto':1,'instarding':1,'iliakorovin':1,'mamkintrader':1};
var MED={'gateio':1,'bingx':1,'bitget':1,'coinw':1,'whitebit':1,'dnevnik':1,'birzhevik':1,'centrproryva':1,'shkolaerina':1,'sercryptoch':1,'prometheuscrypto':1};

function initGraph(){
  var nodes=new vis.DataSet(NN.map(function(n){
    var ec=C[n.g]||'#888';
    // 3-layer structure:
    // Layer 1: Exchanges (центр) — mass=15, size=32
    // Layer 2: Tools (средний слой) — mass=3-4, size=14-22
    // Layer 3: Channels/competitors (внешний слой) — mass=0.8-1.8, size=16-30
    var m,sz;
    if(n.g==='exchange'){m=15; sz=32;}
    else if(n.g==='tool'){m=3; sz=n.id in BIG?20:(n.id in MED?16:13);}
    else{ // competitor/channel
      if(n.id in BIG){m=1.8; sz=28;}
      else if(n.id in MED){m=1.2; sz=20;}
      else{m=0.7; sz=15;}
    }
    // Special sizing for key nodes
    if(n.id==='headliners'){m=6; sz=34;}
    if(n.id==='nikitaanufriev'){m=3; sz=26;}
    
    return{id:n.id,label:n.l,group:n.g,
      color:{background:ec,border:'#fff',
        highlight:{background:'#ffff88',border:ec},
        hover:{background:'#ffff88',border:ec}},
      font:{color:'#fff',strokeWidth:3,strokeColor:'#000',size:Math.min(sz*0.38,13),multi:true,bold:true},
      borderWidth:2,borderWidthSelected:4,size:sz,
      shape:n.g==='exchange'?'box':'dot',mass:m};
  }));
  var edgeColor={'partner':'#ffd93d','competitor':'#ff6b6b','founder':'#00d4aa'};
  var edges=new vis.DataSet(EE.map(function(e,i){
    return{id:i,from:e.f,to:e.t,label:e.l,title:e.d,
      color:{color:edgeColor[e.l]||'#555',highlight:'#fff',hover:'#fff'},
      width:1.8,font:{size:9,color:edgeColor[e.l]||'#888',strokeWidth:2,strokeColor:'#0f0f1a',align:'middle'},
      smooth:{type:'curvedCW',roundness:0.15},
      arrows:{to:{enabled:true,scaleFactor:0.6}}};
  }));
  net=new vis.Network(document.getElementById('graph-canvas'),{nodes:nodes,edges:edges},{
    physics:{solver:'barnesHut',
      barnesHut:{gravitationalConstant:-4000,centralGravity:0.35,springLength:320,springConstant:0.025,damping:0.5},
      stabilization:{iterations:600}},
    layout:{improvedLayout:true},
    interaction:{hover:true,tooltipDelay:200,keyboard:true,zoomView:true,dragView:true},
    edges:{smooth:{type:'curvedCW'}},
  });
  var ld=document.getElementById('loading');
  if(ld)ld.style.display='none';
  net.once('stabilizationIterationsDone',function(){
    net.fit({animation:true,duration:300});
    // Highlight Headliners node initially
    net.selectNodes(['headliners']);
    showNode('headliners');
  });
  net.on('click',function(p){
    if(p.nodes.length>0)showNode(p.nodes[0]);
    else net.unselectAll();
  });
  net.on('hoverNode',function(p){document.body.style.cursor='pointer';});
  net.on('blurNode',function(p){document.body.style.cursor='default';});
}

