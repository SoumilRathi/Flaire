
                outer.style.width = outer.style.height = "165px";

w.onchange = w.oninput = () => {
  outer.style.width = `${w.value}px`;
  wf.textContent = `width: ${w.value}`;
};
h.onchange = h.oninput = () => {
  outer.style.height = `${h.value}px`;
  hf.textContent = `height: ${h.value}`;
};

            