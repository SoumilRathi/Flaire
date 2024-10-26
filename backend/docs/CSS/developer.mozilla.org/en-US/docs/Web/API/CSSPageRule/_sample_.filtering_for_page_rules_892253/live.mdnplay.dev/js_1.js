
                const logElement = document.querySelector("#log");
function log(text) {
  logElement.innerText = `${logElement.innerText}${text}\n`;
  logElement.scrollTop = logElement.scrollHeight;
}

for (
  let sheetCount = 0;
  sheetCount < document.styleSheets.length;
  sheetCount++
) {
  const sheet = document.styleSheets[sheetCount].cssRules;
  log(`styleSheet: ${sheetCount}`);

  const myRules = document.styleSheets[sheetCount].cssRules;
  log(`rules: ${myRules.length}`);
  for (let i = 0; i < myRules.length; i++) {
    log(`rule: ${myRules[i]}`);
    if (myRules[i] instanceof CSSPageRule) {
      //... Do something with CSSPageRule
    }
  }
}

            