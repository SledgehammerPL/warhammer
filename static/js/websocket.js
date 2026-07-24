(function () {
  "use strict";

  function byId(id) {
    return document.getElementById(id);
  }

  function getLeaderName() {
    var el = byId("leader-name");
    if (!el || !el.textContent) {
      return null;
    }
    try {
      return JSON.parse(el.textContent);
    } catch (err) {
      return null;
    }
  }

  function wsScheme() {
    return window.location.protocol === "https:" ? "wss" : "ws";
  }

  function connectWebSocket(leaderName) {
    var safeLeader = encodeURIComponent(leaderName);
    var candidates = [
      wsScheme() + "://" + window.location.host + "/ws/party/" + safeLeader + "/",
      wsScheme() + "://" + window.location.host + "/ws/ws/party/" + safeLeader + "/"
    ];

    var socket = null;
    var index = 0;

    function tryConnect() {
      if (index >= candidates.length) {
        return;
      }
      socket = new WebSocket(candidates[index]);

      socket.onopen = function () {
        setupHandlers(socket);
      };

      socket.onerror = function () {
        index += 1;
        tryConnect();
      };
    }

    function setupHandlers(activeSocket) {
      var chatLog = byId("chat-log");
      var input = byId("chat-message-input");
      var submit = byId("chat-message-submit");

      activeSocket.onmessage = function (event) {
        var data;
        try {
          data = JSON.parse(event.data);
        } catch (err) {
          return;
        }

        if (data.message && chatLog) {
          chatLog.value += data.message + "\n";
          chatLog.scrollTop = chatLog.scrollHeight;
        }

        if (data.redirect) {
          window.location.href = data.redirect;
        }
      };

      if (!input || !submit) {
        return;
      }

      function sendMessage() {
        var message = (input.value || "").trim();
        if (!message || activeSocket.readyState !== WebSocket.OPEN) {
          return;
        }
        activeSocket.send(JSON.stringify({ message: message }));
        input.value = "";
      }

      submit.addEventListener("click", sendMessage);
      input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
          event.preventDefault();
          sendMessage();
        }
      });
    }

    tryConnect();
  }

  document.addEventListener("DOMContentLoaded", function () {
    var leaderName = getLeaderName();
    if (!leaderName) {
      return;
    }
    connectWebSocket(leaderName);
  });
})();
