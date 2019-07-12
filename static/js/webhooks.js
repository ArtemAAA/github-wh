(() => {
  function createEventElement(event) {
    return `
      <div class="media text-muted pt-3">
        <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
          <strong class="d-block text-gray-dark">
            ${event.event_name}
            (<a href="${event.sender}">${event.sender.substring(event.sender.lastIndexOf('/')+1)}</a>)
          </strong>
          <span>
            Repo:
            <a href="${event.repository}">
              ${event.repository.substring(event.repository.lastIndexOf('/')+1)}
            </a>
          </span>
          <pre class="pre-scrollable">${JSON.stringify(event.event_data, undefined, 2)}</pre>
        </div>
      </div>
    `;
  };

  const $eventsList = $('#events-list');

  // load data from db
  $.get(window.URLS['apiWebhookEvents'], (data) => {
    for (const event of data) {
      $eventsList.prepend(createEventElement(event));
    }
  });

  // websockets
  const ws = new WebSocket(`ws://${window.location.host}/ws/webhooks/events/`);
  ws.onmessage = function(e) {
    $eventsList.prepend(createEventElement(JSON.parse(e.data)));
  };

})();
