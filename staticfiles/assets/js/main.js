
(function() {
    "use strict";
  
    /**
     * Easy selector helper function
     */
    const select = (el, all = false) => {
      el = el.trim()
      if (all) {
        return [...document.querySelectorAll(el)]
      } else {
        return document.querySelector(el)
      }
    }
  
    /**
     * Easy event listener function
     */
    const on = (type, el, listener, all = false) => {
      if (all) {
        select(el, all).forEach(e => e.addEventListener(type, listener))
      } else {
        select(el, all).addEventListener(type, listener)
      }
    }
  
    /**
     * Search bar toggle
     */
    if (select('.search-bar-toggle')) {
      on('click', '.search-bar-toggle', function(e) {
        select('.search-bar').classList.toggle('search-bar-show')
      })
    }
  
   
  
  
  })();
  
  document.addEventListener('DOMContentLoaded', () => {
    "use strict";
  
     
    var swiper = new Swiper(".sliderFeaturedPosts", {
      spaceBetween: 0,
      speed: 500,
      centeredSlides: true,
      loop: true,
      slideToClickedSlide: true,
      autoplay: {
        delay: 3000,
        disableOnInteraction: false,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
      navigation: {
        nextEl: ".custom-swiper-button-next",
        prevEl: ".custom-swiper-button-prev",
      },
    });
  
    /**
     * Open and close the search form.
     */
  
  
    /**
     * Animation on scroll function and init
     */
    function aos_init() {
      AOS.init({
        duration: 1000,
        easing: 'ease-in-out',
        once: true,
        mirror: false
      });
    }
    window.addEventListener('load', () => {
      aos_init();
    });
  
  });
  
  /* slider  */
  
  $(document).ready(function()
  {
  
     
          if($('.bbb_viewed_slider').length)
          {
              var viewedSlider = $('.bbb_viewed_slider');
  
              viewedSlider.owlCarousel(
              {
                  loop:true,
                  margin:30,
                  autoplay:true,
                  autoplayTimeout:6000,
                  nav:false,
                  dots:false,
                  responsive:
                  {
                      0:{items:1},
                      575:{items:2},
                      768:{items:3},
                      991:{items:4},
                      1199:{items:6}
                  }
              });
  
              if($('.bbb_viewed_prev').length)
              {
                  var prev = $('.bbb_viewed_prev');
                  prev.on('click', function()
                  {
                      viewedSlider.trigger('prev.owl.carousel');
                  });
              }
  
              if($('.bbb_viewed_next').length)
              {
                  var next = $('.bbb_viewed_next');
                  next.on('click', function()
                  {
                      viewedSlider.trigger('next.owl.carousel');
                  });
              }
          }
  
  
      });