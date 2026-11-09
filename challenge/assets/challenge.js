"use strict";
// Das veröffentlichte Jotform ist ein externer Dienst. Keine vorgetäuschte Speicherung.
// Ausschließlich freigegebene Wochen in diesem öffentlichen Verzeichnis ablegen.
function placeWeekOneRecording() {
  const archive = document.getElementById("woche-1");
  const archiveContent = archive?.querySelector(".week-archive__content");
  const recording = document.getElementById("aufzeichnungen-w1");
  if (archiveContent && recording) archiveContent.append(recording);
}
function openLinkedImpulse() {
  const id = decodeURIComponent(window.location.hash.slice(1));
  const target = document.getElementById(id);
  const parentDetails = target?.matches("details") ? target : target?.closest("details") || target?.querySelector("details");
  if (parentDetails) parentDetails.open = true;
  if (target && target.tagName === "DETAILS") target.open = true;
}
placeWeekOneRecording();
window.addEventListener("hashchange", openLinkedImpulse);
openLinkedImpulse();
