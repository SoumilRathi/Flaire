
                const log = document.getElementById("log");
const button = document.querySelector("button");
const hat = document.querySelector(".colored-hat");
const rules = document.styleSheets[document.styleSheets.length - 1].cssRules;
const greenFontPaletteValuesRule = rules[3];
const blueFontPaletteValuesRule = rules[2];
log.textContent = `Overridden colors: ${blueFontPaletteValuesRule.overrideColors}`;

button.addEventListener("click", (event) => {
  if (hat.style.fontPalette !== "--green") {
    hat.style.fontPalette = "--green";
    log.textContent = `Overridden colors: ${greenFontPaletteValuesRule.overrideColors}`;
  } else {
    hat.style.fontPalette = "--blue";
    log.textContent = `Overridden colors: ${blueFontPaletteValuesRule.overrideColors}`;
  }
});

            