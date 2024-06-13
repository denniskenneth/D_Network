document.addEventListener('DOMContentLoaded', function () {
  const followBtn = document.querySelector('#follow_btn');

  followBtn.addEventListener('click', (e) => follow(followBtn.dataset.userId));
  //   follow();
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
