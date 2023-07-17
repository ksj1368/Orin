// 되돌아가면 메뉴바가 안 보이게 하는 이벤트
window.onpageshow= function(event) {
    if (event.persisted) {
        $("#toggle").prop('checked', false);
    }
    else {}
}

// 다른 곳을 눌러도 메뉴바가 사라지게 하는 이벤트
$(document).on('click', 'body', function(event) {
    if (!$(event.target).hasClass('js_check')) {
        $("#toggle").prop('checked', false);
    }
});