

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
        $('#head_left').find('.loading-icon').show();
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


// input이 변하거나, 브라우저 크기가 변할 때 textarea 조절
var windowHeight = $(window).height();
var paddingTop = parseInt($('#jasoseo').css('padding-top'));
var paddingBottom = parseInt($('#jasoseo').css('padding-bottom'));
var originHeight = windowHeight * 0.6 - paddingTop - paddingBottom;
// 1. 왼쪽
var textarea_left = document.getElementById('jasoseo');
var hidden_textarea_left = document.getElementById('hidden_textarea_left');

function adjustTextareaHeight_left() {
    hidden_textarea_left.innerHTML = textarea_left.value;

    if (hidden_textarea_left.scrollHeight - 90 < originHeight) {
        textarea_left.style.height = originHeight + 'px';
    } else {
        textarea_left.style.height = hidden_textarea_left.scrollHeight - paddingBottom - paddingTop + 'px';
    }
}

textarea_left.addEventListener('input', adjustTextareaHeight_left);
textarea_left.addEventListener('input', adjustCoachingDiv);

$(window).on('resize', function() {
    var newWindow = $(window).height();
    var newOrigin = newWindow * 0.6 - paddingTop - paddingBottom;
    
    if (hidden_textarea_left.scrollHeight - 90 < newOrigin) {
        $('#jasoseo').css('height', newOrigin);
    } else {
        $('#jasoseo').css('height', hidden_textarea_left.scrollHeight - paddingBottom - paddingTop);
    }
    adjustCoachingDiv();
});
// 2. 오른쪽
var textarea_right = document.getElementById('myText');
var viewMode = document.getElementById('myTextView');
var hidden_textarea_right = document.getElementById('hidden_textarea_right');

function adjustTextareaHeight_right() {
    //console.log(textarea_right.value);
    hidden_textarea_right.innerHTML = textarea_right.value;
    //console.log(hidden_textarea_right.value);
    //console.log(hidden_textarea_right.scrollHeight - 90, originHeight)
    if (hidden_textarea_right.scrollHeight - 90 < originHeight) {
        textarea_right.style.height = originHeight + 'px';
        $('#myTextView').css('height', originHeight);
    } else {
        textarea_right.style.height = hidden_textarea_right.scrollHeight - paddingBottom - paddingTop + 'px';
        $('#myTextView').css('height','');
    }
}

textarea_right.addEventListener('input', adjustTextareaHeight_right);
textarea_right.addEventListener('input', adjustCoachingDiv);

$(window).on('resize', function() {
    var newWindow = $(window).height();
    var newOrigin = newWindow * 0.6 - paddingTop - paddingBottom;
    
    if (hidden_textarea_right.scrollHeight - 90 < newOrigin) {
        $('#myText').css('height', newOrigin);
        $('#myTextView').css('height', newOrigin);
    } else {
        $('#myText').css('height', hidden_textarea_right.scrollHeight - paddingBottom - paddingTop);
        $('#myTextView').css('height','');
    }
    adjustCoachingDiv();
});

// 페이지 처음 로드 시, textarea 길이 조절 + 아래 공간 주기
$(document).ready( function() {
    // 왼쪽 조절
    adjustTextareaHeight_left();
    // 오른쪽 조절
    adjustTextareaHeight_right();
    // 아래 공간
    adjustCoachingDiv();
    // 스크롤 맨 아래로
    window.scroll({top: document.documentElement.scrollHeight, behavior: 'smooth'});
});


// 맨위로 이동
$("#top").on("click",function(){
    window.scroll({top: 0, behavior: 'smooth'});
});
// 맨아래로 이동
$("#bottom").on("click",function(){
    window.scroll({top: document.documentElement.scrollHeight, behavior: 'smooth'});
});

// 왼쪽 클립보드 복사
var clipboardLeft = new ClipboardJS('#icon_copy_left');
var alarmLeft = document.querySelector('#alarm_copy_left')
var spanLeft = document.createElement('span_left');

clipboardLeft.on('success', function(e) {

    spanLeft.innerHTML = 'Copied!';
    alarmLeft.appendChild(spanLeft);
    setTimeout(function () {spanLeft.innerHTML = "";} , 1500);

    e.clearSelection();
});

// 왼쪽 초기화(텍스트, 글자수, textarea 길이)
$('#icon_reset_left').click(function(){
    var windowHeight = $(window).height();
    var paddingTop = parseInt($('#jasoseo').css('padding-top'));
    var paddingBottom = parseInt($('#jasoseo').css('padding-bottom'));
    var resetHeight = windowHeight * 0.6 - paddingTop - paddingBottom;
    $('#jasoseo').val('').trigger('input'); //강제로 input이벤트 발생시켜야 글자수 반영됨
    $('#jasoseo').css('height', resetHeight); //textarea 세로 길이 초기화
    adjustCoachingDiv(); // 코칭 위치 조절
});

// 오른쪽 클립보드 복사
var clipboardRight = new ClipboardJS('#icon_copy_right');
var alarmRight = document.querySelector('#alarm_copy_right')
var spanRight = document.createElement('span_right');

clipboardRight.on('success', function(e) {

    spanRight.innerHTML = 'Copied!';
    alarmRight.appendChild(spanRight);
    setTimeout(function () {spanRight.innerHTML = "";} , 1500);

    e.clearSelection();
});


//파일 다운로드기능: 서버로부터 파일을 직접 HTTP로 받는 방법 -> 자동 다운로드 됨
document.getElementById('downloadButton').addEventListener('click', function(){
    var text = document.getElementById('myText').value; //다운로드 받을 자소서

    // form을 생성하여 서버에 POST 요청을 보냄
    var form = document.createElement('form');
    form.method = 'POST';
    form.action = '/correction/download/';

    // CSRF 토큰을 추가
    var csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    //  hidden input 필드 추가
    var hiddenInput = document.createElement('input');
    hiddenInput.type = 'hidden';
    hiddenInput.name = 'text';
    hiddenInput.value = text;

    // hidden input 필드를 form에 추가하고, form을 document body에 추가
    form.appendChild(hiddenInput);
    document.body.appendChild(form);

    // form 제출(서버에 POST 요청 보냄)
    form.submit();

    // form을 document body에서 제거
    document.body.removeChild(form);
});
