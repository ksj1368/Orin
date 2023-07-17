chrome.runtime.onInstalled.addListener(() => {
    console.log("Hello, World!");
});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  var selectedText = message.selectedText;
  console.log(selectedText);
  chrome.storage.local.set({ selectedText: selectedText });
});

chrome.contextMenus.create({
    id: "1",
    title:"Orin 교정 서비스로 바로가기 : \"%s\"",
    contexts: ["selection"],
});

chrome.contextMenus.onClicked.addListener(function(info, tab) {
    const baseURL = "https://orinone.com/correction/";
    const newText = info.selectionText;
  
    chrome.tabs.create({ url: baseURL }, function(newTab) {
      chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo) {
        if (tabId === newTab.id && changeInfo.status === "complete") {
          chrome.tabs.onUpdated.removeListener(listener);
  
          chrome.scripting.executeScript({
            target: { tabId: newTab.id },
            function: setPageContent,
            args: [newText],
          });
        }
      });
    });
  });
  
  function setPageContent(newText) {
    const textarea = document.getElementById("jasoseo");
    if (textarea) {
      textarea.value = newText;
    }
  }

chrome.runtime.onConnect.addListener(function(port) {
  if (port.name === "popup") {
    port.onDisconnect.addListener(function() {
      // popup.html이 닫힐 때 textarea 내용 초기화
      chrome.storage.local.set({ 'textareaContent': '' });
    });
  }
});

// Background Script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  // 메시지 처리 로직

  // 응답 전송
  sendResponse({ result: 'success' });
  // 더 이상 sendResponse를 사용하지 않을 경우, 반드시 true를 반환해야 합니다.
  return true;
});

