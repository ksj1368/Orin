chrome.storage.local.get(['selectedText'], function(result) {
    var selectedText = result.selectedText;
    var contentDiv = document.getElementById('inputTextarea');
    contentDiv.innerText = selectedText;
});

document.addEventListener('DOMContentLoaded', function() {
    const requestButton = document.getElementById('requestButton');
    const inputTextarea = document.getElementById('inputTextarea');
    const outputContainer = document.getElementById('outputContainer');
    const arrow = document.getElementById('arrow');
  
    requestButton.addEventListener('click', function() {
      const inputText = inputTextarea.value;
      arrow.style.display = "block";
  
      const payload = {
        color_blindness: '0',
        q: inputText,
      };
  
      const headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'referer': 'https://search.naver.com/',
      };
  
      const url = 'https://m.search.naver.com/p/csearch/ocontent/util/SpellerProxy';
  
      fetch(url, {
        method: 'POST',
        headers: headers,
        body: new URLSearchParams(payload)
      })
      .then(response => response.json())
      .then(data => {
        console.log(data);
        const result = data.message.result.html;
        outputContainer.innerHTML = result;
      })
      .catch(error => {
        console.error('Error:', error);
      });
    });
    
    var openNewTabButton = document.getElementById('openNewTabButton');
    openNewTabButton.addEventListener('click', function() {
      var newTabUrl = 'https://orinone.com';
      chrome.tabs.create({ url: newTabUrl }, function() {
        // 탭이 성공적으로 열린 후에 textarea 내용 초기화
        chrome.storage.local.set({ 'textareaContent': '' });
      });
    });

    // Submit 버튼을 클릭할 때의 이벤트 리스너를 등록합니다.
    document.getElementById('getSynonymsButton').addEventListener('click', function() {
    // inputTextarea의 값을 가져옵니다.
    var word = inputTextarea.value;
    arrow.style.display = "block";
    // API에 요청을 보냅니다.
    var url = 'https://dict.naver.com/search.dict?dicQuery=' + encodeURIComponent(word) + '&query=' + encodeURIComponent(word) + '&target=dic&ie=utf8&query_utf=&isOnlyViewEE=';
    console.log(url);
    fetch(url)
      .then(response => response.text())
      .then(data => {
        // HTML 코드를 DOM 객체로 파싱합니다.
        var parser = new DOMParser();
        var doc = parser.parseFromString(data, 'text/html');

        // 원하는 내용을 추출하기 위해 DOM 조작을 사용합니다.
        var content = doc.querySelector('#content > div.kr_dic_section.search_result.dic_kr_entry > ul > li:nth-child(1)'); // 예시: 클래스명이 'content'인 요소를 추출
        console.log(content);
        // 클래스가 "syno"인 모든 <a> 요소 추출
        try{
          var whatword = content.querySelector('span.c_b');
          var aElements = content.querySelectorAll('a.syno');

          
          if (aElements.length > 0) {
            var outputText = '';

            for (var i = 0; i < aElements.length; i++) {
              if (i == (aElements.length - 1)){
                outputText += aElements[i].innerText.replace(/\d/g, '');
              }
              else outputText += aElements[i].innerText.replace(/\d/g, '') + ',';
            }
            output =
            `<div><span style="color : red";>${whatword.innerText}</span>의 유의어는 ${outputText}
            입니다.</div>`;

            outputContainer.innerHTML = output;
          } else {
            outputContainer.innerHTML = '결과를 찾을 수 없습니다.';
          }
        } catch {
          outputContainer.innerHTML = '결과를 찾을 수 없습니다.';
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });


      function resetTextarea() {
        document.getElementById('inputTextarea').innerText = '';
      }
      
      // 팝업이 닫힐 때 resetTextarea 함수 호출
      window.onbeforeunload = function() {
        resetTextarea();
      };
  });
  
});
