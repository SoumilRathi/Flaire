
                const logElement = document.querySelector("#log");
function log(text) {
  logElement.innerText = `${logElement.innerText}${text}\n`;
  logElement.scrollTop = logElement.scrollHeight;
}

const myRules = document.styleSheets[1].cssRules;

for (let i = 0; i < myRules.length; i++) {
  if (myRules[i] instanceof CSSPageRule) {
    log(`${myRules[i].style}`);
    log(`margin: ${myRules[i].style.margin}`);

    // Access properties using CamelCase properties
    log(`marginTop: ${myRules[i].style.marginTop}`);
    log(`marginRight: ${myRules[i].style.marginRight}`);
    log(`marginBottom: ${myRules[i].style.marginBottom}`);
    log(`marginLeft: ${myRules[i].style.marginLeft}`);
    log(`pageOrientation: ${myRules[i].style.pageOrientation}`);

    // Access properties using snake-case properties
    log(`margin-top: ${myRules[i].style["margin-top"]}`);
    log(`margin-right: ${myRules[i].style["margin-right"]}`);
    log(`margin-left: ${myRules[i].style["margin-left"]}`);
    log(`margin-bottom: ${myRules[i].style["margin-bottom"]}`);
    log(`page-orientation: ${myRules[i].style["page-orientation"]}`);

    log(`size: ${myRules[i].style.size}`);
    log("\n");
  }
}

            