document.addEventListener('alpine:init', () => {
  Alpine.store('toasts', {
    items: [],
    add(message, type = 'success', timeout = 4000) {
      const id = Date.now() + Math.random();
      this.items.push({ id, message, type, timeout });
      if (timeout) setTimeout(() => this.remove(id), timeout);
      return id;
    },
    remove(id) {
      this.items = this.items.filter((t) => t.id !== id);
    },
  });
});

window.notify = (message, type = 'success', timeout = 4000) =>
  window.Alpine && window.Alpine.store('toasts').add(message, type, timeout);
