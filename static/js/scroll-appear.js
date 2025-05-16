document.addEventListener('DOMContentLoaded', () => {
  const items = document.querySelectorAll('.fade-up');
  console.log('🌍 window.location.href =', window.location.href);
  console.log('🎯 Найдено элементов .fade-up:', items.length);

  if (!items.length) {
    console.warn('⚠️ Нет элементов .fade-up — пропускаем scroll observer');
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const i = entry.target.dataset.index ?? '?';
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        console.log(`✅ Показан элемент ${i}`);
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -10% 0px'
  });

  elements.forEach((el, i) => {
    el.setAttribute('data-index', i);
    const side = Math.random() > 0.5 ? 'align-left' : 'align-right';
    el.classList.add(side);
    console.log(`🔧 ${i}: side ${side}`);
    observer.observe(el);
  });

  // ⬇️ Параллакс эффект
  window.addEventListener('scroll', () => {
    const visibleItems = document.querySelectorAll('.fade-up.visible');
    visibleItems.forEach(item => {
      const rect = item.getBoundingClientRect();
      const offsetY = (window.innerHeight - rect.top) * 0.04;
      item.style.transform = `translateY(${offsetY}px)`;
    });
  });
});
