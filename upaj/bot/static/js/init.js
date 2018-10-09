var slider = $('#chat-pane').slideReveal({
    trigger: $('.trigger'),
    width: '90%',
    push: false,
    position: 'right',
    overlay: true,
    overlayColor: 'rgba(0,0,0,0.5)',
});

// Materialize JS

(function($){
  $(function(){

    $('.sidenav').sidenav();
    $('.parallax').parallax();

  }); // end of document ready
})(jQuery); // end of jQuery name space

$('.message-submit').click(function(event){
    event.preventDefault();

    insertMessage();
});


// Messaging Interactions for Chat Pane

var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {

});

$messages.mCustomScrollbar();
setTimeout(function() {
  fakeMessage();
}, 100);

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
    query = $('textarea[name="message-input"]').val();
    csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

    $.ajax({
        type: 'POST',
        url: '/response',
        data: {
            'query' : query,
            'csrfmiddlewaretoken': csrfmiddlewaretoken,
        },
        success: function(data){
            console.log("success");
            console.log(data);

            $('.message.loading').remove();
            $('<div class="message new"><figure class="avatar"><img src="chathead.png" /></figure>' + data + '</div>').appendTo($('.mCSB_container')).addClass('new');
            setDate();
            updateScrollbar();
            i++;
        },
        error: function(data, err){

        }
    });

  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
    fakeMessage();
}

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})

function fakeMessage() {
  if ($('.message-input').val() != '') {
    return false;
  }
  $('<div class="message loading new"><figure class="avatar"><img src="chathead.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();
}


