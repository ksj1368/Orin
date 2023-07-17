const deleteBtn = document.getElementById('delete_button');
const modal = document.getElementById('modal');
const closeBtn = document.getElementById('close_button');

deleteBtn.onclick = function() {
    modal.style.display = 'flex';
}

closeBtn.onclick = function() {
    modal.style.display = 'none';
}

window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }