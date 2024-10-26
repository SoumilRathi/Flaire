
                const log = document.getElementById("log");
const myRules = document.styleSheets[document.styleSheets.length - 1].cssRules;
const mediaList = myRules[0]; // a CSSMediaRule representing the media query.
log.textContent += ` ${mediaList.media.mediaText}`;

            