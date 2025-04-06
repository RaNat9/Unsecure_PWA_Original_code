// window.onpageshow = function (event) {
//   if (event.persisted) {
//     window.location.reload();
//   }
// };

// history.pushState(null, null, location.href);
// window.onpopstate = function () {
//   history.go(1);
// };

if ("serviceWorker" in navigator) {
  window.addEventListener("load", function () {
    navigator.serviceWorker
      .register("static/js/serviceWorker.js")
      .then((res) => console.log("service worker registered"))
      .catch((err) => console.log("service worker not registered", err));
  });
}
