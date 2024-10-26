
                const colorPicker = document.querySelector("input");
colorPicker.addEventListener("change", (evt) => {
  document.querySelector("p").style.webkitTextStrokeColor = evt.target.value;
});

            