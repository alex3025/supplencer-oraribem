function showPassword() {
    var input = document.getElementById("password");

    if (input.type === "password") {
        input.type = "text";
    } else {
        input.type = "password";
    }
}

function onBoxChange() {
    var a = new Date();
    var days = new Array(7);
    days[0] = "Sunday";
    days[1] = "Monday";
    days[2] = "Tuesday";
    days[3] = "Wednesday";
    days[4] = "Thursday";
    days[5] = "Friday";
    days[6] = "Saturday";
    var r = days[a.getDay()];

    var e = document.getElementById('day');
    var day = e.options[e.selectedIndex].value;

    var se = document.getElementById('search-errors');

    if (day != r) {
        se.style.display = 'block';
    } else {
        se.style.display = 'none';
    }
}