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
                
                const like=$('#like-count').text(response.likes_count)
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
    
                // Create a new comment element
                const commentDiv = $('<div class="d-flex mb-4 comment">');
                commentDiv.append('<div class="flex-shrink-0">');
                commentDiv.find('.flex-shrink-0').append('<img class="rounded-circle" src="https://dummyimage.com/50x50/ced4da/6c757d.jpg" alt="..." />');
                commentDiv.append('<div class="fs-6">');
                commentDiv.find('.fs-6').append('<div class="comment">');
                commentDiv.find('.comment').append('<span class="author">' + response.author + ':</span>');
                commentDiv.find('.comment').append('<span class="text-muted">' + response.content + '</span>');

                // Format the date in the desired format
                const formattedDate = new Date(response.created_at);
                const options = { hour: 'numeric', minute: 'numeric', year: 'numeric', month: 'short', day: 'numeric' };
                const formattedDateString = formattedDate.toLocaleDateString('en-US', options);

                commentDiv.find('.fs-6').append('<div class="small fst-italic text-muted created_at">' + formattedDateString + '</div>');

                // Append the new comment to the comments container
                $('#comments-container').prepend(commentDiv);

                
                // Clear form inputs using .find()
                $('.comment-form').find('input, textarea').val('');
            },
            error: function (response) {
                console.log("failed ", response);
            }
        });
    });
});
