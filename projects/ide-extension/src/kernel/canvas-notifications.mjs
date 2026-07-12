function revisionNotice(current) {
  return {
    schema_version: '1',
    type: 'canvas.revision.available',
    surface_id: current.surface_id,
    revision_id: current.revision.revision_id
  };
}

export function createCanvasNotificationHub() {
  const clients = new Set();
  let nextEventId = 1;

  function send(response, current) {
    const id = nextEventId;
    nextEventId += 1;
    response.write(`id: ${id}\ndata: ${JSON.stringify(revisionNotice(current))}\n\n`);
    return id;
  }

  return {
    register(response, current = null) {
      response.writeHead(200, {
        'content-type': 'text/event-stream; charset=utf-8',
        'cache-control': 'no-cache, no-transform',
        connection: 'keep-alive',
        'x-accel-buffering': 'no'
      });
      response.write(': canvas notifications connected\n\n');
      clients.add(response);
      const unregister = () => clients.delete(response);
      response.once('close', unregister);
      if (current) send(response, current);
      return unregister;
    },

    broadcast(current) {
      for (const response of [...clients]) {
        if (response.destroyed || response.writableEnded) {
          clients.delete(response);
          continue;
        }
        send(response, current);
      }
    },

    close() {
      for (const response of clients) response.end();
      clients.clear();
    },

    get clientCount() {
      return clients.size;
    }
  };
}
