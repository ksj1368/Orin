const btn = document.getElementById('openBtn');
const modal = document.getElementById('modal');
const closeBtn = document.getElementById('closeBtn');

btn.onclick = function() {
    modal.style.display = 'flex';
    modal.style.justifyContent = 'center';
    modal.style.alignItems = 'center';
}

closeBtn.onclick = function() {
    modal.style.display = 'none';
}

function validateForm() {
    var checkbox = document.getElementById("myCheckbox");
    if (checkbox.checked) {
      return true; // 체크되었을 때 폼이 제출됨
    } else {
      alert("약관에 동의해주세요.");
      return false; // 체크되지 않았을 때 폼 제출이 중지됨
    }
  }