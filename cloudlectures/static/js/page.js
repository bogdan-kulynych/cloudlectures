$(document).ready(function() {
    $('#unit0').addClass('in')
               .find('.lecture0').addClass('active');

    var youtube = $('#unit0 .lecture0 a').attr('data-video-url');
    set_video(youtube);

    function set_video(url) {
        var vid = youtube_parser(url);

        setTimeout(function() {
            $vc = $('#video-container');
            $vc.empty();
            $vc.append($('<div></div>'));
            $vc.find('div').attr('id', 'dummy');
            player = new YT.Player('dummy',
            {
                videoId: vid,
                playerVars: { 'autoplay': 1, 'controls': 1 },
                events: {
                 // 'onStateChange': onPlayerStateChange
                }
            });
        }, 100);
    }

    $('.video-toggle').click(function(e) {
        e.preventDefault();

        var $this = $(this);

        $('#units-list li').removeClass('active');
        $this.closest('li').addClass('active');

        var title = $this.closest('.unit').text();
        var description = $this.attr('data-description');
        
        $('#video-title').text(title);
        $('#video-description').text(description);

        var url = $this.attr('data-video-url');
        set_video(url);
    });
});