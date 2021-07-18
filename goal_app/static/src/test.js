//const fetch = require("node-fetch");

const url = 'https://zenquotes.io/api/random';
fetch(url)
    .then((response) => response.json())
    .then(function(data) {
        let quote = data[0]["q"];
        let author = data[0]["a"];
        let htmlquote = data[0]["h"];
        console.log(htmlquote);
    })
