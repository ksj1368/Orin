var currentStep = 0;

function moveToStep(previousStep, targetStep) {
    $(`#icon_service[data-index="${previousStep}"]`).attr('name','radio-button-off');
    $("#service" + previousStep).hide();
  
    $(`#icon_service[data-index="${targetStep}"]`).attr('name','radio-button-on');
    $("#service" + targetStep).css('display','flex');
    currentStep = targetStep;
};

// 다음 버튼 클릭 시 넘어감
$("#icon_nextBtn").click(function() {
    moveToStep(currentStep, (currentStep + 1) % 6);
});

// 동그라미 버튼 클릭 시 넘어감
$("[id^=icon_service]").click(function() {
    var clickedStep = $(this).data('index');

    if (clickedStep != currentStep) {
        moveToStep(currentStep, clickedStep);
    };
});

// 자동 넘김
function autoStep() {
    $('#icon_nextBtn').trigger('click');
};

setInterval(autoStep, 13000); // 13초마다 넘겨지게