// Adds a `.checked` visual state to the checkbox-tile wrapper when ticked.
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.checkbox-tile').forEach(function (tile) {
    const input = tile.querySelector('input[type="checkbox"]');
    if (!input) return;
    const sync = () => tile.classList.toggle('checked', input.checked);
    sync();
    input.addEventListener('change', sync);
  });
});
