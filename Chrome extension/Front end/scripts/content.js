chrome.runtime.onMessage.addListener(function(request) {
  let notification = document.createElement('div');
  notification.className = 'myExtensionNotification';

  notification.innerHTML = "Tweet: " + request.tweet + "<br>Result: " + request.result;
  document.body.appendChild(notification);
  setTimeout(function() {
    document.body.removeChild(notification);
  }, 10000);
});