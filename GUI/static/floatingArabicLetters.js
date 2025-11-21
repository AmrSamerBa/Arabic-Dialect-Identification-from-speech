// Random floating arabic letters
const colors = ["#1d2228","#fb8122"];
const letters = ["إزيك","شحالك","كيف حالك","شلونك","وشراك","الأخبار","زول","زلمة","رجل","ريال"];

const numText = 12;
const texts = [];

for (let i = 0; i < numText; i++) {
    let text = document.createElement("div");
    text.innerText = letters[Math.floor(Math.random() * letters.length)];
    text.classList.add("text");
    text.style.left = `${Math.floor(Math.random() * 90)}vw`;
    text.style.top = `${Math.floor(Math.random() * 500)}px`;
    text.style.fontSize = `${(Math.random()*(5 - 3 + 1)) + 3}em`;
    text.style.opacity = ((Math.random()*(0.9 - 0.6)) + 0.6);
    // text.style.color = colors[Math.floor(Math.random()*0.6)];
    text.style.color = colors[Math.floor(Math.random()*2)];

    
    texts.push(text);
    document.getElementById("floatingArabicLetters").appendChild(text);
}

// Keyframes
texts.forEach((el, i, ra) => {
let to = {
    x: Math.random() * (i % 2 === 0 ? -5 : 5),
    y: Math.random() * 6
};

let anim = el.animate(
    [
        { transform: "translate(0, 0)" },
        { transform: `translate(${to.x}rem, ${to.y}rem)` }
    ],
    {
        duration: (Math.random() + 1) * 3000, // random duration
        direction: "alternate",
        fill: "both",
        iterations: Infinity,
        easing: "ease-in-out"
    }
);
});