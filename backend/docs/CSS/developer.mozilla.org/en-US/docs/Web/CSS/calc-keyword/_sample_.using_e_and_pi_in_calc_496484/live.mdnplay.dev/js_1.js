
                // sliders
const eInput = document.querySelector("#e-slider");
const piInput = document.querySelector("#pi-slider");
// spans for displaying values
const eValue = document.querySelector("#e-value");
const piValue = document.querySelector("#pi-value");

eInput.addEventListener("input", function () {
  e.style.transform = "rotate(calc(1deg * pow(" + this.value + ", e)))";
  eValue.textContent = e.style.transform;
});

piInput.addEventListener("input", function () {
  pi.style.rotate = "calc(sin(" + this.value + " * pi) * 100deg)";
  piValue.textContent = pi.style.rotate;
});

            