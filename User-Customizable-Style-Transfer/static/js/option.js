const baseUri = "https://localhost:5001/api";
const styleUri = "/Style/";
const apiUri = baseUri + styleUri;

console.log(apiUri)
var artistall = new Array();
var data = new Array();



var jqxhr = $.getJSON(apiUri,function(json){
    console.log("success");
    console.log(JSON.stringify(json));   
    console.log(json[0]);
    console.log(typeof(json));
    data = json;
    console.log(data);
    for (let index=0; index< json.length; index++) {
        console.log(json[index].id);
        console.log(json[index].artist);
        console.log(json[index].filepath);
        console.log(json[index].style)
        var img = document.createElement('img');
    
        let imgID   = json[index].id;
        let imgArtist = json[index].artist;
        let imgStyle = json[index].style;
        let imglink = apiUri + imgID + "/pic"
        let imginfolink = apiUri + imgID +"/info"

        var gallerycontainer = document.getElementById("gallery");
        var img = document.createElement('img');
        img.src = imglink;
        gallerycontainer.appendChild(img);    


        

        if (String(artistall).indexOf(json[index].artist) == -1)   {
            artistall[artistall.length] = (String(json[index].artist));
            let artistoption = document.createElement('option');
            artistoption.text = (json[index].artist);
            var artist_select=document.getElementById("artist-select");
            artist_select.add(artistoption);
            console.log(artistall);

        };

    };
        
});




$(document).ready(function () {    
    
    $('#gallery img').click(function () {
        //alert('selected');
        $('#gallery img').removeClass('selected');
        $(this).addClass('selected');
    });


    $('#artist-select').change(function () {
        let data_selected = new Array();
        var text = $('option:selected', this).text(); //to get selected text
        //alert(text)


        for (let index=0; index< data.length; index++) {
            let imgArtist = data[index].artist;
            if (text == imgArtist) {
                data_selected[data_selected.length] = data[index];                
            };
            if (text == "All"){
                data_selected = data;                
            };
        };

        console.log(data_selected);

        $('.selectionclear').remove();
        $('#gallery img').addClass('selectionclear');
        $('.selectionclear').remove();

        for (let index=0; index< data_selected.length; index++) {
            var img_selected = document.createElement('img');
            let imgID_selected   = data_selected[index].id;
            let imgArtist_selected = data_selected[index].artist;
            let imgStyle_selected = data_selected[index].style;
            let imglink_selected = apiUri + imgID_selected + "/pic"
            let imginfolink_selected = apiUri + imgID_selected +"/info"
            var gallerycontainer_selected = document.getElementById("gallery");
            img_selected.src = imglink_selected;
            gallerycontainer_selected.appendChild(img_selected); 
        };
        $('#gallery img').addClass('selectionclear');

        $('#gallery img').click(function () {
            //alert('selected');
            $('#gallery img').removeClass('selected');
            $(this).addClass('selected');
        });

        
    });

   










});     
        
        
 
        