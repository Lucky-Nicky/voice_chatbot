// var websocket = null;
// var audioContext = new (window.AudioContext || window.webkitAudioContext)();
// var audioElement = document.getElementById('audio');
//
// // var startBtn = document.getElementById('startBtn');
// // startBtn.addEventListener('click', startAudioStream);
//
//
//
// function startAudioStream() {
//     if (!websocket) {
//         websocket = new WebSocket('wss://tts-api.xfyun.cn/v2/tts?authorization=YXBpX2tleT0iOGNiMjA3NmU4MGUwMGY4NzA4NmJkNjEwMzE2MjkzZjUiLCBhbGdvcml0aG09ImhtYWMtc2hhMjU2IiwgaGVhZGVycz0iaG9zdCBkYXRlIHJlcXVlc3QtbGluZSIsIHNpZ25hdHVyZT0iaEc4ZkZkcVVpMGZILzF3eDRmZmNZRThMQ1RkZGt3K2NJVU9Xb3FXY0NFST0i&date=Sun%2C+04+Jun+2023+15%3A13%3A50+GMT&host=ws-api.xfyun.cn'); // 替换为你的音频流 WebSocket URL
//
//         websocket.onopen = function () {
//             console.log('WebSocket 连接已建立');
//         };
//
//         websocket.onmessage = function (event) {
//             var audioData = event.data;
//             playAudio(audioData);
//         };
//
//         websocket.onclose = function () {
//             console.log('WebSocket 连接已关闭');
//             websocket = null;
//         };
//
//         websocket.onerror = function (event) {
//             console.error('WebSocket 错误:', event);
//         };
//     }
// }
//
// function playAudio(audioData) {
//     audioContext.decodeAudioData(audioData, function (buffer) {
//         var source = audioContext.createBufferSource();
//         source.buffer = buffer;
//         source.connect(audioContext.destination);
//         source.start(0);
//     }, function (error) {
//         console.error('解码音频数据出错:', error);
//     });
// }
//
