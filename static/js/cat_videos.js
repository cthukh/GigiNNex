const posts = [];

        function addPost() {
            const postContent = document.getElementById('postContent').value;
            if (postContent.trim() === '') return;

            const newPost = {
                content: postContent,
                comments: []
            };
            posts.push(newPost);
            document.getElementById('postContent').value = '';
            renderPosts();
        }

        function renderPosts() {
            const postsContainer = document.getElementById('postsContainer');
            postsContainer.innerHTML = '';

            posts.forEach((post, index) => {
                const postDiv = document.createElement('div');
                postDiv.className = 'post';
                postDiv.innerHTML = `
                    <p>${post.content}</p>
                    <input type="text" id="commentInput${index}" placeholder="Escribe un comentario...">
                    <button onclick="addComment(${index})">Comentar</button>
                    <div class="comments" id="comments${index}"></div>
                `;
                postsContainer.appendChild(postDiv);
            });
        }

        function addComment(postIndex) {
            const commentInput = document.getElementById(`commentInput${postIndex}`);
            const commentContent = commentInput.value;
            if (commentContent.trim() === '') return;

            posts[postIndex].comments.push(commentContent);
            commentInput.value = '';
            renderComments(postIndex);
        }

        function renderComments(postIndex) {
            const commentsContainer = document.getElementById(`comments${postIndex}`);
            commentsContainer.innerHTML = '';

            posts[postIndex].comments.forEach(comment => {
                const commentDiv = document.createElement('div');
                commentDiv.textContent = comment;
                commentsContainer.appendChild(commentDiv);
            });
        }