let country_info;

let country_border = [];
let true_border = [];

let canvas;

let ctx;

let image;

async function fetch_country() {
    let request_index = await fetch('/api/v1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "random"
        }),
    });

    index = await request_index.json();

    let request_data = await fetch('/api/v1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "fetch",
            index: index
        }),
    });

    country_info = await request_data.json();
}

async function compareCountry() {
    let map_scaling = [20037508.342789244, 10018754.171394622]
    let modified_border = country_border.map(function (e) {
        return [2 * (e[0] - 0.5) * map_scaling[0], - 2 * (e[1] - 0.5) * map_scaling[1]]
    })

    let request_data = await fetch('/api/v1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "compare",
            geometry: modified_border,
            index: index
        }),
    });
    let score = await request_data.json()
    for (i of document.getElementsByClassName("score")) {
        i.innerText = Math.round(score * 10000) / 100
    }
    document.getElementById("score viewer").style.visibility = "visible";

    let second_request = await fetch('/api/v1', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            type: "border",
            index: index
        }),
    });
    //console.log(await second_request.text())
    let border = await second_request.json()
    true_border = border.map(function (e) {
        return [e[0] / map_scaling[0] / 2 + 0.5, - e[1] / map_scaling[1] / 2 + 0.5]
    })

    canvasManagement()
}

function set_country_info() {
    for (i of document.getElementsByClassName("country")) {
        i.innerText = country_info.name;
    }
    for (i of document.getElementsByClassName("iso")) {
        i.innerText = country_info.iso;
    }
}

function printMousePos(event) {
    let x = event.pageX - event.target.offsetLeft;
    let y = event.pageY - event.target.offsetTop;
    x /= event.target.width;
    y /= event.target.height;

    if (event.button == 0) {
        country_border.push([x, y]);
    } else if (event.button == 2) {
        country_border.pop()
    }

    canvasManagement()
}

window.onload = function () {
    document.getElementById("map").addEventListener('click', event => printMousePos(event));
    document.getElementById("map").addEventListener('contextmenu', event => { event.preventDefault(); printMousePos(event); return false; });

    window.addEventListener('resize', function (e) { canvasManagement() })

    fetch_country().then(e => set_country_info());

    image = document.getElementById("source_map")

    canvas = document.getElementById("map");

    ctx = canvas.getContext('2d');

    country_border = [];
    true_border = [];

    canvasManagement()
}

function canvasManagement() {
    canvas.width = canvas.parentElement.clientWidth
    canvas.height = canvas.parentElement.clientWidth * image.height / image.width
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.drawImage(image, 0, 0, canvas.width, canvas.height)

    try {
        ctx.beginPath();
        ctx.moveTo(country_border[0][0] * canvas.width, country_border[0][1] * canvas.height)
        for (i of country_border) {
            ctx.lineTo(i[0] * canvas.width, i[1] * canvas.height)
        }
        ctx.fillStyle = '#00FF0040'
        ctx.lineWidth = 1
        ctx.stroke();
        ctx.fill()
    } catch (e) { console.log("error drawing sketch country") }
    console.log("fail")
    try {
        ctx.beginPath();
        ctx.moveTo(true_border[0][0] * canvas.width, true_border[0][1] * canvas.height)
        for (i of true_border) {
            ctx.lineTo(i[0] * canvas.width, i[1] * canvas.height)
        }
        ctx.fillStyle = '#0000FF40'
        ctx.lineWidth = 1
        ctx.stroke();
        ctx.fill()
    } catch (e) { console.log("error drawing true country") }


}

