
//mypage 저장 모달창에서 카테고리 추가하기 버튼 구현
function addCategory(){
    var select = $("#categoryInput");
    var exists = false;
    var new_category = prompt("추가할 카테고리 이름을 입력해주세요.");

    if(new_category===null){
        //취소누르면
        return;    
    }else if (new_category.trim().length===0){
        //한 글자 이상 누르지 않으면
        alert("한 글자 이상 입력해주세요");
        return;
    }
    
    //이미 존재하는 카테고리라면
    select.find('option').each(function(){  //배열은 forEach, jquery객체는 each(index,각 객체) 
        if(this.value.trim() === new_category){
            alert('이미 존재하는 카테고리 입니다.');
            exists = true;
            return false;   //each 순회만 중단 함. 전체 함수 종료를 위해서 exists 생성
        }
    })
    
    if(exists){
        return; //이미 존재하는 카테고리라면 함수 종료
    }

    //새로운 카테고리 저장 및 띄우기
    $.ajax({
        url : '/correction/correct/categories/',
        type : 'POST',
        contentType : 'application/json',
        data : JSON.stringify({
            category_name : new_category 
        }),
        headers: {
            'X-CSRFToken': csrfToken
        },
        success : function(data){
            //성공적으로 카테고리 생성함
            var option = $('<option>', {value : data.category_name, text : data.category_name});
            select.append(option);
        },
        error : function(jqXHR, textStatus, errorThrown){
            alert("카테고리 추가에 실패했습니다. 다시 시도해주세요.");
        }
    })
}

//mypage에 최종 저장 로직
function save(content){

    var title = $('#titleInput').val();
    var category = $('#categoryInput').val();   //사용자가 선택한 option의 value가 곧 select 태그의 value

    if (title.trim() === '') {
        alert('파일 제목을 입력해주세요.');
        return; // 입력이 없으면 함수 종료
    }
    if (category === '') {
        alert('카테고리를 선택해주세요.');
        return; // 카테고리가 선택되지 않았으면 함수 종료
    }            

    $.ajax({
        url: '/correction/correct/savejasoseo/',
        type : 'POST',
        data : { //ajax 의 data기본 옵션은 application/x-www-form-urlencoded
            'title' : title,
            'category' : category,
            'content' : content,
        },
        headers: { 'X-CSRFToken': csrfToken },  // Django의 CSRF 토큰을 헤더에 포함
        success : function(data){
            alert('저장이 완료되었습니다.');
            //modal.style.display='none';
            modal.style.visibility = 'hidden';
            modal.style.opacity = '0';
        },
        error : function(jqXHR, textStatus, errorThrown){
            alert("저장에 실패했습니다. 다시 시도해주세요.");
        }
    });
}

//모달창에서 취소버튼 클릭-> 모달창 닫기

function closeModal(){
    modal.style.visibility='hidden';
    modal.style.opacity = '0';
}



//모달창 밖 클릭했을 때도 -> 모달창 닫기
window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.visibility = "hidden";
      modal.style.opacity = '0';
      $('body').css('overflow-y','unset'); // 스크롤 막기 풀기
    }
}
