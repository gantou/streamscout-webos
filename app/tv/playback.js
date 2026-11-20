/* Bounded playback policy; shared by the browser and deterministic tests. */
(function(root){
  'use strict';
  function playerConfig(smooth=true) {
    return {lowLatencyMode:false,startLevel:-1,maxBufferLength:smooth?60:20,
      maxMaxBufferLength:smooth?90:30,maxBufferSize:64*1024*1024,backBufferLength:20,
      liveSyncDurationCount:smooth?6:3,liveMaxLatencyDurationCount:smooth?12:6,
      maxLiveSyncPlaybackRate:1,abrBandWidthFactor:0.7,abrBandWidthUpFactor:0.5};
  }
  function createPlayback(options) {
    const {video,Hls,url,status}=options;
    if(!Hls){
      status('HLS.js unavailable; browser-native HLS may still work.');
      options.onFailure?.();
      return {
        engine:null,
        get failed(){return true;},
        destroy(){}
      };
    }
    const engine=new Hls(playerConfig(options.smooth!==false));
    const now=options.now||(()=>Date.now()),schedule=options.setInterval||root.setInterval.bind(root),cancel=options.clearInterval||root.clearInterval.bind(root);
    let dead=false,failed=false,networkRetries=0,mediaRetries=0,refreshes=0,refreshing=false,lastTime=video.currentTime,lastAdvance=now(),stalls=0,live=false,download=0;
    function fail(){failed=true;engine.stopLoad?.();status('Source unavailable. Try another source.');options.onFailure?.();}
    let healthySince=now();
    function lower(){healthySince=now();if(engine.levels.length>1){engine.nextAutoLevel=Math.max(0,engine.currentLevel-1);engine.autoLevelCapping=Math.max(0,engine.currentLevel-1);}}
    function recoverQuality(buffer){
      if(refreshing||buffer<10){healthySince=now();return;}
      const cap=engine.autoLevelCapping;
      if(Number.isInteger(cap)&&cap>=0&&now()-healthySince>=30000){
        engine.autoLevelCapping=cap+1>=engine.levels.length-1?-1:cap+1;
        healthySince=now();
      }
    }
    async function fresh(){
      if(refreshing||dead||failed)return;
      if(!options.refresh||refreshes>=1){fail();return;}
      refreshes++;refreshing=true;status('Refreshing expired or unavailable stream…');
      try{const next=await options.refresh();if(dead||failed)return;engine.loadSource(next);engine.startLoad();lastAdvance=now();}
      catch{if(!dead)fail();}finally{refreshing=false;}
    }
    engine.on(Hls.Events.ERROR,(_,data)=>{
      if(dead||failed||refreshing)return;
      if(data.details==='bufferStalledError')lower();
      if(!data.fatal)return;
      if(data.type===Hls.ErrorTypes.NETWORK_ERROR){
        const code=data.response?.code||data.networkDetails?.status;
        if(options.refresh&&[401,403,404,410,502].includes(code)&&refreshes<1){void fresh();return;}
        if(networkRetries++<2){status('Retrying stream…');lower();engine.startLoad();}
        else if(options.refresh&&refreshes<1)void fresh();else fail();
      } else if(data.type===Hls.ErrorTypes.MEDIA_ERROR&&mediaRetries++<1){status('Recovering video decoder…');engine.recoverMediaError();}
      else fail();
    });
    engine.on(Hls.Events.LEVEL_LOADED,(_,data)=>{live=!!data.details?.live;});
    engine.on(Hls.Events.FRAG_LOADED,(_,data)=>{
      const stats=data.frag?.stats||data.stats;
      const seconds=stats?.loading?(stats.loading.end-stats.loading.start)/1000:0;
      if(seconds>0&&stats.loaded>0)download=stats.loaded*8/seconds/1000000;
    });
    function tick(){
      if(dead||failed)return;
      let buffer=0;for(let i=0;i<video.buffered.length;i++){if(video.buffered.start(i)<=video.currentTime+.1&&video.buffered.end(i)>video.currentTime){buffer=video.buffered.end(i)-video.currentTime;break;}}
      const bandwidth=download||(Number(engine.bandwidthEstimate)||0)/1000000;
      options.diagnostics?.(`Buffer: ${buffer.toFixed(1)}s · ${video.videoHeight?video.videoHeight+'p':'Quality pending'} · Download: ${bandwidth?bandwidth.toFixed(1)+' Mbps':'pending'} · ${live&&Number.isFinite(engine.latency)?'Live delay: '+engine.latency.toFixed(1)+'s':'Live delay: unknown'} · ${engine.levels.length>1?'Adaptive quality':'Single quality source'}`);
      if(video.paused||video.ended||video.seeking||video.currentTime<lastTime-.1){healthySince=now();lastTime=video.currentTime;lastAdvance=now();return;}
      if(video.currentTime>lastTime+.1){lastTime=video.currentTime;lastAdvance=now();recoverQuality(buffer);return;}
      healthySince=now();
      if(now()-lastAdvance>=8000&&!refreshing){
        lastAdvance=now();stalls++;lower();status('Buffering — recovering slow stream…');
        if(stalls<=2)engine.startLoad();else if(options.refresh&&refreshes<1)void fresh();else fail();
      }
    }
    const timer=schedule(tick,1000);
    const playing=()=>{if(!dead&&!failed)status('Playing');};
    const waiting=()=>{healthySince=now();if(!dead&&!failed)status('Buffering — waiting for video data…');};
    video.addEventListener('playing',playing);video.addEventListener('waiting',waiting);
    engine.loadSource(url);engine.attachMedia(video);
    return {engine,get failed(){return failed;},destroy(){dead=true;cancel(timer);video.removeEventListener('playing',playing);video.removeEventListener('waiting',waiting);engine.destroy();}};
  }
  const lib={playerConfig,createPlayback};root.StreamScoutPlayback=lib;
  if(typeof module!=='undefined')module.exports=lib;
})(globalThis);
