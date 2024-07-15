document.addEventListener('DOMContentLoaded', function () {
  const followBtn = document.querySelector('#follow_btn');
  const allPostBtn = document.querySelector('#allPosts');
  const fllwnPostBtn = document.querySelector('#fllwnPosts');

  if (followBtn != null) {
    followBtn.addEventListener('click', (e) =>
      follow(followBtn.dataset.userId)
    );
  }
  allPostBtn.addEventListener('click', () => posts('all'));
  fllwnPostBtn.addEventListener('click', (e) => posts('following'));
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
