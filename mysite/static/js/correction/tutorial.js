var currentStep = 1;
var maxSteps = 5;

// 각 단계별로 강조할 요소를 명시하는 객체
var stepFocusElements = {
    1: '#option-area',
    2: '#icon_view',
    3: '#syn-icon-area',
    4: '#right-icons',
    5: '#coachButton'
};


function showSpotlight() {
    $('#tutorial_spotlight').addClass('is-visible');
}

function hideSpotlight() {
    $('#tutorial_spotlight').removeClass('is-visible');
}


function updateSpotlight() {
    var focusElementInfo = stepFocusElements[currentStep];
    var $spotlight = $("#tutorial_spotlight");
    if (typeof focusElementInfo === "string") {
        var $focusElement = $(focusElementInfo);
        var offset = $focusElement.offset();
        var padding = 5; // 스포트라이트 영역 패딩
        $spotlight.css({
            width: $focusElement.outerWidth(true) + 2 * padding,
            height: $focusElement.outerHeight(true) + 2 * padding,
            transform: 'translate3d(' + (offset.left - padding) + 'px,' + (offset.top - padding) + 'px, 0px)',
        });
    } else {
        $spotlight.css({
            width: focusElementInfo.width + 2 * padding,
            height: focusElementInfo.height + 2 * padding,
            transform: 'translate3d(' + (focusElementInfo.left - padding) + 'px,' + (focusElementInfo.top - padding) + 'px, 0px)',
        });
    }
}

  
function initTutorial() {
    currentStep = 1;
    $('.bullets span').removeClass('is-active');
    $('.bullets span[data-index="1"]').addClass('is-active');

    //다 숨기고 무조건 1단계만 띄우기
    $(".description div").hide();
    $("#desc1").show();

    //추천유의어 아이콘 표시
    $('#syn_ment').show();
    $('#synonymButton').show();
    isTutorialMode = true;  // 튜토리얼 모드 시작

    $('body').css('overflow-y', 'hidden'); // 스크롤 막기

    updateSpotlight();
    showSpotlight();
}


function moveToStep(previousStep, targetStep) {
    $(`.bullets span[data-index="${previousStep}"]`).removeClass('is-active');
    $("#desc" + previousStep).hide();
  
    if (targetStep <= maxSteps) {
      $(`.bullets span[data-index="${targetStep}"]`).addClass('is-active');
      $("#desc" + targetStep).show();
      currentStep = targetStep;
    
      updateSpotlight();
      showSpotlight();
    
    } else {
        //맨 마지막 step이면 모달 닫음
        closeModal();
    }
  }


function handleNextButton() {
    $("#next-step").click(function() {
      if (currentStep < maxSteps) {
        moveToStep(currentStep, currentStep + 1);
      } else {
        closeModal();
      }
    });
  }

function handleBulletClick() {
    $(".bullets span").click(function() {
        var clickedStep = $(this).data('index');
        if (clickedStep != currentStep) {
            moveToStep(currentStep, clickedStep);
        }
    });
}

function closeModal() {
    //추천유의어 아이콘 숨김
    isTutorialMode = false;  // 튜토리얼 모드 종료
    $('#syn_ment').hide();
    $('#synonymButton').hide();
    synbtn.off('click'); // 아이콘의 클릭 이벤트 핸들러 제거
    
    $("#tutorial_spotlight").css({
        width: 0,
        height: 0,
        top: 0,
        left:0,
        transform: 'translate(0, 0)'
    });
    hideSpotlight();
    $("#tutorialModal").hide();

    $('body').css('overflow-y','unset'); // 스크롤 막기 풀기
}

window.moveToStep = moveToStep;
window.handleNextButton = handleNextButton;
window.handleBulletClick = handleBulletClick;
window.initTutorial = initTutorial;
