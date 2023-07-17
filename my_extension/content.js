// document.body.style.backgroundColor = 'orange';

console.log("CONTENT")

chrome.runtime.sendMessage({greeting:"hello"}, function(response){
    console.log(response.farewell);
});

document.addEventListener('mouseup', function(event) {
    var selectedText = window.getSelection().toString();
    try {
      chrome.runtime.sendMessage({ selectedText: selectedText });
    } catch (error) {
      // 예외 처리 로직
      console.error('메시지 전송 중 오류가 발생했습니다:', error);
    }
});