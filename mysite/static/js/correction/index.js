//옵션 선택 안했을 시 에러 문구 띄우기, 제출되면 로딩중 뜨기
$('#correctionForm').on('submit',function(e){
    var opt1_state = $('#option1').is(':checked'); //요소가 체크되어 있는 상태를 선택
    var opt2_state = $('#option2').is(':checked');

    function showError(element) {
        e.preventDefault();
        $(element).css('visibility', 'visible');
        $(element).css('opacity', '1');
        setTimeout(function() {
            $(element).css('visibility', 'hidden');
            $(element).css('opacity', '0');
        }, 2000);
    }

    if(!opt1_state && !opt2_state && !($('#jasoseo').val().trim().length < 1)){
        showError('#only-option-error');
    }
    else if (!(!opt1_state && !opt2_state) && ($('#jasoseo').val().trim().length < 1)) {
        showError('#jasoseo-error');
    }
    else if (!opt1_state && !opt2_state && ($('#jasoseo').val().trim().length < 1)) {
        showError('#jasoseo-error');
        showError('#option-error');
    }
    //correct제출될 때 로딩중 뜨기
    else{
        $('#correctButton').prop('disabled', true);
        $('.loading-icon').show();
    }
});

// 소제목 체크하면 문단구분 알림
$('#option2').on('click', function() {
    if ($(this).prop('checked')) {
        $('#mini-title-comment').css('visibility', 'visible');
        $('#mini-title-comment').css('opacity', '1');
        setTimeout(function() {
            $('#mini-title-comment').css('visibility', 'hidden');
            $('#mini-title-comment').css('opacity', '0');
        }, 3000);
    };
});

// 초안 글자수 반영
window.onload = function() {
    $('#counter').html($('#jasoseo').val().length + ' / 3000');
    adjustTextareaHeight();
}

// 글자 수 제한
//'keyup' 이벤트 대신 'input' 이벤트 사용-> 키보드 입력 뿐 아니라 마우스로 붙여넣기 등의 다른 방식으로 입력된 텍스트도 감지함
$(document).ready(function() {
    //로딩중 무조건 숨기기
    $('#correctButton').prop('disabled', false);
    $('.loading-icon').hide();

    $('#jasoseo').on('input', function(e){
        var content = $(this).val();
        if (content.length > 3000) {
            // 초과된 부분 제거
            $(this).val(content.substring(0, 3000));
            // textarea 길이 조절
            adjustTextareaHeight();
        }
        // 현재 글자 수 표시
        $('#counter').html($(this).val().length + ' / 3000');
    });
});

//뒤로가기 해서 페이지가 캐시에서 로드 될 때에도 실행됨
$(window).on('pageshow', function() {
    //로딩중 무조건 숨기기
    $('.loading-icon').hide();
    $('#correctButton').prop('disabled', false);
});


// input이 변하거나, 브라우저 크기가 변할 때 textarea 조절
var textarea = document.getElementById('jasoseo');
var hidden_textarea = document.getElementById('hidden_textarea');
var windowHeight = $(window).height();
var paddingTop = parseInt($('#jasoseo').css('padding-top'));
var paddingBottom = parseInt($('#jasoseo').css('padding-bottom'));
var originHeight = windowHeight * 0.6 - paddingTop - paddingBottom;

function adjustTextareaHeight() {
    hidden_textarea.innerHTML = textarea.value;
    console.log(hidden_textarea.scrollHeight - 90, originHeight)
    
    if (hidden_textarea.scrollHeight - 90 < originHeight) {
        textarea.style.height = originHeight + 'px';
    } else {
        textarea.style.height = hidden_textarea.scrollHeight - paddingBottom - paddingTop + 'px';
    }
}

textarea.addEventListener('input', adjustTextareaHeight);

$(window).on('resize', function() {
    var newWindow = $(window).height();
    var newOrigin = newWindow * 0.6 - paddingTop - paddingBottom;
    console.log(hidden_textarea.scrollHeight, newOrigin)
    
    if (hidden_textarea.scrollHeight - 90 < newOrigin) {
        $('#jasoseo').css('height', newOrigin);
    } else {
        $('#jasoseo').css('height', hidden_textarea.scrollHeight - paddingBottom - paddingTop);
    }
});


// 클립보드 복사
var clipboard = new ClipboardJS('#icon_copy');
var alarm = document.querySelector('#alarm_copy')
var span = document.createElement('span');

clipboard.on('success', function(e) {

    span.innerHTML = 'Copied!';
    alarm.appendChild(span);
    setTimeout(function () {span.innerHTML = "";} , 1500);

    e.clearSelection();
});


// 초기화(텍스트, 글자수, textarea 길이)
$('#icon_reset').click(function(){
    var windowHeight = $(window).height();
    var paddingTop = parseInt($('#jasoseo').css('padding-top'));
    var paddingBottom = parseInt($('#jasoseo').css('padding-bottom'));
    var resetHeight = windowHeight * 0.6 - paddingTop - paddingBottom;
    $('#jasoseo').val('').trigger('input'); //강제로 input이벤트 발생시켜야 글자수 반영됨
    $('#jasoseo').css('height', resetHeight); //textarea 세로 길이 초기화
});

// 맨위로 이동
$("#top").on("click",function(){
    window.scroll({top: 0, behavior: 'smooth'});
});
// 맨아래로 이동
$("#bottom").on("click",function(){
    window.scroll({top: document.documentElement.scrollHeight, behavior: 'smooth'});
});