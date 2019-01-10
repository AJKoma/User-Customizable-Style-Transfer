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
    });

    // Choose
    $('#btn-choose').click(function() {
        $.ajax({
            type: 'POST',
            url: '/choose',
            data: $('.selected').attr("src"),

            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                console.log(data);
                alert("The style is ready, Upload and transfer now!");
            },
        });
    });

    

    $('.popup').magnificPopup({

        delegate: 'a',
		type: 'image',
		tLoading: 'Loading image #%curr%...',
		mainClass: 'mfp-img-mobile',
		gallery: {
			enabled: true,
			navigateByImgClick: true,
			preload: [0,1] // Will preload 0 - before current, and 1 after the current image
		},
    });
    
    // Profile
    $('#btn-editPwd').click(function() {
        $.ajax({
            url: '/editPwd',
            data: $('#editPwd').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
        
    // Profile
    // $('#btn-profile').click(function() {
    //     $.ajax({
    //         url: '/profile',
    //         dataType: 'json',
    //         type: 'GET',
    //         success: function(result) {
    //             console.log(result);
    //         },
    //         error: function(error) {
    //             console.log(error);
    //         }
    //     });
    // });

});

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

// /* Overlay Nav */
// function openNav() {
//     document.getElementById("myNav").style.display = "block";
// };
  
// function closeNav() {
//     document.getElementById("myNav").style.display = "none";
// };

