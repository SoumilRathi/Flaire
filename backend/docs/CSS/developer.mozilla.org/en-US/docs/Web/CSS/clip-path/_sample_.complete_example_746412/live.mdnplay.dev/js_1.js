
                const clipPathSelect = document.getElementById("clipPath");
clipPathSelect.addEventListener("change", (evt) => {
  document.getElementById("clipped").style.clipPath = evt.target.value;
});

            