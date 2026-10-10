/* ==========================================================================
   DUNVEA — theme.js
   Composants : galerie produit, choix de variante, quantité, ajout au panier,
   notification panier, barre d'achat fixe, recommandations, annonces, panier.
   ========================================================================== */
(() => {
  'use strict';

  const theme = window.theme || {};

  /* ---------- Utilitaires ---------- */
  const formatMoney = (cents, format = theme.moneyFormat || '{{amount_with_comma_separator}} €') => {
    if (typeof cents === 'string') cents = cents.replace('.', '');
    const value = Number(cents);
    const placeholder = /\{\{\s*(\w+)\s*\}\}/;
    const fmt = (number, decimals, thousands = '.', decimal = ',') => {
      const fixed = (number / 100).toFixed(decimals);
      const [whole, frac] = fixed.split('.');
      const withThousands = whole.replace(/(\d)(?=(\d{3})+(?!\d))/g, `$1${thousands}`);
      return frac ? `${withThousands}${decimal}${frac}` : withThousands;
    };
    const match = format.match(placeholder);
    if (!match) return fmt(value, 2);
    let out;
    switch (match[1]) {
      case 'amount': out = fmt(value, 2, ',', '.'); break;
      case 'amount_no_decimals': out = fmt(value, 0, ',', '.'); break;
      case 'amount_with_comma_separator': out = fmt(value, 2, '.', ','); break;
      case 'amount_no_decimals_with_comma_separator': out = fmt(value, 0, '.', ','); break;
      case 'amount_with_space_separator': out = fmt(value, 2, ' ', ','); break;
      case 'amount_with_apostrophe_separator': out = fmt(value, 2, "'", '.'); break;
      default: out = fmt(value, 2, '.', ',');
    }
    return format.replace(placeholder, out);
  };

  const updateCartCount = (count) => {
    document.querySelectorAll('[data-cart-count]').forEach((el) => {
      el.textContent = count;
      if (el.classList.contains('cart-count')) el.hidden = count === 0;
    });
  };

  /* ---------- Galerie produit ---------- */
  class MediaGallery extends HTMLElement {
    connectedCallback() {
      this.slider = this.querySelector('[data-slider]');
      this.slides = [...this.querySelectorAll('.gallery__slide')];
      this.thumbs = [...this.querySelectorAll('[data-thumb]')];
      this.counter = this.querySelector('[data-current]');
      this.prev = this.querySelector('[data-prev]');
      this.next = this.querySelector('[data-next]');
      this.lightbox = this.querySelector('[data-lightbox]');
      if (!this.slider) return;

      this.thumbs.forEach((thumb) => thumb.addEventListener('click', () => this.goTo(Number(thumb.dataset.thumb))));
      this.prev?.addEventListener('click', () => this.goTo(this.index - 1));
      this.next?.addEventListener('click', () => this.goTo(this.index + 1));

      let ticking = false;
      this.slider.addEventListener('scroll', () => {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(() => {
          const i = Math.round(this.slider.scrollLeft / this.slider.clientWidth);
          this.setActive(i);
          ticking = false;
        });
      }, { passive: true });

      this.querySelectorAll('[data-zoom]').forEach((btn) => btn.addEventListener('click', () => this.openLightbox(btn)));
      this.querySelector('[data-lightbox-close]')?.addEventListener('click', () => this.lightbox.close());
      this.lightbox?.addEventListener('click', (e) => { if (e.target === this.lightbox) this.lightbox.close(); });

      // Démarre sur l'image de la variante sélectionnée
      const active = this.slides.findIndex((s) => s.classList.contains('is-active'));
      this.index = 0;
      if (active > 0) requestAnimationFrame(() => this.goTo(active, false));
      else this.setActive(0);
    }

    goTo(i, smooth = true) {
      if (!this.slides.length) return;
      const index = Math.max(0, Math.min(i, this.slides.length - 1));
      this.slider.scrollTo({ left: index * this.slider.clientWidth, behavior: smooth ? 'smooth' : 'auto' });
      this.setActive(index);
    }

    goToMedia(mediaId) {
      const i = this.slides.findIndex((s) => s.dataset.mediaId === String(mediaId));
      if (i > -1) this.goTo(i);
    }

    setActive(i) {
      if (i === this.index && this._initialised) return;
      this._initialised = true;
      this.index = i;
      this.slides.forEach((s, n) => s.classList.toggle('is-active', n === i));
      this.thumbs.forEach((t, n) => {
        const on = n === i;
        t.classList.toggle('is-active', on);
        if (on) {
          t.setAttribute('aria-current', 'true');
          const rail = t.closest('.gallery__thumbs');
          if (rail && rail.scrollWidth > rail.clientWidth) {
            rail.scrollTo({ left: t.offsetLeft - rail.clientWidth / 2 + t.clientWidth / 2, behavior: 'smooth' });
          }
        } else {
          t.removeAttribute('aria-current');
        }
      });
      if (this.counter) this.counter.textContent = i + 1;
      if (this.prev) this.prev.disabled = i === 0;
      if (this.next) this.next.disabled = i === this.slides.length - 1;
    }

    openLightbox(btn) {
      if (!this.lightbox || typeof this.lightbox.showModal !== 'function') return;
      this.lightbox.showModal();
      document.body.style.overflow = 'hidden';
      this.lightbox.addEventListener('close', () => { document.body.style.overflow = ''; }, { once: true });
      const target = this.lightbox.querySelector(`[data-lightbox-index="${btn.dataset.zoom}"]`);
      if (target) target.scrollIntoView({ block: 'start' });
    }
  }
  customElements.define('media-gallery', MediaGallery);

  /* ---------- Choix de variante ---------- */
  class VariantPicker extends HTMLElement {
    connectedCallback() {
      this.sectionId = this.dataset.sectionId;
      this.root = this.closest('[data-section]') || document;
      try {
        this.variants = JSON.parse(this.querySelector('[data-variants]').textContent);
      } catch (e) {
        this.variants = [];
      }
      this.addEventListener('change', () => this.onChange());
      this.markUnavailable();
    }

    selectedOptions() {
      const fieldsets = [...this.querySelectorAll('fieldset')];
      return fieldsets.map((fs) => fs.querySelector('input:checked')?.value);
    }

    onChange() {
      const options = this.selectedOptions();
      const variant = this.variants.find((v) => v.options.every((o, i) => o === options[i]));

      options.forEach((value, i) => {
        const label = this.querySelector(`[data-selected-value="${i}"]`);
        if (label) label.textContent = value;
      });
      this.markUnavailable();

      const button = this.root.querySelector('[data-add-button]');
      const buttonLabel = this.root.querySelector('[data-add-label]');
      const stickyButton = this.root.querySelector('[data-sticky-add]');
      const idInput = this.root.querySelector('[data-variant-id]');

      if (!variant) {
        if (button) button.disabled = true;
        if (stickyButton) stickyButton.disabled = true;
        if (buttonLabel) buttonLabel.textContent = theme.strings.unavailable;
        return;
      }

      if (idInput) idInput.value = variant.id;
      if (button) button.disabled = !variant.available;
      if (stickyButton) stickyButton.disabled = !variant.available;
      if (buttonLabel) buttonLabel.textContent = variant.available ? theme.strings.addToCart : theme.strings.soldOut;

      this.updatePrice(variant);

      if (variant.featured_media_id) {
        this.root.querySelector('media-gallery')?.goToMedia(variant.featured_media_id);
      }

      const url = new URL(window.location.href);
      url.searchParams.set('variant', variant.id);
      window.history.replaceState({}, '', url.toString());

      this.dispatchEvent(new CustomEvent('variant:change', { bubbles: true, detail: { variant } }));
    }

    updatePrice(variant) {
      const priceRoot = this.root.querySelector('.product__price [data-price]');
      const sticky = this.root.querySelector('[data-sticky-price]');
      if (sticky) sticky.textContent = formatMoney(variant.price);
      if (!priceRoot) return;

      const current = priceRoot.querySelector('[data-price-current]');
      const compare = priceRoot.querySelector('[data-price-compare]');
      const savings = priceRoot.querySelector('[data-price-savings]');
      const onSale = variant.compare_at_price > variant.price;

      if (current) current.textContent = formatMoney(variant.price);
      priceRoot.classList.toggle('price--on-sale', onSale);
      if (compare) {
        compare.hidden = !onSale;
        compare.textContent = onSale ? formatMoney(variant.compare_at_price) : '';
      }
      if (savings) {
        savings.hidden = !onSale;
        savings.textContent = onSale
          ? theme.strings.youSave.replace('[amount]', formatMoney(variant.compare_at_price - variant.price))
          : '';
      }
    }

    // Grise les valeurs qui ne mènent à aucune variante disponible
    markUnavailable() {
      const selected = this.selectedOptions();
      this.querySelectorAll('input[type="radio"]').forEach((input) => {
        const index = Number(input.dataset.optionIndex);
        const candidate = [...selected];
        candidate[index] = input.value;
        const match = this.variants.find((v) => v.options.every((o, i) => o === candidate[i]));
        input.classList.toggle('is-unavailable', !match || !match.available);
      });
    }
  }
  customElements.define('variant-picker', VariantPicker);

  /* ---------- Quantité ---------- */
  class QuantityInput extends HTMLElement {
    connectedCallback() {
      this.input = this.querySelector('input');
      this.querySelectorAll('button').forEach((btn) => btn.addEventListener('click', () => {
        const min = Number(this.input.min) || 0;
        const current = Number(this.input.value) || min;
        const next = btn.name === 'plus' ? current + 1 : Math.max(min, current - 1);
        if (next !== current) {
          this.input.value = next;
          this.input.dispatchEvent(new Event('change', { bubbles: true }));
        }
      }));
    }
  }
  customElements.define('quantity-input', QuantityInput);

  /* ---------- Ajout au panier ---------- */
  class ProductForm extends HTMLElement {
    connectedCallback() {
      this.form = this.querySelector('form');
      this.error = this.querySelector('[data-error]');
      this.button = this.querySelector('[data-add-button]');
      this.form?.addEventListener('submit', (e) => this.onSubmit(e));
    }

    async onSubmit(event) {
      event.preventDefault();
      if (this.button?.disabled || this.button?.classList.contains('is-loading')) return;
      this.button?.classList.add('is-loading');
      if (this.error) this.error.hidden = true;

      try {
        const body = new FormData(this.form);
        const response = await fetch(`${theme.routes.cartAdd}.js`, {
          method: 'POST',
          headers: { Accept: 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
          body,
        });
        const data = await response.json();
        if (!response.ok || data.status) throw new Error(data.description || data.message || theme.strings.cartError);

        const cart = await fetch(`${theme.routes.cart}.js`).then((r) => r.json());
        updateCartCount(cart.item_count);
        document.querySelector('cart-notification')?.show(data);
      } catch (err) {
        if (this.error) {
          this.error.textContent = err.message || theme.strings.cartError;
          this.error.hidden = false;
        }
      } finally {
        this.button?.classList.remove('is-loading');
      }
    }
  }
  customElements.define('product-form', ProductForm);

  /* ---------- Notification panier ---------- */
  class CartNotification extends HTMLElement {
    connectedCallback() {
      this.panel = this.querySelector('[role="dialog"]');
      this.querySelectorAll('[data-close]').forEach((el) => el.addEventListener('click', () => this.hide()));
      this.addEventListener('keyup', (e) => { if (e.key === 'Escape') this.hide(); });
    }

    show(item) {
      const target = this.querySelector('[data-item]');
      if (target && item) {
        const img = item.image ? `<img src="${item.image}${item.image.includes('?') ? '&' : '?'}width=200" alt="" width="80" height="100" loading="lazy">` : '<span></span>';
        const variant = item.variant_title ? `<p class="cart-notification__item-meta">${item.variant_title}</p>` : '';
        target.innerHTML = `${img}<div><p class="cart-notification__item-title">${item.product_title}</p>${variant}<p class="cart-notification__item-meta">${item.quantity} × ${formatMoney(item.final_price)}</p></div>`;
      }
      this.lastFocus = document.activeElement;
      this.hidden = false;
      this.panel?.focus();
      clearTimeout(this.timer);
    }

    hide() {
      this.hidden = true;
      this.lastFocus?.focus?.();
    }
  }
  customElements.define('cart-notification', CartNotification);

  /* ---------- Barre d'achat fixe (mobile) ---------- */
  class StickyAtc extends HTMLElement {
    connectedCallback() {
      const section = this.closest('[data-section]');
      const anchor = section?.querySelector('.product__buy');
      if (!anchor || !('IntersectionObserver' in window)) return;
      this.hidden = false;
      const footer = document.querySelector('.footer');
      let pastButton = false;
      let footerVisible = false;
      const update = () => this.classList.toggle('is-visible', pastButton && !footerVisible);
      new IntersectionObserver(([entry]) => {
        pastButton = !entry.isIntersecting && entry.boundingClientRect.top < 0;
        update();
      }).observe(anchor);
      if (footer) {
        new IntersectionObserver(([entry]) => { footerVisible = entry.isIntersecting; update(); }).observe(footer);
      }
    }
  }
  customElements.define('sticky-atc', StickyAtc);

  /* ---------- Recommandations produit ---------- */
  class ProductRecommendations extends HTMLElement {
    connectedCallback() {
      if (!this.dataset.url || this.querySelector('.product-grid')) return;
      const load = () => {
        fetch(this.dataset.url)
          .then((r) => r.text())
          .then((html) => {
            const doc = new DOMParser().parseFromString(html, 'text/html');
            const fresh = doc.querySelector('product-recommendations');
            if (fresh && fresh.innerHTML.trim().length) this.innerHTML = fresh.innerHTML;
            else this.closest('.shopify-section')?.setAttribute('hidden', '');
          })
          .catch(() => {});
      };
      if (!('IntersectionObserver' in window)) return load();
      const io = new IntersectionObserver((entries) => {
        if (!entries[0].isIntersecting) return;
        io.disconnect();
        load();
      }, { rootMargin: '0px 0px 400px 0px' });
      io.observe(this);
    }
  }
  customElements.define('product-recommendations', ProductRecommendations);

  /* ---------- Barre d'annonce (rotation) ---------- */
  class AnnouncementBar extends HTMLElement {
    connectedCallback() {
      const messages = [...this.querySelectorAll('.announcement__message')];
      if (messages.length < 2 || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      let i = 0;
      setInterval(() => {
        messages[i].classList.remove('is-active');
        i = (i + 1) % messages.length;
        messages[i].classList.add('is-active');
      }, Number(this.dataset.speed || 5) * 1000);
    }
  }
  customElements.define('announcement-bar', AnnouncementBar);

  /* ---------- Panier : mise à jour auto des quantités ---------- */
  class CartItems extends HTMLElement {
    connectedCallback() {
      const form = this.closest('form');
      let timer;
      this.addEventListener('change', (e) => {
        if (!e.target.matches('input[name="updates[]"]')) return;
        clearTimeout(timer);
        timer = setTimeout(() => form?.submit(), 450);
      });
    }
  }
  customElements.define('cart-items', CartItems);

  /* ---------- Menu mobile : fermeture via Échap / overlay ---------- */
  document.addEventListener('keyup', (e) => {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('details[data-drawer][open]').forEach((d) => {
      d.removeAttribute('open');
      d.querySelector('summary')?.focus();
    });
  });
  document.addEventListener('click', (e) => {
    const close = e.target.closest('[data-drawer-close]');
    if (close) close.closest('details[data-drawer]')?.removeAttribute('open');
  });
  document.addEventListener('toggle', (e) => {
    if (e.target.matches?.('details[data-drawer]')) {
      document.body.style.overflow = e.target.open ? 'hidden' : '';
    }
  }, true);

  /* ---------- Apparition douce des sections ---------- */
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    document.querySelectorAll('.reveal').forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll('.reveal').forEach((el) => el.classList.add('is-visible'));
  }
})();
