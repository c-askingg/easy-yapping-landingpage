"use strict";
// Das veröffentlichte Jotform ist ein externer Dienst. Keine vorgetäuschte Speicherung.
// Ausschließlich freigegebene Wochen in diesem öffentlichen Verzeichnis ablegen.
function openLinkedImpulse() {
  const id = decodeURIComponent(window.location.hash.slice(1));
  const target = document.getElementById(id);
  if (target && target.tagName === "DETAILS") target.open = true;
}
window.addEventListener("hashchange", openLinkedImpulse);
openLinkedImpulse();
