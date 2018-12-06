$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-transfer').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Upload Style Preview
    function readSURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#stylePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#stylePreview').hide();
                $('#stylePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#styleUpload").change(function () {
        $('.style-section').show();
        $('#btn-confirm').show();
        readSURL(this);
    });

    // Customize
    $('#btn-confirm').click(function () {
        var form_data = new FormData($('#upload-style')[0]);

        // Show loading animation
        $(this).hide();
        $('#L2').show();

        // Make transfer by calling api /customize
        $.ajax({
            type: 'POST',
            url: '/customize',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('#L2').hide();
                console.log(data);
                alert("Your own style is ready, Upload and transfer now!");
            },
        });
    });

    // Transfer
    $('#btn-transfer').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('#L1').show();

        // Make transfer by calling api /transfer
        $.ajax({
            type: 'POST',
            url: '/transfer',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('#L1').hide();
                $('#result').fadeIn(600);
                //$('#result').text(' Result:  ' + data);
                //console.log('Success!');
                console.log("Image ready!");
                
                var img = document.createElement('img');
                img.src = data;
                img.style = "width: 280px; height: 210px border: 1px solid #F8F8F8;"
                document.getElementById("result").appendChild(img);
            },
        });
    });

    $('#gallery img').click(function () {
        //alert("select");
    $('#gallery img').removeClass('selected');
    $(this).addClass('selected');
    //var selectedimg = document.getElementsByClassName('selected');
    var imgsrc=$(this).attr('src');  
    console.log(imgsrc);
    alert(imgsrc);

    });

});

// /* Overlay Nav */
// function openNav() {
//     document.getElementById("myNav").style.display = "block";
// };
  
// function closeNav() {
//     document.getElementById("myNav").style.display = "none";
// };

