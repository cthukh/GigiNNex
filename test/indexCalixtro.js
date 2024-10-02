
console.log("hola22222")
const stars = document.querySelectorAll('.star');
const selectedRating = document.getElementById('selected-rating');
let currentRating = 0;

stars.forEach((star, index) => {
    star.addEventListener('click', () => {
        currentRating = index + 1;
        updateStars();
        selectedRating.textContent = `Calificación: ${currentRating} estrellas`;
    });
});

function updateStars() {
    stars.forEach((star, index) => {
        if (index < currentRating) {
            star.classList.add('selected');
        } else {
            star.classList.remove('selected');
        }
    });
}

// Comment section logic
const commentForm = document.getElementById('comment-form');
const commentInput = document.getElementById('comment');
const commentsList = document.getElementById('comments-list');

commentForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const commentText = commentInput.value.trim();
    if (commentText !== '') {
        const commentDiv = document.createElement('div');
        commentDiv.classList.add('comment');
        commentDiv.textContent = commentText;
        commentsList.appendChild(commentDiv);
        commentInput.value = '';
    }
});