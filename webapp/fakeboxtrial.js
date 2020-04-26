var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');

var app = express();
app.use(express.static(__dirname+'/views'));

app.use(bodyParser.urlencoded({ extended: true }));

const request = require('request');
const https = require("https");

const admin = require('firebase-admin');
const serviceAccount = require('./hacknow-275310-firebase-adminsdk-kr51l-b520871a54.json')

admin.initializeApp({
    credential: admin.credential.applicationDefault()
});

const Firestore = require('@google-cloud/firestore');

const firestore = new Firestore({
    project_id: 'hacknow-275310',
    keyFilename: './hacknow-275310-firebase-adminsdk-kr51l-b520871a54.json',
    timestampsInSnapshots: true,
});

const db = admin.firestore();


var getTimeStamp = () => {
    var today = new Date()
    return today.getFullYear()+"-"+(today.getMonth()+1)+"-"+today.getDate() + " " + today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();  
}

var analyzeCallBack = (pageContent, req, resp) => {
    request.post(
        'http://localhost:8080/fakebox/check',
        {
        json: {
            url: req.body.url,
            content: pageContent
        }
        },
        (error, res, body) => {
        if (error) {
            console.error(error, "test")
            return
        }
        console.log(`statusCode: ${res.statusCode}`)
        resp.sendFile(path.join(__dirname+'/views/submission.html'));
        console.log(body)
        console.log(body.content.score)
        var temp = 1 - body.content.score
        console.log(req.body.url)
        const urlData = {
            url: req.body.url,
            probToBeFake: temp
        }
        console.log(getTimeStamp())
        firestore.collection('links').doc(getTimeStamp().toString()).set(urlData).then(()=> {console.log("added new link to db")})
        }
    )
};

app.post('/submit', function (req, resp) {
    request.post(
        'https://us-central1-hacknow-275310.cloudfunctions.net/loadAddress',
        {
            json: {
                url: req.body.url,
            }
        }, 
        (error, res, body) => {
            if (error) {
            console.error(error, "test")
            return
            }
            console.log(`statusCode: ${res.statusCode}`)
            console.log(body)
            analyzeCallBack(body, req, resp)
        }
    );
})

app.get('/admin', function (req, res) {
    res.sendFile(path.join(__dirname+'/views/admin.html'));
})

app.get('/leaderboard', function (req, res) {
    res.sendFile(path.join(__dirname+'/views/leaderboard.html'));
})

app.get('/analysis', function (req, res) {
    res.sendFile(path.join(__dirname+'/views/submission.html'));
})

app.get('/', function (req, res){
    res.sendFile(path.join(__dirname+'/views/index.html'));
});


app.listen(3000, function () {
    console.log('Example app listening on port 3000!');
});

