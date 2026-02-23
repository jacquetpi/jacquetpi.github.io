const body = document.body;
const themeColor = document.getElementsByClassName('theme-color');
const themeContrast = document.getElementsByClassName('theme-contrast');
const themeGrey = document.getElementsByClassName('theme-grey');
const backgroundConstrat = document.getElementsByClassName('background-contrast');

function lightOn() {
    body.style.backgroundColor = 'white';
    for (var i = 0; i < themeColor.length; i++){themeColor[i].style.setProperty('color', 'white', 'important');};

    body.style.color = 'black';
    for (var i = 0; i < themeContrast.length; i++){themeContrast[i].style.setProperty('color', 'black'); themeContrast[i].style.setProperty('fill', 'black');};
    for (var i = 0; i < backgroundConstrat.length; i++){backgroundConstrat[i].style.setProperty('background-color', 'black', 'important');};

    for (var i = 0; i < themeGrey.length; i++){themeGrey[i].style.setProperty('color', '#5a5a5a'); themeGrey[i].style.setProperty('fill', '#5a5a5a');};
}

function lightOff() {
    body.style.backgroundColor = 'black';
    for (var i = 0; i < themeColor.length; i++){themeColor[i].style.setProperty('color', 'black', 'important');};

    body.style.color = 'white';
    for (var i = 0; i < themeContrast.length; i++){themeContrast[i].style.setProperty('color', 'white'); themeContrast[i].style.setProperty('fill', 'white');};
    for (var i = 0; i < backgroundConstrat.length; i++){backgroundConstrat[i].style.setProperty('background-color', 'white', 'important');};
    
    for (var i = 0; i < themeGrey.length; i++){themeGrey[i].style.setProperty('color', '#e6e6e6'); themeGrey[i].style.setProperty('fill', '#e6e6e6');};
}

function checkPrefExists() { return 'theme' in localStorage;}
function checkPrefDark(){ return localStorage.getItem('theme') === 'dark';}

if (checkPrefExists()){
    if(checkPrefDark()){lightOff();}
    else{lightOn();}   
}
else{
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){lightOff();}
    else{lightOn();}   
}

const colorButton = document.getElementById('colorSwitchButton');
if (colorButton) colorButton.addEventListener('click', () => {
    if (body.style.backgroundColor === 'black') {
        localStorage.setItem('theme', 'light');
        lightOn();
    } else {
        localStorage.setItem('theme', 'dark');
        lightOff();
    }
});

const picture = document.getElementById('profile-picture');
if (picture) picture.addEventListener('click', () => {window.location.href = '/'})

// var userLang = navigator.language || navigator.userLanguage;
// let isFrench = userLang.includes('fr');