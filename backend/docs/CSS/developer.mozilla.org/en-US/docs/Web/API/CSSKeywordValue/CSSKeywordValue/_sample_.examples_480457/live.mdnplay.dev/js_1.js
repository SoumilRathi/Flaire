
                const keyword = new CSSKeywordValue("initial");
const myElement = document.getElementById("myElement").attributeStyleMap;
myElement.set("display", keyword);

console.log(myElement.get("display").value); // 'initial'
console.dir(keyword);

            