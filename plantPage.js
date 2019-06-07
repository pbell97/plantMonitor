var address = "http://10.0.0.131";
var latestFolder = "";

function makeGet(url, callbackFunction){
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onload = function () {
        callbackFunction(JSON.parse(xhr.responseText));
    };
    xhr.send();
}

function makePost(url, callbackFunction){
    var that = this;
    $.ajax({
        url: that.url,
        type: 'POST',
        data:{},
        async: true,
        success: function (data) {
            console.log("Success. Got " + data + " from server ");
            that.callbackFunction(data)
        }
    });
}


function updateFolders(folderNames){
    var list = document.getElementById("foldersList");

    var child = list.lastElementChild;  
    while (child) { 
        list.removeChild(child); 
        child = list.lastElementChild;
    }

    for (var i = 0; i < folderNames.length; i++){
        var newListItem = document.createElement('li');
        var htmlText = "<li onclick=getFiles(this)>" + folderNames[i] + "</li>";
        newListItem.innerHTML = htmlText;
        // newListItem.innerText = folderNames[i];
        list.appendChild(newListItem);
    }
}

function getFolders(){
    makeGet(address + '/existingFolders/', updateFolders);
}


function updateFiles(fileNames){
    var list = document.getElementById("filesList");

    var child = list.lastElementChild;  
    while (child) { 
        list.removeChild(child); 
        child = list.lastElementChild;
    }

    for (var i = 0; i < fileNames.length; i++){
        var newListItem = document.createElement('li');
        var htmlText = "<li onclick=getFile(this)>" + fileNames[i] + "</li>";
        newListItem.innerHTML = htmlText;
        // newListItem.innerText = fileNames[i];
        list.appendChild(newListItem);
    }

}

function getFiles(folder){
    folder = folder.innerText;
    latestFolder = folder;
    makeGet(address + "/existingFiles/" + folder, updateFiles);
}

function getFile(file){
    file = file.innerText;
    var src = address + "/getPicture/" + latestFolder + "/" + file, updatePicture;
    document.getElementById('currentViewPicture').src = src;
}

function getCurrentView(){
    var src = address + "/currentView/";
    document.getElementById('currentViewPicture').src = src;
}

function startServer(){
    makeGet(address + "/startCamera/", function(){});
    setTimeout(getStatus, 1000);
}

function stopServer(){
    makeGet(address + "/stopCamera/", function(){});
    setTimeout(getStatus, 7000);
}


function getStatus(){
    makeGet(address + "/cameraIsRunning/", updateStatus);
}

function updateStatus(status){
    var dot = document.getElementById('statusCircle');
    var statusEl = document.getElementById('statusLabel');
    if (status == true){
        dot.style.backgroundColor = "green";
        statusEl.innerText = "On";
    } else {
        dot.style.backgroundColor = "red";
        statusEl.innerText = "Off";
    }
}

// Get folders
makeGet(address + '/existingFolders/', updateFolders);
getCurrentView();
getStatus();