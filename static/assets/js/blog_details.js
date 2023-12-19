$(document).ready(function(){
    $('.like-form').submit(function(e) {
        e.preventDefault();
        const blog_id = $('.like-btn').val();
        
        // Fix the name of the CSRF token input field
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const url = $(this).attr('action');

        $.ajax({
            method: "POST",
            url: url,
            headers: {'X-CSRFToken': token},  // Fix the CSRF token header
            data: {
                'blog_id': blog_id
            },
            success: function(response) {
                // Fix the typo in accessing the response property
                $('#like-count').text(response.likes_count);
            },
            error: function(response) {
                console.log("failed ", response);
            }
        });
    });
});
