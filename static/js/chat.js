// 使用流式的方法，展示gpt的结果
function gpt_show_stream_info(url) {

    $("#submitbtn").prop('disabled', true)
    $("#submitCashBtn").prop('disabled', true)
    $("#result").html("ChatGPT正在请求中...")
    // "/chatgpt-clone?question="+$("#question").val()
    var source = new EventSource(url)
    var begin_output = false
    var context = ""
    var mp3_url;
    var isPlaying = false;
    var count = 0;
    var str_len = 10;  // 控制首次断句位置
    var started = false;  // 是否已开始（非首次）
    var currChunk = '';  // 当前需要转换成音频的片段
    var context_all = '';

    source.onmessage = function (event) {
        if (begin_output === false) {
            begin_output = true
            // $("#result").html("")
        }
        if (event.data === "[DONE]") {
            console.log('最后的内容：' + context);
            mp3_url = "/mp3_play?context=" + context + '&count=' + count;
            mp3_url = mp3_url.replace(/\s+/g, "");
            mp3_url = mp3_url.replace(/\<br\/\>/g, "");
            mp3_url = mp3_url.replace(/<br\s*\/?>/gi, "");
            mp3_show_stream_info(mp3_url);
            source.close()

            $("#submitbtn").prop('disabled', false)
            $("#submitCashBtn").prop('disabled', false)

            context = "";
            context_all = "";
            isPlaying = false;
            started = false;
            count = 0;

        } else {

            // 向页面写入chatGPT返回结果
            context_all = context_all + event.data;
            var textWithLineBreaks = context_all.replace(/<br\s*\/?>/g, "\n");
            if (isPlaying) {
                // 强制等待 2 秒
                setTimeout(function () {
                    $("#result").html(textWithLineBreaks);
                }, 2000);

            }

            context += event.data
            if (context.length >= str_len) {

                if (!started) {
                    currChunk = context.substring(0, str_len);
                    context = '';
                } else {
                    if (event.data.startsWith('。') || event.data.startsWith('，')) {
                        currChunk = context;
                        context = '';
                    } else {
                        currChunk = '';
                    }
                }

                if (currChunk.length > 0) {
                    mp3_url = "/mp3_play?context=" + currChunk + '&count=' + count;
                    mp3_url = mp3_url.replace(/\s+/g, "");
                    mp3_url = mp3_url.replace(/\<br\/\>/g, "");
                    mp3_show_stream_info(mp3_url);

                    // 从context中移除已经处理完毕的部分
                    context = context.substring(str_len);
                    count += 1;
                    started = true;

                    // 开始播放
                    if (count === 1 && !isPlaying) {
                        console.log('开始播放音频！')
                        playNextAudio();
                        isPlaying = true;
                    }
                }
            }
        }
    }

}

// 使用流式的方法，展示mp3音频结果
function mp3_show_stream_info(url) {
    $.ajax({
        url: url,
        type: "GET",
        success: function (data) {
            // $("#audio")[0].play();   # 这里有BUG，需要强制刷新音频资源
            // 播放音频
            // playAudio();

        }
    })
}

// 原先的逻辑
// function playAudio() {
//     var audioEle = document.getElementById('audio');
//     var audioSource = '/static/audio/demo.pcm'
//
//     var timestamp = new Date().getTime();
//     audioEle.src = audioSource + '?' + timestamp;
//
//     audioEle.play();
// }


var audioFiles = ['demo0.pcm'];  // 初始化为空数组

var currentIndex = 0;
var audioPlayer = document.getElementById("audio");
audioPlayer.addEventListener("ended", playNextAudio);
var maxRetryCount = 5; // 最大重试次数
var retryCount = 0; // 当前重试次数

function playNextAudio() {

    if (currentIndex < audioFiles.length) {
        var timestamp = new Date().getTime();
        audioPlayer.src = '/static/audio/' + audioFiles[currentIndex] + '?' + timestamp;
        audioPlayer.play()
            .then(function () {
                currentIndex++;  // 下标累增
                retryCount = 0; // 重置重试计数器
            })
            .catch(function (error) {
                // 播放失败
                if (retryCount < maxRetryCount) {
                    // 尝试重试
                    console.log('播放失败，尝试重试（第' + retryCount + '次）');
                    retryCount++;
                    setTimeout(playNextAudio, 2000) // 递归调用进行重试，间隔2秒
                } else {
                    console.log('播放失败次数超过最大重试次数，终止播放');
                }
            });

    } else {
        // 播放完成，尝试获取最新的音频列表
        fetchAudioList();
    }
}

function fetchAudioList() {
    // 发起异步请求获取最新的音频列表
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_audio_list", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // 解析后端返回的音频文件列表
            var updatedAudioFiles = JSON.parse(xhr.responseText);

            // 判断是否有更新的音频文件
            if (updatedAudioFiles.length > audioFiles.length) {
                audioFiles = updatedAudioFiles;
                playNextAudio();  // 播放下一个音频
            }else{
                console.log('播放完毕---------------------');
                audioFiles = ['demo0.pcm'];  // 初始化为空数组
                currentIndex = 0;
            }
        }
    };
    xhr.send();
}


function show_quota_info() {
    $.ajax({
        url: "/show_quotas",
        type: "GET",
        success: function (data) {
            $("#quota_info").html(data)
        }
    })
}