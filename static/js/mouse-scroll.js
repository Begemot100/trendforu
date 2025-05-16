document.addEventListener('DOMContentLoaded', () => {
  const scrollBall = document.getElementById('scrollBall');
  if (!scrollBall) return;

  let currentX = window.innerWidth / 2;
  let currentY = window.innerHeight - 100;
  let targetX = currentX;
  let targetY = currentY;
  const lerpFactor = 0.07;

  const gradientColors = [
    'rgba(255, 255, 255, 0.2)',
    'rgba(255, 0, 100, 0.2)',
    'rgba(0, 255, 150, 0.2)',
    'rgba(255, 255, 0, 0.2)'
  ];
  let colorIndex = 0;

  function updateColor() {
    scrollBall.style.background = gradientColors[colorIndex];
    colorIndex = (colorIndex + 1) % gradientColors.length;
  }

  function updateTarget(x, y) {
    targetX = x;
    targetY = y;
  }

  document.addEventListener('mousemove', e => updateTarget(e.clientX, e.clientY));
  document.addEventListener('touchmove', e => {
    const touch = e.touches[0];
    if (touch) updateTarget(touch.clientX, touch.clientY);
  }, { passive: true });

  function animate() {
    currentX += (targetX - currentX) * lerpFactor;
    currentY += (targetY - currentY) * lerpFactor;

    scrollBall.style.left = `${currentX}px`;
    scrollBall.style.top = `${currentY}px`;
    scrollBall.style.transform = 'translate(-50%, -50%)';

    requestAnimationFrame(animate);
  }

  animate();
  setInterval(updateColor, 1500);
});
