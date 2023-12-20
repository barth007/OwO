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
                if(response.liked_by_user===true){
                    $('.like-icon').addClass('text-blue-700')
                }else{
                    $('.like-icon').removeClass('text-blue-700')
                }
                // Fix the typo in accessing the response property
                like=$('#like-count').text(response.likes_count)
                parseInt(like)
            },
            error: function(response) {
                console.log("failed ", response);
            }
        });
    });

    $('.comment-form').submit(function (e) {
        e.preventDefault();
    
        // Serialize the form data
        const formData = $(this).serialize();
    
        const blog_id = $('#comment-btn').val();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        const url = $(this).attr('action');
    
        $.ajax({
            method: "POST",
            url: url,
            headers: { 'X-CSRFToken': token },
            data: formData,
            success: function (response) {
                // Handle success, e.g., update UI
                console.log(response);
                $('.comment').text(response.content);
                $('.author').text(response.author);
                $('.created-at').text(response.created_at);
                $('.success-message').text('Comment added successfully').show();
    
                // Clear form inputs using .find()
                $('.comment-form').find('input, textarea').val('');
            },
            error: function (response) {
                console.log("failed ", response);
            }
        });
    });
    
});

   