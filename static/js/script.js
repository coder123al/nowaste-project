$(document).ready(function() {
    //fade ins for the top
    var firstText = $("#first-container-text-container");
    firstText.hide();
    firstText.delay( 300 ).fadeIn( 1000 );

    var firstImage = $("#first-container-image");
    firstImage.hide();
    firstImage.delay( 500 ).fadeIn( 1500 );

  
    //second fade ins
    $(window).scroll( function(){
        $('.text').each( function(){
            var bottom_of_element = $(this).offset().top + $(this).outerHeight()*.75;
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            if( bottom_of_window > bottom_of_element ){
                $(this).css('opacity', '1');
            }
            else{
                $(this).css('opacity', '0');
            }
        });

        $('.first-analysis-title').each( function(){
            var bottom_of_element = $(this).offset().top + $(this).outerHeight();
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            if( bottom_of_window > bottom_of_element ){
                $(this).css('opacity', '1');
            }
            else{
                $(this).css('opacity', '0');
            }
        });

        $('.first-analysis-image').each( function(){     
            var bottom_of_element = $(this).offset().top;
            var bottom_of_window = $(window).scrollTop() + ($(window).height()/(4/3));
            if( bottom_of_window > bottom_of_element ){
                $(this).css('opacity', '1');
            }
            else{
                $(this).css('opacity','0')
            }
        });
    });
});

