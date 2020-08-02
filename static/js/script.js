$(document).ready(function() {
    //fade ins for the top
    var element = $("#first-container-text-container");
    element.hide();
    element.delay( 300 ).fadeIn( 1000 );

    var element2 = $("#first-container-image");
    element2.hide();
    element2.delay( 500 ).fadeIn( 1500 );

  
    //second fade ins
    $(window).scroll( function(){

        $('.first-analysis-title').each( function(){
            var bottom_of_element = $(this).offset().top + $(this).outerHeight();
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            if( bottom_of_window > bottom_of_element ){
                $(this).animate({'opacity':'1'},1000);

            }
        });

        $('.first-analysis-image').each( function(){     
            var bottom_of_element = $(this).offset().top;
            var bottom_of_window = $(window).scrollTop() + ($(window).height()/(4/3));
            if( bottom_of_window > bottom_of_element ){
                $(this).animate({'opacity':'1'},1000);

            }
        });
    });
});

