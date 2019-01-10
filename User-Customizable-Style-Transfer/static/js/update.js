$(document).ready(function () {

    $('.form').find('input, textarea').on('keyup blur focus', function (e) {
        var $this = $(this),
        label = $this.prev('label');
        
        if (e.type === 'keyup') {
            if ($this.val() === '') {
                label.removeClass('active highlight');
            } else {
                label.addClass('active highlight');
            }
        } else if (e.type === 'blur') {
            if( $this.val() === '' ) {
                label.removeClass('active highlight'); 
            } else {
                label.removeClass('highlight');   
            }   
        } else if (e.type === 'focus') {
            if( $this.val() === '' ) {
                label.removeClass('highlight'); 
            }
            else if( $this.val() !== '' ) {
                label.addClass('highlight');
            }
        }
    });

    $('#btn-update').click(function() {
        $.ajax({
            url: '/update',
            data: $('#update').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });

});