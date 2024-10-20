const body = document.body;
const themeConstrat = document.getElementsByClassName('theme-contrast')
const themeGrey = document.getElementsByClassName('theme-grey');

function lightOn() {
    body.style.backgroundColor = 'white';
    body.style.color = 'black';
    for (var i = 0; i < themeConstrat.length; i++){themeConstrat[i].style.color = "black"; themeConstrat[i].style.fill = "black";}
    for (var i = 0; i < themeGrey.length; i++){themeGrey[i].style.color = "#5a5a5a"; themeGrey[i].style.fill = "#5a5a5a"}
}
function lightOff() {
    body.style.backgroundColor = 'black';
    body.style.color = 'white';
    for (var i = 0; i < themeConstrat.length; i++){themeConstrat[i].style.color = "white"; themeConstrat[i].style.fill = "white";}
    for (var i = 0; i < themeGrey.length; i++){themeGrey[i].style.color = "#e6e6e6"; themeGrey[i].style.fill = "#e6e6e6";}
}

function checkPrefExists() { return "theme" in localStorage;}
function checkPrefDark(){ return localStorage.getItem("theme") === "dark";}

if (checkPrefExists()){
    if(checkPrefDark()){lightOff();}
    else{lightOn();}   
}
else{
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){lightOff();}
    else{lightOn();}   
}

const colorButton = document.getElementById('colorSwitchButton');
colorButton.addEventListener('click', () => {
    if (body.style.backgroundColor === 'black') {
        localStorage.setItem("theme", "light");
        lightOn();
    } else {
        localStorage.setItem("theme", "dark");
        lightOff();
    }
});

const picture = document.getElementById('profile-picture');
picture.addEventListener('click', () => {window.location.href = '/'})

// var userLang = navigator.language || navigator.userLanguage;
// let isFrench = userLang.includes("fr");