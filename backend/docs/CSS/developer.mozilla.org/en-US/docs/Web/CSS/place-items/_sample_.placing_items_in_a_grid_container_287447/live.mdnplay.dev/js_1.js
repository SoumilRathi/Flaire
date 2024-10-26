
                const values = document.getElementById("grid-values");
const container = document.getElementById("grid-container");

values.addEventListener("change", (evt) => {
  container.style.placeItems = evt.target.value;
});

            