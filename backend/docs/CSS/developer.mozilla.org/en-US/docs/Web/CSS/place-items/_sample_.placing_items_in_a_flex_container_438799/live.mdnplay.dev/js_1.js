
                const values = document.getElementById("values");
const container = document.getElementById("container");

values.addEventListener("change", (evt) => {
  container.style.placeItems = evt.target.value;
});

            