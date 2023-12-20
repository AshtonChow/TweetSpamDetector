chrome.runtime.onInstalled.addListener(function() {
    chrome.contextMenus.create({
      "id": "spamDetect",
      "title": "Tweet Spam Detector",
      "contexts": ["selection"]
    });
  });

chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if (info.menuItemId === "spamDetect") {
    fetch('http://127.0.0.1:5000/classify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: info.selectionText })
    })
    .then(response => response.json())
    .then(data => {
      chrome.tabs.sendMessage(tab.id, {tweet: data.tweet, result:data.result});
    });
  }
});