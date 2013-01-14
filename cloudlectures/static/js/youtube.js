// Gets video id from youtube link
// http://stackoverflow.com/questions/3452546/javascript-regex-how-to-get-youtube-video-id-from-url
function youtube_parser(url){
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=)([^#\&\?]*).*/;
    var match = url.match(regExp);
    if (match && match[2].length === 11) {
        return match[2];
    } else {
        return null;
    }
}
