document.addEventListener('DOMContentLoaded', function () {
  // const followBtn = document.querySelector('#follow_btn');
  // const allPostBtn = document.querySelector('#allPosts');
  // const fllwnPostBtn = document.querySelector('#fllwnPosts');

  // Event delegation for edit buttons
  document.addEventListener('click', function (event) {
    const btn = event.target;
    // console.log(btn.id === 'edit_btn');

    // Handle click on edit button
    if (btn.id === 'edit_btn') {
      const card = btn.closest('.card');
      const editForm = card.querySelector('#postEditForm');
      const cardContent = card.querySelector('#cardContent');
      const textarea = editForm.querySelector('.form-control');
      const postContent = cardContent.querySelector('.card-text');
      const post_id = btn.dataset.postId;

      // Toggle edit mode
      editToSaveBtn(btn, editForm, cardContent, textarea, postContent, post_id);
    }
  });

  // Event listener for follow button (assuming followBtn is present)
  const followBtn = document.querySelector('#follow_btn');
  if (followBtn) {
    followBtn.addEventListener('click', (e) =>
      follow(followBtn.dataset.userId)
    );
  }

  // Event listeners for posts filtering buttons
  const allPostBtn = document.querySelector('#allPosts');
  const fllwnPostBtn = document.querySelector('#fllwnPosts');

  if (allPostBtn) {
    allPostBtn.addEventListener('click', () => posts('all'));
  }

  if (fllwnPostBtn) {
    fllwnPostBtn.addEventListener('click', () => posts('following'));
  }
});

function follow(user_id) {
  fetch(`/follow/${user_id}/`, {
    method: 'post',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
  })
    .then((response) =>
      response.json().then((data) => ({ data, status: response.status }))
    )
    .then(({ data, status }) => {
      console.log(data.message); // Log the message from the server response

      // Reload the page if the response was successful
      if (status >= 200 && status < 300) {
        window.location.reload(true);
      }
    })
    .catch((error) => console.error(error.message));
}

function card() {
  const div1 = document.createElement('div');
  div1.classList.add('card', 'mt-3');

  const div2 = document.createElement('div');
  div2.classList.add('card-body');

  const header_h4 = document.createElement('h4');
  const username_a = document.createElement('a');
  const date_span = document.createElement('span');
  date_span.classList.add('text-muted');

  header_h4.appendChild(username_a);
  header_h4.appendChild(date_span);

  const text_p = document.createElement('p');
  text_p.classList.add('card-text');

  const icon_a = document.createElement('a');
  icon_a.classList.add('red-link');
  const icon_i = document.createElement('i');
  icon_i.classList.add('fa-regular', 'fa-heart');
  icon_a.appendChild(icon_i);

  const num_span = document.createElement('span');
  num_span.classList.add('ml-1');

  div2.appendChild(header_h4);
  div2.appendChild(text_p);
  div2.appendChild(icon_a);
  div2.appendChild(num_span);

  div1.appendChild(div2);

  document.querySelector('#posts').appendChild(div1);
}

function posts(pageName) {
  // fetch(`/posts/${pageName}/`)
  //   .then((response) => {
  //     if (!response.ok) {
  //       throw new Error(`HTTP error! Status: ${response.status}`);
  //     }
  //     return response.json();
  //   })
  //   .then((posts) => {
  //     card();
  //     posts.forEach((post) => console.log(post.id));
  //   })
  //   .catch((error) => console.log(error.message));
  // console.log(pageName);
  // fetch(`/postsroute`)
  //   .then()
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function editToSaveBtn(
  btn,
  editForm,
  cardContent,
  textarea,
  p_postContent,
  post_id
) {
  // const editForm = document.querySelector('#postEditForm');
  // const cardContent = document.querySelector('#cardContent');
  // const textarea = document.querySelector('#postEditTxtAra');
  // const p_postContent = document.querySelector('#postContent');

  // Toggle edit mode
  if (btn.textContent == 'Save') {
    let result = saveEdit(p_postContent, post_id, textarea);

    if (result) {
      btn.textContent = 'Edit';
      editForm.classList.toggle('hide');
      cardContent.classList.toggle('hide');
    }
  } else {
    btn.textContent = 'Save';
    // cardContent.style.display = 'none';
    cardContent.classList.toggle('hide');

    textarea.value = p_postContent.textContent.trim();
    editForm.classList.toggle('hide');
  }
}

function saveEdit(content, post_id, textarea) {
  fetch(`/`, {
    method: 'PUT',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
      content: textarea.value,
      post_id: post_id,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'success') {
        content.textContent = textarea.value;
      } else {
        console.error('Update failed', data.message);
        return false;
        ``;
      }
    })
    .catch((error) => {
      console.log('Error:', error);
      return false;
    });

  return true;
}
